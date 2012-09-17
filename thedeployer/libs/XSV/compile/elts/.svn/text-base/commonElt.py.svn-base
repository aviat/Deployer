"""Schema compilation first phase for common elements"""

__version__="$Revision: 1.2 $"
# $Id: commonElt.py,v 1.2 2002-11-25 10:39:01 ht Exp $

from XSV.compile.QName import QName

class commonElt:
  def __init__(self,sschema,elt):
    if sschema is not None:
      self.schema=sschema.current
    self.elt=elt

  def error(self,msg,warn=0):
    self.schema.error(msg,self.elt,warn)

  def newComponent(self,kind,table):
    comp=self.component
    if comp is None:
      return
    comp.register(kind,table)

# $Log: commonElt.py,v $
# Revision 1.2  2002-11-25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
