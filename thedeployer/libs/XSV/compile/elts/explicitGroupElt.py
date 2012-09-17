"""Schema compilation first phase for explicitGroup elements"""

__version__="$Revision: 1.1 $"
# $Id: explicitGroupElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt

from XSV.compile.Group import All, Choice, Sequence
from XSV.compile.Particle import Particle

class explicitGroupElt(commonElt):
  minOccurs=None
  maxOccurs=None
  def __init__(self,sschema,elt):
    commonElt.__init__(self,sschema,elt)
    self.model=[]

  def init(self,elt):
    if self.maxOccurs=="0":
      self.component=None
    else:
      self.component=Particle(self.schema.sschema,self,
                                        self.compClass(self.schema.sschema,
                                                       self))

class allElt(explicitGroupElt):
  compClass=All

class choiceElt(explicitGroupElt):
  compClass=Choice

class sequenceElt(explicitGroupElt):
  compClass=Sequence



# $Log: explicitGroupElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
