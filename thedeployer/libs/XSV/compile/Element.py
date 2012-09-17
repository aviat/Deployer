"""Schema compilation: Element component"""

__version__="$Revision: 1.16 $"
# $Id: Element.py,v 1.16 2007-02-16 15:49:10 ht Exp $

import types

from Component import Component
from QName import QName
from KCons import Key, Keyref, Unique
from Type import Type

from SchemaError import shouldnt

groupElt=None                           # imported by init()

class Element(Component):
  typeDefinitionName=None
  equivClassName=None
  valueConstraint=None                  # TODO: implement this! (and in aps)
  foundWhere='elementTable'
  def __init__(self,sschema,xrpr=None,scope=None):
    if (type(scope) is types.StringType or (xrpr and xrpr.form=='qualified')):
      ns='ns'
    else:
      ns=None
    Component.__init__(self,sschema,xrpr,ns)
    if xrpr is not None:
      if type(scope) is types.StringType:
        self.scope=scope
      else:
        self.scopeRepr=scope              # an xrpr, component not available yet
      self.abstract=xrpr.abstract or 'false'
      self.nullable=xrpr.nullable or 'false'
      if xrpr.substitutionGroup is not None:
        self.equivClassName = QName(xrpr.substitutionGroup,xrpr.elt,
                                    sschema)
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
        self.prohibitedSubstitutions=('restriction','extension','substitution')
      if xrpr.type is not None:
        self.typeDefinitionName=QName(xrpr.type,xrpr.elt,
                                      sschema)
        if xrpr.simpleType or xrpr.complexType:
          self.error("declaration with 'type' attribute must not have nested type declaration")
      elif xrpr.simpleType is not None:
        self.typeDefinition=xrpr.simpleType.component
      elif xrpr.complexType is not None:
        self.typeDefinition=xrpr.complexType.component
      elif not self.equivClassName:
        self.typeDefinition=Type.urType
      if xrpr.fixed is not None:
        # todo: check vc against type
        self.valueConstraint=('fixed',xrpr.fixed)
      elif xrpr.default is not None:
        self.valueConstraint=('default',xrpr.default)
      self.keys=map(lambda e:e.component,xrpr.keys)
      self.keyrefs=map(lambda e:e.component,xrpr.keyrefs)
      self.uniques=map(lambda e:e.component,xrpr.uniques)
    else:
      self.keys=[]
      self.uniques=[]
      self.keyrefs=[]

  def __hash__(self):
    return hash(self.name)

  def __coerce__(self,other):
    return None
  
  def __unicode__(self):
    if (self.typeDefinition is not None and self.typeDefinition.name and
        self.typeDefinition.name[0]!='['):
      return "{Element {%s}%s:%s}"%(self.targetNamespace,self.name,
                                self.typeDefinition.name)
    else:
      return "{Element {%s}%s:%s}"%(self.targetNamespace,self.name,
                                unicode(self.typeDefinition))

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def __getattr__(self,name):
    if name=='equivalenceClassAffiliation':
      self.equivalenceClassAffiliation=None
      if self.equivClassName:
        #print ('eq',self.name,self.equivClassName)
        if self.schema.vElementTable.has_key(self.equivClassName):
          self.equivalenceClassAffiliation=exemplar=self.schema.vElementTable[self.equivClassName]
          if (self.typeDefinition is not None and
              exemplar.typeDefinition is not None):
            if not self.typeDefinition.isSubtype(exemplar.typeDefinition,()):
                self.error("type {%s}%s not subtype of type {%s}%s of exemplar %s"%(self.typeDefinition.targetNamespace,self.typeDefinition.name, exemplar.typeDefinition.targetNamespace,exemplar.typeDefinition.name, exemplar.qname))
        else:
          self.error("Undefined element %s referenced as equivalence class affiliation"%self.equivClassName)
      return self.equivalenceClassAffiliation
    elif name=='equivClass':
      # first access propagates everything
      if type(self.scope) is not types.StringType:
        shouldnt('not global %s'%self.name)
      for schema in self.sschema.schemas.values():
        for ed in schema.elementTable.values():
          if not ed.__dict__.has_key('equivClass'):
            ed.equivClass=[]
          if (ed.abstract!='true' and
              ed.equivalenceClassAffiliation is not None):
            ed.equivalenceClassAffiliation.addECM(ed)
      return self.equivClass
    elif name=='typeDefinition':
      self.typeDefinition=None
      if self.typeDefinitionName:
        if self.schema.vTypeTable.has_key(self.typeDefinitionName):
          self.typeDefinition=self.schema.vTypeTable[self.typeDefinitionName]
        else:
          self.error("Undefined type %s referenced as type definition of %s"%(self.typeDefinitionName, self.name))
      elif self.equivClassName:
        if self.equivalenceClassAffiliation is not None:
          self.typeDefinition=self.equivalenceClassAffiliation.typeDefinition
      else:
        shouldnt('etd')
      return self.typeDefinition
    elif name=='scope':
      if isinstance(self.scopeRepr,groupElt):
        self.scope=None
      else:
        self.scope=self.scopeRepr.component
      return self.scope
    elif name=='qname':
      # top-level get them at build time, locals may need them
      self.qname=QName(None,self.name,self.targetNamespace)
      return self.qname
    elif name=='vcv':
      # value constraint value
      return self.doVcv(self.typeDefinition)
    else:
      raise AttributeError,name

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p5=(self.scope is not None)
    if type(self.scope) is types.StringType:
      p1=(self.equivalenceClassAffiliation is not None)
      p2=(self.equivClass is not None)
    else:
      p1=p2=1
    p3=(self.typeDefinition is not None) and self.typeDefinition.prepare()
    p4=self.keys or self.keyrefs or self.uniques
    if p4:
      p6=1
      for i in self.keys:
        ip=i.prepare()
        p6=p6 and ip
      for i in self.keyrefs:
        ip=i.prepare()
        p6=p6 and ip
      for i in self.uniques:
        ip=i.prepare()
        p6=p6 and ip
    else:
      p4=p6=1
    p7=(self.valueConstraint is not None) and (self.vcv is not None)
    return (p1 and p2 and p3 and p4 and p5 and p6 and p7)

  def addECM(self,member):
    if member is self:
        self.error("circular substitution group");
        return
    if not self.__dict__.has_key('equivClass'):
      self.equivClass=[member]
    else:
      if member in self.equivClass:
        # 2nd time around, either prior loop or late-arriving schema
        return
      ef = self.prohibitedSubstitutions
      tf = self.typeDefinition.prohibitedSubstitutions
      if ef is not () or tf is not ():
        ef = list(ef)+list(tf)
      if not member.typeDefinition.isSubtype(self.typeDefinition,ef):
        self.error("type {%s}%s not substitutable for type {%s}%s of substitution group head %s"%(member.typeDefinition.targetNamespace,member.typeDefinition.name, self.typeDefinition.targetNamespace,self.typeDefinition.name, self.qname),True)
      else:
        self.equivClass.append(member)
    if self.equivalenceClassAffiliation is not None:
      self.equivalenceClassAffiliation.addECM(member)

  def note(self,table):
    shouldnt('notee')
    if table.has_key(self.qname):
      if self.typeDefinition  is not  table[self.qname].typeDefinition:
	self.error("illegal redeclaration of %s" % self.qname)
      elif not (type(self.scope) is types.StringType and
                type(table[self.qname].scope) is types.StringType):
	self.error("redeclaration of %s ok - same type\n" % self.qname,1)
      return
    table[self.qname] = self
    if (type(self.scope) is types.StringType and
        'substitution' not in self.prohibitedSubstitutions):
      # check for equivalence classes
      # is this necessary -- it's quite expensive
      for decl in self.equivClass:
	table[decl.qname]=decl

  def merge(self,other):
    # not called anymore
    shouldnt('merge2')
    # TODO: check default/fixed -- what else?
    if self.name!=other.name or self.targetNamespace!=other.targetNamespace:
      self.error("declaration in a restriction not same name as declaration it corresponds to: {%s}%s vs. {%s}%s"%(self.targetNamespace,self.name,other.targetNamespace,other.name))
    if (self.typeDefinition is not None and
        other.typeDefinition is not None and
        not self.typeDefinition.isSubtype(other.typeDefinition,['extension']+other.typeDefinition.final)):
      self.error("type {%s}%s not subtype of type {%s}%s of {%s}%s in restriction"%(self.typeDefinition.targetNamespace,self.typeDefinition.name, other.typeDefinition.targetNamespace,other.typeDefinition.name, self.targetNamespace, self.name))
    return self

  def keyRebuild(self,val):
    if val is not None:
      for ic in val:
        if isinstance(ic,Key):
          self.keys.append(ic)
        elif isinstance(ic,Keyref):
          self.keyrefs.append(ic)
        elif isinstance(ic,Unique):
          self.uniques.append(ic)
        else:
          shouldnt('bogusic: %s'%ic)

def init():
  # cut import loop
  global groupElt
  from elts.groupElt import groupElt

# $Log: Element.py,v $
# Revision 1.16  2007-02-16 15:49:10  ht
# only warn about blocked subst
#
# Revision 1.15  2007/02/16 15:30:12  ht
# check block wrt subst groups better
#
# Revision 1.14  2006/11/03 16:55:37  ht
# some subst dissallowed/excluded hacking
#
# Revision 1.13  2006/04/21 11:02:50  ht
# accommodate change to final handling
#
# Revision 1.12  2005/06/08 16:14:47  ht
# fix circular subst groups properly
#
# Revision 1.11  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.10  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.9  2005/04/14 13:55:30  ht
# protect against missing head
#
# Revision 1.8  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.7  2003/06/06 17:02:39  ht
# break circular subst groups
#
# Revision 1.6  2002/11/25 14:53:08  ht
# involve vcv in preparation
#
# Revision 1.5  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.4  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.3  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:09:25  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
