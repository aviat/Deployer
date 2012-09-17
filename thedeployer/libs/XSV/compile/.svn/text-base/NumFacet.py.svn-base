"""Schema compilation: NumFacet component"""

__version__="$Revision: 1.5 $"
# $Id: NumFacet.py,v 1.5 2005-06-08 16:16:11 ht Exp $

from Facet import Facet

class NumFacet(Facet):
  def val(self,type):
    if self.valByType:
      return type.convertToFacetValue(self.stringValue,self.name,self)
    else:
      # Integer
      return _num.convertToFacetValue(self.stringValue,self.name,self)

class MaxInclusive(NumFacet):
  name='maxInclusive'
  valByType=1

class MinInclusive(NumFacet):
  name='minInclusive'
  valByType=1

class MinExclusive(NumFacet):
  name='minExclusive'
  valByType=1

class MaxExclusive(NumFacet):
  name='maxExclusive'
  valByType=1

class FractionDigits(NumFacet):
  name='fractionDigits'
  valByType=0

class TotalDigits(NumFacet):
  name='totalDigits'
  valByType=0

class MinScale(NumFacet):
  name='minScale'
  valByType=0

class MaxScale(NumFacet):
  name='maxScale'
  valByType=0

class Length(NumFacet):
  name='length'
  valByType=0

class MaxLength(NumFacet):
  name='maxLength'
  valByType=0

class MinLength(NumFacet):
  name='minLength'
  valByType=0

def init():
  global _num
  from AbInitio import DecimalST
  _num=DecimalST(None)

# $Log: NumFacet.py,v $
# Revision 1.5  2005-06-08 16:16:11  ht
# q&d add of precisionDecimal
#
# Revision 1.4  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/09/23 21:35:43  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
