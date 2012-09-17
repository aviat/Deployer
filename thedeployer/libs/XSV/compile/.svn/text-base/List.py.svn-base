"""Schema compilation: List component"""

__version__="$Revision: 1.4 $"
# $Id: List.py,v 1.4 2004-12-09 11:02:00 ht Exp $

from Component import Component
from QName import QName
from Facet import Whitespace
from Type import Type

from SchemaError import shouldnt

class List(Component):
  variety='list'
  primitiveType=None
  memberTypes=None
  itemtypeName=None
  allowedFacets=['length', 'minLength', 'maxLength',
                 'pattern', 'enumeration','whiteSpace']
  facets={}
  def __init__(self,sschema,xrpr):
    Component.__init__(self,sschema,xrpr)
    if xrpr.itemType:
      self.itemtypeName=QName(xrpr.itemType,xrpr.elt,sschema)
      if xrpr.simpleType is not None:
        self.error("list with 'type' attribute must not have nested type declaration")
    elif xrpr.simpleType is not None:
      self.itemType=xrpr.simpleType.component
    else:
      # no elt means builtin
      if xrpr.elt is not None:
        self.error("list must have 'type' attribute or SimpleType child")

  def __getattr__(self,name):
    if name=='itemType':
      self.itemType=None
      if self.itemtypeName:
        if self.schema.vTypeTable.has_key(self.itemtypeName):
          self.itemType=self.schema.vTypeTable[self.itemtypeName]
        else:
          self.error("Undefined type %s referenced as type definition of %s"%(self.itemtypeName, self.super.name))
          self.itemType=Type.urSimpleType # prevent later crash
      else:
        self.itemType=Type.urSimpleType
      return self.itemType
    else:
      raise AttributeError,name

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    return self.itemType.prepare()

def init():
  wf=Whitespace(None,None)
  wf.value='collapse'
  wf.fixed=1
  List.facets['whiteSpace']=wf

# $Log: List.py,v $
# Revision 1.4  2004-12-09 11:02:00  ht
# avoid prepare crash on undefined itemType
#
# Revision 1.3  2003/07/09 10:26:55  ht
# prepare item/members
#
# Revision 1.2  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
