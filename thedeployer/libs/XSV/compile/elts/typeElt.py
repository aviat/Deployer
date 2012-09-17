"""Schema compilation first phase for type elements"""

__version__="$Revision: 1.1 $"
# $Id: typeElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt

class typeElt(commonElt):
  name=None
  basetype=None
  derivedBy=None
  id=None
  annot=None
  def __init__(self,sschema,elt):
    commonElt.__init__(self,sschema,elt)

  def newComponent(self,schema):
    commonElt.newComponent(self,'type',schema.typeTable)


# $Log: typeElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
