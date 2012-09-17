"""Schema compilation first phase for anyAttribute elements"""

__version__="$Revision: 1.2 $"
# $Id: anyAttributeElt.py,v 1.2 2002-11-11 18:18:40 ht Exp $

from XSV.compile.AttributeUse import AttributeUse

from commonElt import commonElt
from anyElt import RefineAny

class anyAttributeElt(commonElt):
  namespace="##any"
  processContents="lax"

  def init(self,elt):
    self.component=AttributeUse(self.schema.sschema,self,
                                          RefineAny(self,
                                                    self.namespace),
                                          'optional')


# $Log: anyAttributeElt.py,v $
# Revision 1.2  2002-11-11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
