"""Schema compilation: ComplexType component"""

__version__="$Revision: 1.37 $"
# $Id: ComplexType.py,v 1.37 2007-02-16 15:30:12 ht Exp $

import copy
import types

from Component import Component
from Group import Group, Sequence
from Particle import Particle
from Type import Type
from SimpleType import SimpleType
from QName import QName
from AttributeUse import AttributeUse
from FSM import UniqueFSM

from XSV import xsvNS

from elts.simpleTypeElt import simpleTypeElt
from elts.rulElt import restrictionElt

from SchemaError import shouldnt

class ComplexType(Type):
  idt=0
  def __init__(self,sschema,xrpr):
    Type.__init__(self,sschema,xrpr)
    if xrpr is not None:
      self.basetypeName=xrpr.basetype
      self.abstract=xrpr.abstract
      if xrpr.final=='':
        self.final=()
      else:
        self.final=xrpr.final.split()
      if '#all' in self.final:
        self.final=('restriction','extension')
      if xrpr.block=='':
        self.prohibitedSubstitutions=()
      else:
        self.prohibitedSubstitutions=xrpr.block.split()
      if '#all' in self.prohibitedSubstitutions:
        self.prohibitedSubstitutions=('restriction','extension')

  def __unicode__(self):
    if self.basetype is not None:
      if isinstance(self.basetype,QName):
	bt=" based on %s"%self.basetype
      else:
	bt=" based on {%s}%s"%(self.basetype.targetNamespace,
                               self.basetype.name)
    else:
      bt=""
    c = " contentType "+self.contentType;
    if (self.contentType in ('elementOnly','mixed')) and self.model:
      model="%s: %s"%(self.model.term.compositor,''.join(map(str,self.model.term.particles)))
    elif self.contentType=='textOnly' and self.basetype:
      model="{%s}%s"%(self.basetype.targetNamespace,
                      self.basetype.name)
    else:
      model=""
    if self.attributeDeclarations:
      attrs=''.join(map(str,self.attributeDeclarations.values()))
    else:
      attrs=""
    return "{Complex type %s%s%s:%s%s}"%(self.name,bt,c,model,attrs)

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def __getattr__(self,name):
    if name=='basetype':
      return Type.__getattr__(self,name)
    # the next _two_ properties taken together make the REC's {content type}
    elif name=='derivationMethod':
      self.derivationMethod=self.xrpr.derivedBy
      return self.derivationMethod
    elif name=='contentType':
      # textOnly iff simpleContent
      mm=0
      if (self.xrpr.simpleContent is not None or
          self.xrpr.complexContent is not None):
        if self.xrpr.simpleContent is not None:
          self.contentType='textOnly'
          if self.xrpr.mixed=='true':
            self.error("mixed='true' is ignored with simpleContent",1)
        elif self.xrpr.complexContent is not None:
          if (self.basetype is not None and
              self.basetype.contentType=='textOnly'):
            self.error("attempt to derive a complex basetype from a simple base: %s"%self.basetype.name)
            self.contentType='textOnly'
          else:
            # temporary
            self.contentType='elementOnly'
          if self.xrpr.complexContent.mixed=='true':
            mm=1
            # note if basetype is not mixed that's an error
          elif self.xrpr.complexContent.mixed=='unspecified' and self.xrpr.mixed=='true':
            mm=1
            # ditto
        if self.contentType=='elementOnly':
          if self.derivationMethod=='restriction':
            if mm:
              self.contentType='mixed'
            elif self.xrpr.model is None:
              # TODO: check for defective cases which -> empty per the REC
              self.contentType='empty'
            else:
              self.contentType='elementOnly'
          else:
            # extension
            if (self.xrpr.model is None and
                not mm and
                self.basetype is not None):
              self.contentType=self.basetype.contentType
            elif mm:
              self.contentType='mixed'
      else:
        # restriction of urType
        if self.xrpr.mixed=='true':
          self.contentType='mixed'
        elif self.xrpr.model is None:
          # TODO: check for defective cases which -> empty per the REC
          self.contentType='empty'
        else:
          self.contentType='elementOnly'
      if (self.derivationMethod=='extension' and self.basetype is not None and
          self.basetype.contentType!='empty' and
           (self.contentType=='mixed')!=(self.basetype.contentType=='mixed')):
        self.error("attempt to extend a mixed basetype into an unmixed type or vice versa (%s, %s)"%(self.name,self.basetype.name))
        self.model=Type.urType.model          # protect against later crash
        self.contentType='mixed'
      if (self.derivationMethod=='restriction' and
          self.basetype is not None):
        st=self.basetype
        if ((mm or self.contentType=='mixed') and st.contentType!='mixed'):
          self.error("attempt to restrict a non-mixed basetype into an mixed type")
        if (self.contentType!='mixed' and st.contentType=="mixed" and
            not st.emptiable()):
          self.error("attempt to restrict a non-emptiable mixed basetype into an non-mixed type")
      return self.contentType
    elif name=='model':
      if self.contentType=='textOnly':
        if (self.xrpr.simpleContent is not None and
            self.xrpr.simpleContent.restriction is not None):
          restr = self.xrpr.simpleContent.restriction
          if restr.__dict__.has_key('simpleType'):
            # nested simpleType, use it as base
            # TODO: will ignore higher-level facets???
            if len(restr.facets)>0:
              self.xrpr.simpleContent.final="" # desperate fixup hack
              self.model=SimpleType(self.sschema,
                                    self.xrpr.simpleContent,
                                    'restriction',None,
                                    restr.component)
            else:
              # can skip a level and just use the nested simple type
              self.model=restr.simpleType.component
          else:
            # no nested simpleType, shared basetypeName better do it
            # todo: error if base not complex
            fake=simpleTypeElt(self.sschema,self.xrpr.elt)
            fake.name=None
            fake.restriction=self.xrpr.simpleContent.restriction
            fake.init(self.xrpr.elt)
            fake.component.basetypeName=self.basetypeName # for chameleons
            self.model=fake.component
          self.model.withinComplex=1
        elif self.basetype is not None:
          self.model=self.basetype.simple()
        else:
          self.model=Type.urSimpleType
      else:
        self.model=self.realModel(self.xrpr.model)
      return self.model
    elif name=='attributeDeclarations':
      # a dictionary of attributeUse instances keyed by qname
      self.attributeDeclarations=self.mergeAttrs(self.basetype,self.derivationMethod)
      return self.attributeDeclarations
    elif name=='fsm':
      if (self.model is None or
          self.contentType not in ("elementOnly","mixed")):
	self.fsm = None
	return self.fsm
      (self.fsm,nd)=UniqueFSM(self.model)
      if nd:
        self.error("non-deterministic content model for type %s: %s" %
                   (self.name, nd))
        self.fsm = self.fsm.determinise()
      elif (self.derivationMethod=='restriction' and
            self.basetype is not None and
            self.basetype is not Type.urType):
        if not self.basetype.fsm:
          self.error("Restriction of empty model (of %s) with non-empty model (of %s) not allowed"%(self.basetype.name or "[Anonymous]",self.name or "[Anonymous]"))
          return self.fsm
        res=self.fsm.subsumed(self.basetype.fsm)
        if res is not None:
          self.fsm.subsumptionError(self,self.basetype.fsm,res,"type",
                                    self.name,self.basetype.name,xsvNS)
      return self.fsm
    else:
      raise AttributeError,name

  def rebuild(self):
    global currentCTC
    Component.rebuild(self)
    Type.currentCTC=self.saveCTC

  def simple(self):
    return self.model                # assumes textonly content

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=(self.basetype is not None) and self.basetype.prepare()
    p2=(self.model is not None) and self.model.prepare()
    p3=self.attributeDeclarations
    if p3:
      p4 = 1
      for au in p3.values():
        p4=au.prepare() and p4
    p5=self.fsm
    return (p1 and p2 and p3 and p5)

  def checkBase(self,derived):
    return derived.checkComplexBase(self)

  def checkSimpleBase(self,st):
    if self.xrpr.simpleContent is None:
      # can't use contentType w/o an infinite loop of lazy interaction between
      # contentType and basetype
      self.error("type %s with simple basetype %s may not have complex content"%(self.name or '[anonymous]',st.name))
      return
    if self.derivationMethod=='restriction':
      self.error('derivation of complex type by restriction of simple type not allowed')
      return
    else:
      return st

  def checkComplexBase(self,st):
    if (self.xrpr.simpleContent is not None and not
        (st.contentType=="textOnly" or
         (self.derivationMethod=='restriction' and
          st.contentType=="mixed" and st.emptiable()))):
      self.error("type %s with simple content must have simple or emptiable mixed basetype %s:%s"%(self.name,st.name,st.contentType))
      return
    if self.derivationMethod in st.final:
      self.error("Error, %s declares %s as base, which is final"%(self.name,
                                                             st.name))
      return
    else:
      return st

  def realModel(self,raw):
    # XXX doesn't deal with all groups yet
    # deals with derivation simple cases only
    if self.basetype is not None:
      other=self.basetype.model
    else:
      # error already
      other=None
    if raw is not None:
      mine=_topGroup(self.sschema,raw)
    elif self.derivationMethod=='restriction' or other is None:
      mine=Particle(self.sschema,None,
                    Sequence(self.sschema,None,self.xrpr))
      mine.occurs=(1,1)
      mine.particles=[]
    else:
      return other
    if self.derivationMethod=='restriction':
      if (other is None) or self.basetype is Type.urType or other is Type.urType.model:
        return mine
      else:
        res=mine.merge(other)
        if res is not None:
          return res
        else:
          if self.contentType=='elementOnly':
            self.contentType='empty'
          return None
    elif ((self.basetype is None) or self.basetype.contentType=='empty'):
      return mine
    else:
      if (self.basetype.contentType=='textOnly' and
          (self.contentType!='textOnly' or raw is not other)):
        # TODO: I no longer understand what the 'raw is not other' clause is
        self.error("extension of simple content %s may not have content model"%other)
        return mine

      # needs more checks for allowed extension. . .
      if (isinstance(other,Particle) and
          (other.term is not None) and
          other.term.compositor=='sequence' and other.occurs==(1,1)):
        newp=copy.copy(other)
        newp.term=copy.copy(other.term)
        newp.term.particles=other.term.particles+[mine]
        return newp
      else:
        np=Particle(self.sschema,None,
                    Sequence(self.sschema,None,mine.xrpr),mine.xrpr)
        np.occurs=(1,1)
        np.term.particles=[other,mine]
        return np

  def guessBase(self):
    # called to supply base type when we don't have one explicitly
    if self.xrpr is not None and self.xrpr.simpleContent is not None:
      return Type.urSimpleType
    else:
      return Type.urType

  def mergeAttrs(self,basetype,derivedBy):
    mine=self.expandAttrGroups()
    if basetype is not None:
      others=basetype.attributeDeclarations
    else:
      others={}
    for (adn,ad) in others.items():
      if adn=='#any':
        if derivedBy=='extension':
          if mine.has_key(adn):
            mine[adn].attributeDeclaration=ad.attributeDeclaration.intersect(mine[adn].attributeDeclaration)
          else:
            mine[adn]=ad
        else:
          # restriction
          pass                          # not inherited
      elif mine.has_key(adn):
        if derivedBy=='extension':
          self.error("attempt to extend with an attribute already declared {%s}"%adn)
        else:
          # restriction
          me=mine[adn]
          if me.maxOccurs==0:
            if ad.minOccurs==1:
              self.error("attempt to eliminate required attribute %s"%me.qname)
            else:
              del mine[adn]
          else:
            if ad.minOccurs==1:
              if me.minOccurs==0:
                self.error("attempt to make required attribute %s optional"%me.qname)
                me.minOccurs=1
            if ad.valueConstraint is not None:
              if (ad.valueConstraint[0]=='fixed' and
                  ((me.valueConstraint is None) or
                   me.valueConstraint[0]!='fixed' or
                   me.valueConstraint[1]!=ad.valueConstraint[1])):
                self.error("attempt to change or abandon fixed value for attribute %s"%me.qname)
            me.attributeDeclaration.checkSubtype(ad.attributeDeclaration)
      else:
        mine[adn]=ad
    return mine

  def expandAttrGroups(self):
    tab={}
    for ad in self.xrpr.attrs:
      ad.component.expand(tab)
    return tab

  def note(self,table):
    self.term.note(table)

  def emptiable(self):
    # TODO: should do some real work . . .
    return (self is Type.urType or
            isinstance(self.model,SimpleType) or      # !!might be wrong!!
            self.model.occurs[0]==0 or
            (len(filter(lambda p:p.occurs[0]==0,self.model.term.particles))==
             len(self.model.term.particles)))

  def attributeUseRebuild(self,val):
    if not self.__dict__.has_key('attributeDeclarations'):
      self.attributeDeclarations={}
    if val is None:
      return
    for au in val:
      self.attributeDeclarations[QName('',
                                  au.attributeDeclaration.name,
                                  au.attributeDeclaration.targetNamespace)]=au

  def attributeWildcardRebuild(self,val):
    if val is not None:
      if not self.__dict__.has_key('attributeDeclarations'):
        self.attributeDeclarations={}
      awu=AttributeUse(self.sschema,
                       None,
                       val)
      awu.minOccurs=0
      self.attributeDeclarations['#any']=awu

  def contentTypeRebuild(self,val):
    self.contentType=val.variety
    self.model=val.model

  def isSubtype(self,other,avoid=None):
    #print ('ist',self.name,other.name,avoid)
    if 'extension' in avoid and 'restriction' in avoid:
      return 0
    if self is other:
      return 1
    if self.basetype is self or self.basetype is None:
      return 0
    if avoid is not None and self.derivationMethod in avoid:
      return 0
    else:
      return self.basetype.isSubtype(other,avoid)

