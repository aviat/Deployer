"""Schema compilation first phase for any elements"""

__version__="$Revision: 1.2 $"
# $Id: anyElt.py,v 1.2 2002-11-11 18:18:40 ht Exp $

from XSV.compile.Particle import Particle
from XSV.compile.Wildcard import AnyAny, AnyOther, AnyInList

from commonElt import commonElt

class anyElt(commonElt):
  namespace="##any"
  minOccurs="1"
  maxOccurs=None
  processContents="strict"
  def __init__(self,sschema,elt):
    commonElt.__init__(self,sschema,elt)

  def init(self,elt):
    if self.maxOccurs=="0":
      self.component=None
    else:
      self.component=Particle(self.schema.sschema,self,
                              RefineAny(self,self.namespace))

def RefineAny(xrpr,namespace):
  if namespace=='##any':
    anyinst=AnyAny
  elif namespace=='##other':
    anyinst=AnyOther
  else:
    anyinst=AnyInList
  return anyinst(xrpr.schema.sschema,xrpr)


# $Log: anyElt.py,v $
# Revision 1.2  2002-11-11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
