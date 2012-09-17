"""Schema compilation first phase for redefine elements"""

__version__="$Revision: 1.1 $"
# $Id: redefineElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from includeElt import includeElt

class redefineElt(includeElt):
  schemaLocation=None

  def init(self,elt):
    res=self.schema.sschema.checkinSchema(self.schema.targetNS,
                                          self.schemaLocation,
                                          self.schema.sschema.fileNames[0],
                                          "redefine",0,0,elt)
    if res is not None and self.__dict__.has_key('dds'):
      for dd in self.dds:
        if dd.name:
          dd.component.redefine()


# $Log: redefineElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
