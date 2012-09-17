"""Schema compilation: AnyAttribute component"""

__version__="$Revision: 1.1 $"
# $Id: AnyAttribute.py,v 1.1 2002-06-28 09:40:22 ht Exp $

from Component import Component

class AnyAttribute(Component):
  namespace=None
  def __init__(self,sschema,xrpr,wildcard):
    Component.__init__(self,sschema,xrpr,None)
    self.wildcard=wildcard

  def merge(self,mine,other):
    self.error("*** merging anyAttrs %s and %s, not implemented yet\n"%
                   (mine, other),
               1)
    return mine


# $Log: AnyAttribute.py,v $
# Revision 1.1  2002-06-28 09:40:22  ht
# XSV as package: components
#
