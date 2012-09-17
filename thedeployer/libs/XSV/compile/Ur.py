"""Schema compilation: Ur component"""

__version__="$Revision: 1.3 $"
# $Id: Ur.py,v 1.3 2005-04-18 13:47:09 ht Exp $

from Component import Component
from Type import Type
from SimpleType import SimpleType
from ComplexType import ComplexType
from Particle import Particle
from Group import Sequence
from QName import QName

from XSV.compile import XMLSchemaNS

class Ur(ComplexType,SimpleType):

  def __init__(self,sschema):
    Component.__init__(self,sschema,None)

  def isSubtype(self,other,avoid=None):
    return self is other


def init():
  # TODO: why is anybody looking at the details of this, c.f. prisc.{xml,xsd}
  urType=Ur(None)
  urType.basetype=urType
  urType.final=[]
  urType.prohibitedSubstitutions=[]
  urType.contentType='mixed'
  urType.model=Particle(None,None,Sequence(None,None))
  urType.model.occurs=(1,1)
  urType.model.term.particles=[]
  urType.name='anyType'
  urType.targetNamespace=XMLSchemaNS
  urType.qname=QName(None,'anyType',XMLSchemaNS)
  urType.attributeDeclarations={}
  urType.derivationMethod='restriction'
  urType.abstract='false'
  urType.extendable=0			# stale!!
  Type.urType=urType                        # publish it



# $Log: Ur.py,v $
# Revision 1.3  2005-04-18 13:47:09  ht
# give urtype a qname
#
# Revision 1.2  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
