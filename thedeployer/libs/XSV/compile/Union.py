"""Schema compilation: Union component"""

__version__="$Revision: 1.6 $"
# $Id: Union.py,v 1.6 2007-02-16 14:20:54 ht Exp $

from Component import Component
from QName import QName
from SimpleType import SimpleType
from AbInitio import AbInitio

class Union(Component):
  variety='union'
  primitiveType=None
  itemType=None
  membertypeNames=[]
  someMembers=None
  allowedFacets=['pattern', 'enumeration','whiteSpace']
  facets={}

  def __init__(self,sschema,xrpr):
    Component.__init__(self,sschema,xrpr)
    if xrpr.memberTypes:
      self.membertypeNames=map(lambda n,e=xrpr.elt,f=sschema:QName(n,e,f),
                               xrpr.memberTypes.split())
    if xrpr.subTypes:
      self.someMembers=map(lambda sub:sub.component,
                           xrpr.subTypes)
    elif not xrpr.memberTypes:
      # no elt means builtin
      if xrpr.elt is not None:
        self.error("union must have 'memberTypes' attribute or some SimpleType children")

  def __getattr__(self,name):
    if name=='memberTypes':
      self.memberTypes=self.someMembers or []
      if self in self.memberTypes:
        self.error("union may not include itself")
        self.memberTypes=[]        
      for mtn in self.membertypeNames:
        if self.schema.vTypeTable.has_key(mtn):
          td=self.schema.vTypeTable[mtn]
          if isinstance(td,SimpleType):
           if td.variety=="union":
             if (td is self or td.memberTypes is self.memberTypes):
               self.error("union may not include itself")
             else:
               for std in td.memberTypes:
                 self.memberTypes.append(std)
           else:
            self.memberTypes.append(td)
          elif isinstance(td,AbInitio):
            self.memberTypes.append(td)
          else:
            self.error("Members of union types must be simple types, but %s is not"%td.name)
        else:
          self.error("Undefined type %s referenced as type definition of %s"%(mtn, self.super.name))
      return self.memberTypes
    else:
      raise AttributeError,name

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=1
    for mt in self.memberTypes:
      p1=mt.prepare() and p1
    return p1

# $Log: Union.py,v $
# Revision 1.6  2007-02-16 14:20:54  ht
# implement self-inclusion bar checking
#
# Revision 1.5  2003/07/09 10:26:55  ht
# prepare item/members
#
# Revision 1.4  2003/04/22 15:15:35  ht
# check for simple, fold union
#
# Revision 1.3  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.2  2002/08/21 08:54:34  ht
# some missing imports
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
