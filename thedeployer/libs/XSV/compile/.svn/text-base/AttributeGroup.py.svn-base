"""Schema compilation: AttributeGroup component"""

__version__="$Revision: 1.7 $"
# $Id: AttributeGroup.py,v 1.7 2005-04-22 13:54:20 ht Exp $

from Component import Component

from SchemaError import shouldnt
from AttributeUse import AttributeUse
from QName import QName

attributeGroupElt=None                           # imported by init()
Attribute=None                           # imported by init()

class AttributeGroup(Component):
  # TODO: check wildcard intersection during expansion
  base=None
  dummy=None                            # only relevant when doing a rel refl
  foundWhere='attributeGroupTable'

  def __unicode__(self):
    return "{AttrGroup %s}"%self.name

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def __getattr__(self,name):
    if name=='attributeDeclarations':
      tab={}
      for xa in self.xrpr.attrs:
        if xa.component.maxOccurs!=0:
          xa.component.expand(tab)
      if self.base is not None:
        # we were redefined wrt self.base, check restriction
        for ad in self.base.attributeDeclarations:
          if tab.has_key(ad.qname):
            me=tab[ad.qname]
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
          elif ad.minOccurs==1:
            self.error("attempt to eliminate required attribute %s"%ad.qname)
      self.attributeDeclarations=tab.values()
      return self.attributeDeclarations
    else:
      raise AttributeError,name

  def attributeUseRebuild(self,val):
    if self.__dict__.has_key('attributeDeclarations'):
      shouldnt('xyzzy')
    self.attributeDeclarations=val

  def attributeWildcardRebuild(self,val):
    if val is not None:
      mv=AttributeUse(self.sschema,None,val)
      if self.attributeDeclarations is None:
        self.attributeDeclarations=[mv]
      else:
        self.attributeDeclarations.append(mv)

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=(self.attributeDeclarations is not None)
    if p1:
      p2=1
      for au in self.attributeDeclarations:
        ad=au.attributeDeclaration
        if isinstance(ad,Attribute):
          p2=ad.prepare() and p2
    return p1 and p2

  def expand(self,table):
    for au in self.attributeDeclarations:
      au.expand(table)

  def redefine(self):
    # we have a component which should be based on itself
    # note this forces some reference resolution normally left until later
    if not self.schema.attributeGroupTable.has_key(self.name):
      self.error("attempt to redefine in terms of non-existent attribute group: %s"%self.name)
      return
    else:
      redefed=self.schema.attributeGroupTable[self.name]
    qn=QName(None,self.name,self.schema.targetNS)
    selfRefs=self.findSelfRefs(qn)
    if len(selfRefs)>1:
      self.error("more than one self-reference not allowed in attribute group redefinition")
    else:
      redefed.name="%d %s"%(redefed.id,self.name)
      self.schema.attributeGroupTable[redefed.name]=redefed
      self.schema.attributeGroupTable[self.name]=self
      self.qname=qn
      if len(selfRefs)==0:
        # must be a restriction -- postpone the real work
        self.base=redefed
      elif len(selfRefs)==1:
        # an extension, just use it, duplicates will be detected later
        selfRefs[0].component.attributeDeclarationName=QName(None,redefed.name,
                                                             self.schema.targetNS)

  def findSelfRefs(self,qn):
    return filter(lambda d,qn=qn:(isinstance(d,attributeGroupElt) and
                                  d.component.qname==qn),
                  self.xrpr.attrs)


def init():
  # cut import loops
  global Attribute, attributeGroupElt
  from Attribute import Attribute
  from elts.attributeGroupElt import attributeGroupElt

# $Log: AttributeGroup.py,v $
# Revision 1.7  2005-04-22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.6  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.5  2005/04/14 13:23:39  ht
# fix redef name bug
#
# Revision 1.4  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.3  2002/11/05 14:17:33  ht
# fix dbl redefine name bug
#
# Revision 1.2  2002/09/02 16:09:24  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