def _topGroup(sschema,rawModel):
  if ((rawModel.component is not None) and
      isinstance(rawModel.component.term,Group)):
    # we have exactly one group, so use it
    return rawModel.component
  else:
    # earlier schema error, signalled I hope
    return None


# $Log: ComplexType.py,v $
# Revision 1.37  2007-02-16 15:30:12  ht
# check block wrt subst groups better
#
# Revision 1.36  2006/11/03 16:51:37  ht
# block 0-length derivation if both routes blocked
#
# Revision 1.35  2006/08/15 16:11:21  ht
# use xsvNS for dumping FSMs
#
# Revision 1.34  2006/04/21 10:36:18  ht
# improve final and block support
#
# Revision 1.33  2005/10/10 14:07:40  ht
# handle anonymous base inside simple content properly
#
# Revision 1.32  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.31  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.30  2004/08/18 08:43:36  ht
# allow empty->mixed or empty->elt-only extension
#
# Revision 1.29  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.28  2004/02/04 10:42:25  ht
# Argh -- roll out E1-17 'fix'
#
# Revision 1.27  2004/01/31 14:41:52  ht
# warn == error(. . . ,1)
#
# Revision 1.26  2004/01/31 11:46:19  ht
# try again to get mixed derivation errors right
#
# Revision 1.25  2003/12/04 10:51:25  ht
# move subsumption error messages to FSM;
# implement E1-17, test subType by name only
#
# Revision 1.24  2003/07/09 13:48:12  ht
# grr yet again contentType
#
# Revision 1.23  2003/07/09 13:06:49  ht
# finally get contentType stuff OK with regrtest
#
# Revision 1.22  2003/07/09 12:50:14  ht
# make mixed above simpleContent a warning
#
# Revision 1.21  2003/07/09 12:46:19  ht
# still fussing with mixed/textOnly/etc
#
# Revision 1.20  2003/07/09 11:04:45  ht
# again
#
# Revision 1.19  2003/07/09 11:01:47  ht
# fix over eager fix
#
# Revision 1.18  2003/07/09 10:38:11  ht
# another cya patch
#
# Revision 1.17  2003/07/09 10:26:03  ht
# cover for some post-error processing bugs
#
# Revision 1.16  2003/06/30 18:58:58  ht
# no facets if no base
#
# Revision 1.15  2003/06/11 11:56:03  ht
# check mixed derivations better
#
# Revision 1.14  2003/06/11 11:54:24  ht
# no more fake component for simple content by extension (why was there ever -- worry)
#
# Revision 1.13  2003/04/01 18:50:33  ht
# catch a complex-from-simple derivation bug
#
# Revision 1.12  2003/02/20 14:44:52  ht
# fix two minor bugs to do with derivation by extension
#
# Revision 1.11  2003/01/20 12:25:06  ht
# improved robustness wrt earlier errors
#
# Revision 1.10  2002/12/03 10:32:33  ht
# typo
#
# Revision 1.9  2002/12/01 21:54:58  ht
# add and inherit idt (identity constraint type) to type defs
#
# Revision 1.8  2002/11/29 21:11:48  ht
# rework contentType computation to make it lazy,
# fixing bogus extentsion of simpleContent case,
# check for mix/nomix extension cases
#
# Revision 1.7  2002/11/25 14:53:08  ht
# involve vcv in preparation
#
# Revision 1.6  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.5  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.4  2002/11/05 14:18:22  ht
# package FSM construction and checking and move to FSM
#
# Revision 1.3  2002/11/01 17:07:49  ht
# fail more gracefully in absence of base type
#
# Revision 1.2  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
