"""Schema compilation: KCons component"""

__version__="$Revision: 1.1 $"
# $Id: KCons.py,v 1.1 2002-06-28 09:40:22 ht Exp $

import types

from Component import Component
from QName import QName

from XSV.util.xpath import XPath

from elts.commonElt import commonElt

class Kcons(Component):
  def __init__(self,sschema,xrpr):
    Component.__init__(self,sschema,xrpr)
    if xrpr is not None:
      self.fields=map(lambda x:XPath(x.xpath,x.elt.namespaceDict),
                      xrpr.fields)
      self.selector=XPath(xrpr.selector.xpath,
                                xrpr.selector.elt.namespaceDict)
      self.register('identity constraint', self.schema.keyUniqueTable)

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1

  def selectorRebuild(self,val):
    self.selector=XPath(val.path,self.sschema.sfors.nsdict)

  def fieldsRebuild(self,val):
    if type(val)is types.ListType:
      self.fields=map(lambda xpi,nsd=self.sschema.sfors.nsdict:XPath(xpi.path,
                                                                      nsd),
                 val)
    else:
      self.fields=[XPath(val.path,self.sschema.sfors.nsdict)]

# could these all be double-rooted??
class Unique(Kcons):
  refer=None
  cname='unique'

class Keyref(Kcons):
  cname='keyref'
  def __init__(self,sschema,xrpr):
    Kcons.__init__(self,sschema,xrpr)
    self.referName=QName(xrpr.refer,xrpr.elt,sschema)

  def __getattr__(self,name):
    if name=='refer':
      self.refer=None
      if self.schema.vKeyUniqueTable.has_key(self.referName):
        self.refer=self.schema.vKeyUniqueTable[self.referName]
      else:
        self.error("Undefined key/unique %s referenced from {%s}%s"%(self.referName,
                                                                     self.targetNamespace,
                                                                     self.name))
      return self.refer
    else:
      raise AttributeError,name
    
  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    return (self.refer is not None)

class Key(Kcons):
  refer=None
  cname='key'


# $Log: KCons.py,v $
# Revision 1.1  2002-06-28 09:40:22  ht
# XSV as package: components
#
