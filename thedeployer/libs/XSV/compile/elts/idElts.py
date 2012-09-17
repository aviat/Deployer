"""Schema compilation first phase for idElts.py elements"""

__version__="$Revision: 1.1 $"
# $Id: idElts.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt
from XSV.compile.KCons import Key, Keyref, Unique

class uniqueElt(commonElt):
  def init(self,elt):
    self.component=Unique(self.schema.sschema,self)

class keyrefElt(commonElt):
  def init(self,elt):
    self.component=Keyref(self.schema.sschema,self)

class keyElt(commonElt):
  def init(self,elt):
    self.component=Key(self.schema.sschema,self)


# $Log: idElts.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
