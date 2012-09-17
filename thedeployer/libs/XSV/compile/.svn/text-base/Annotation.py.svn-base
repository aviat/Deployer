"""Schema compilation: Annotation component"""

__version__="$Revision: 1.1 $"
# $Id: Annotation.py,v 1.1 2002-06-28 09:40:22 ht Exp $

from Component import Component

class Annotation(Component):
  documentation=[]
  appinfo=[]
  attrs=[]

  def __init__(self,sschema,xrpr=None):
    Component.__init__(self,sschema,xrpr)
    if xrpr is not None:
      if xrpr.documentation is not None:
        self.documentation=map(lambda a:a.elt.elt,xrpr.documentation)
      if xrpr.appinfo is not None:
        self.appinfo=map(lambda a:a.elt.elt,xrpr.appinfo)


# $Log: Annotation.py,v $
# Revision 1.1  2002-06-28 09:40:22  ht
# XSV as package: components
#
