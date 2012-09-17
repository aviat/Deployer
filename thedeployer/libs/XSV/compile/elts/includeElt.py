"""Schema compilation first phase for include elements"""

__version__="$Revision: 1.1 $"
# $Id: includeElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt

class includeElt(commonElt):
  schemaLocation=None

  def init(self,elt):
    self.schema.sschema.checkinSchema(self.schema.targetNS,
                                      self.schemaLocation,
                                      self.schema.sschema.fileNames[0],
                                      "include",0,0,elt)


# $Log: includeElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
