"""Schema compilation: SimpleType component"""

__version__="$Revision: 1.23 $"
# $Id: SimpleType.py,v 1.23 2007-02-16 14:22:33 ht Exp $

import types

from Type import Type
from SimType import SimType
from ListFacet import ListFacet
from NumFacet import NumFacet
from QName import QName
from Facet import Whitespace

from XSV.compile import simpleTypeMap

class SimpleType(Type,SimType):
  isSimple=1
  withinComplex=None
  basetypeName=None
  attributeDeclarations={}              # for use when this is a ct's basetype
  contentType='textOnly'                # ditto
  elementTable={}                       # ditto

  def __init__(self,sschema,xrpr,derivedBy=None,
               basetypeName=None,subComponent=None):
    Type.__init__(self,sschema,xrpr)
    self.basetypeName=basetypeName
    if xrpr is not None:
      if xrpr.final=='':
        self.final=()
      else:
        self.final=xrpr.final.split()
      if '#all' in self.final:
        self.final=('restriction','extension','list','union')
    self.subComp=subComponent
    if subComponent is not None:
      subComponent.super=self
      if hasattr(subComponent,'basetype'):
        self.basetype=subComponent.basetype
    self.derivedBy=derivedBy

  def __unicode__(self):
    if (self.basetype is not None) and self.basetype is not self:
      if isinstance(self.basetype,QName):
	bt=" based on %s"%self.basetype
      else:
	bt=" based on %s"%self.basetype.name
    else:
      bt=""
    v='???'
    return "{Simple %s type {%s}%s%s}"%(v,self.targetNamespace,
                                            self.name,bt)

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def __getattr__(self,name):
    if name=='basetype':
      if (Type.__getattr__(self,name) is Type.urSimpleType and
          self.variety=='atomic'):
        # not allowed for simple types!
        self.error("Must have basetype for atomic simpleType %s"%(self.name or '[anonymous]'))
        self.basetype=None
      return self.basetype
    elif name=='variety':
      # lazy because it involves the real basetype
      if self.derivedBy=='restriction':
        self.variety=self.subComp.variety or 'atomic' # in case of error
      else:
        self.variety=self.derivedBy or 'atomic' # in case of error
      return self.variety
    elif name=='reflectedName':
      self.reflectedName=self.variety
      return self.reflectedName
    elif name=='reflectionOutMap':
      self.reflectionOutMap=simpleTypeMap[self.variety].reflectionOutMap
      return self.reflectionOutMap
    elif name=='idt':
      if self.basetype is None:
        self.idt=0
      else:
        self.idt=self.basetype.idt
      return self.idt
    elif name=='validateTextSub':
      if self.variety=='atomic':
        self.validateTextSub=self.validateTextAtomic
      elif self.variety=='list':
        self.validateTextSub=self.validateTextList
      elif self.variety=='union':
        self.validateTextSub=self.validateTextUnion
      else:
        shouldnt("variety: %s"%self.variety)
      return self.validateTextSub
    elif name not in ('rootName','primitiveType','convertToActualValue',
                      'memberTypes','itemType','restrict','facets'):
      raise AttributeError,name
    elif self.subComp is not None:
      return getattr(self.subComp,name)
    else:
      # should be e.g. itemType on vanilla simple type from rebuild
      setattr(self,name,None)
      return None

  def simple(self):
    return self

  def guessBase(self):
    # called to supply base type when we don't have one explicitly
    return Type.urSimpleType

  def hasMember(self,other):
    if self.variety!='union':
      return 0
    else:
      for mtd in self.memberTypes:
        if (other==mtd or
            (mtd.basetype==other and
             ((not mtd.facets) or
              (len(mtd.facets)==1 and
               'whiteSpace' in mtd.facets)))):
          # this isn't quite right . . .
          return 1
      return 0

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=(self.basetype is not None) and self.basetype.prepare()
    p2=self.variety is not None
    p3=1
    if self.facets is not None:
      for f in self.facets.values():
        p3=f.prepare() and p3
    p4 = (self.subComp is not None) and self.subComp.prepare()
    return p1 and p2 and p3

  def emptiable(self):
    # should do some real work . . .
    return self is Type.urType

  def facetRebuild(self,val):
    # val should be list of facet instances
    self.facets={}
    if val is not None:
      if self.variety=='atomic':
        ft=self.primitiveType
      else: # self.variety=='list' or self.variety=='union':
        ft=self
      for f in val:
        if isinstance(f,ListFacet):
          # list values not decoded?
          if self.facets.has_key(f.name):
            self.facets[f.name].stringValue.append(f.value)
            del f.value
            continue
          else:
            f.stringValue=[f.value]
        else:
          f.stringValue=f.value
        f.type=ft
        del f.value
        self.facets[f.name]=f

  def fundamentalFacetRebuild(self,val):
    return

  def uvarietyRebuild(self,val):
    self.variety='union'

  def lvarietyRebuild(self,val):
    self.variety='list'

  def varietyReflect(self,x):
    pass

  def isSubtype(self,other,avoid=None):
    if self is other:
      return 1
    if 'restriction' in avoid:
      return 0
    if self.basetype is self or self.basetype is None:
      return 0
    if (other is Type.urSimpleType or
        other is Type.urType or
        (isinstance(other,SimpleType) and
         other.variety=='union' and
         ((avoid is None) or ('union' not in avoid)) and
         (self in other.memberTypes))):
      return 1
    return self.basetype.isSubtype(other,avoid)



# $Log: SimpleType.py,v $
# Revision 1.23  2007-02-16 14:22:33  ht
# remove redundant init
#
# Revision 1.22  2007/02/16 14:10:09  ht
# enforce block in subtype checking
#
# Revision 1.21  2006/11/03 17:12:31  ht
# cover gaps wrt prohibitedSubst
#
# Revision 1.20  2006/04/21 10:36:18  ht
# improve final and block support
#
# Revision 1.19  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.18  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.17  2004/10/21 14:23:46  ht
# bullet-proofing
#
# Revision 1.16  2004/08/18 08:26:50  ht
# roll back E1-17 "fix" :-(
#
# Revision 1.15  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.14  2003/12/04 10:56:16  ht
# implement E1-17, test subType by name only
#
# Revision 1.13  2003/07/09 10:26:30  ht
# cover for some post-error processing bugs,
# prepare subComp (list or union)
#
# Revision 1.12  2003/06/06 17:02:23  ht
# fix element default vs mixed bug
#
# Revision 1.11  2002/12/03 10:34:47  ht
# catch no-basetype case wrt idt inheritance
#
# Revision 1.10  2002/12/03 10:33:34  ht
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
# Revision 1.7  2002/11/25 14:56:34  ht
# fix rebuilding of Enumerations to compute value
#
# Revision 1.6  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.5  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.4  2002/09/23 21:35:43  ht
# move to string methods from string library
#
# Revision 1.3  2002/09/23 14:00:55  ht
# pick up pattern sharing hack
#
# Revision 1.2  2002/07/24 08:14:46  ht
# fix inheritance chain for derived builtins
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
