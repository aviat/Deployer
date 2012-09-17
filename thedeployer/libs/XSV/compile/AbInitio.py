"""Schema compilation: base class for all ab initio simple types"""

__version__="$Revision: 1.11 $"
# $Id: AbInitio.py,v 1.11 2005-06-08 16:16:11 ht Exp $

# Ab Initio primitive types

import types

from Type import Type
from SimpleType import SimpleType
from SimType import SimType

from XSV.compile import XMLSchemaNS, AST
from XSV.util import xstime

from XSV.compile import abInitioTypes


class AbInitio(SimType):
  isSimple=1
  name=None
  attributeDeclarations={}              # for use when this is a ct's basetype
  contentType='textOnly'                # ditto
  elementTable={}                       # ditto
  basetype=None
  final=[]
  content=None
  abstract="false"
  variety='atomic'
  targetNamespace=XMLSchemaNS
  allowedFacets=[]
  itemType=None
  memberTypes=None
  idt=0
  def __init__(self,sschema):
    self.sschema=sschema
    self.elements=[]
    self.facets={}

  def prepare(self):
    return 1

  def simple(self):
    return self
  
  def isSubtype(self,other,avoid=None):
    if self is other:
      return 1
    if other is Type.urType or other is Type.urSimpleType:
      return 1
    elif (isinstance(other,SimpleType) and
          other.hasMember(self) and
          ((avoid is None) or ('union' not in avoid))):
      return 1
    elif (isinstance(self.basetype,AbInitio) and
          ((avoid is None) or ('restriction' not in avoid))):
      return self.basetype.isSubtype(other,avoid)
    else:
      return 0

  def convertToFacetValue(self,str,facetName,context):
    try:
      return self.convertToValue(str,context)
    except ValueError,ves:
      if ves is None:
        ves=""
      context.error("facet %s value not a valid %s literal%s: %s"%
                    (facetName,self.name,ves,str))
      return

  def convertToActualValue(self,str,item):
    try:
      item.actualValue=self.convertToValue(str,item)
      return
    except ValueError,ves:
      if ves is None:
        ves=""
      return " is not a valid %s literal%s"%(self.name,ves)

  def convertToValue(self,str,item):
    return str

class BooleanST(AbInitio):
  name='boolean'
  allowedFacets=['pattern','whiteSpace']

class StringST(AbInitio):
  name='string'
  allowedFacets=['length', 'minLength', 'maxLength',
                 'pattern', 'enumeration','whiteSpace']

class NumericST(AbInitio):
  pass

class DoubleST(NumericST):
  name='double'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

  def convertToValue(self,str,item):
    try:
      return float(str)
    except ValueError:
      # discard error comment in favour of our own
      if str in ("NaN", "INF", "-INF"):
        return str
      raise ValueError

class FloatST(DoubleST):
  name='float'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class DecimalST(NumericST):
  name='decimal'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive', 'pattern',
		 'maxInclusive', 'enumeration', 'totalDigits',
                 'fractionDigits', 'whiteSpace']

  def convertToValue(self,str,item):
    try:
      if '.' in str:
        return float(str)               # TODO: should do better eventually
      else:
        return long(str)
    except ValueError:
      # discard error comment in favour of our own
      raise ValueError

class pDecimalST(NumericST):
  name='pDecimal'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive', 'pattern',
		 'maxInclusive', 'enumeration', 'totalDigits',
                 'fractionDigits', 'whiteSpace', 'minFractionDigits',
                 'precision', 'lexicalMappings']

  def convertToValue(self,str,item):
    try:
      if '.' in str:
        return float(str)               # TODO: should do better eventually
      else:
        return long(str)
    except ValueError:
      # discard error comment in favour of our own
      raise ValueError

class precisionDecimalST(NumericST):
  name='precisionDecimal'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive', 'pattern',
		 'maxInclusive', 'enumeration', 'totalDigits',
                 'maxScale', 'whiteSpace', 'minScale']

  def convertToValue(self,str,item):
    try:
      if '.' in str:
        return float(str)               # TODO: should do better eventually
      else:
        return long(str)
    except ValueError:
      # discard error comment in favour of our own
      raise ValueError

class TimeDurationST(AbInitio):
  name='duration'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class DateTimeST(NumericST):
  name='dateTime'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

  def convertToValue(self,str,item):
    tv=xstime.xstime(_dateTimeRE)
    tv.install(str)
    tv.normalize()
    return tv

class TimeST(NumericST):
  name='time'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

  def convertToValue(self,str,item):
    tv=xstime.xstime(_timeRE)
    tv.install(str)
    tv.year=tv.month=tv.day=1
    tv.normalize()
    return tv

class DateST(NumericST):
  name='date'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

  def convertToValue(self,s,item):
    tv=xstime.xstime(_dateRE)
    tv.install(s)
    if tv.tz is not None:
      tv.hour=tv.minute=tv.second=0
      tv.normalize()
    tv.isDate=1
    return tv

class gYearMonthST(AbInitio):
  name='gYearMonth'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class gYearST(AbInitio):
  name='gYear'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class gMonthDayST(AbInitio):
  name='gMonthDay'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class gDayST(AbInitio):
  name='gDay'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class gMonthST(AbInitio):
  name='gMonth'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'pattern','whiteSpace']

class HexBinaryST(AbInitio):
  name='hexBinary'
  allowedFacets=['length', 'minLength', 'maxLength',
                 'pattern', 'enumeration','whiteSpace']

class Base64BinaryST(AbInitio):
  name='base64Binary'
  allowedFacets=['length', 'minLength', 'maxLength',
                 'pattern', 'enumeration','whiteSpace']

class URIReferenceST(AbInitio):
  name='anyURI'
  allowedFacets=['length', 'minLength', 'maxLength',
                 'pattern', 'enumeration','whiteSpace']

class NOTATIONST(AbInitio):
  name='NOTATION'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'length',
		 'maxLength', 'minLength', 'pattern','whiteSpace']

class QNameST(AbInitio):
  name='QName'
  allowedFacets=['minExclusive', 'maxExclusive', 'minInclusive',
		 'maxInclusive', 'enumeration', 'length',
		 'maxLength', 'minLength', 'pattern','whiteSpace']

def init():
  global _dateTimeRE, _dateRE, _timeRE
  _dateTimeRE=xstime.xstime(xstime.dateTimePat).compiled_re
  _dateRE=xstime.xstime(xstime.datePat).compiled_re
  _timeRE=xstime.xstime(xstime.timePat).compiled_re
  urSimpleType=AbInitio(None)
  urSimpleType.basetype=Type.urType
  urSimpleType.rootName=urSimpleType.name=AST
  Type.urSimpleType=urSimpleType
  AbInitio.basetype=urSimpleType
  abInitioTypes.extend([('boolean',BooleanST),
                  ('string',StringST), ('float',FloatST),
                  ('double',DoubleST), ('decimal',DecimalST),
                  ('pDecimal',pDecimalST),
                  ('precisionDecimal',precisionDecimalST),
                  ('duration',TimeDurationST),
                  ('dateTime',DateTimeST), ('time',TimeST), ('date',DateST),
                  ('gYearMonth',gYearMonthST), ('gYear',gYearST), 
                  ('gMonthDay',gMonthDayST), ('gDay',gDayST),
                  ('gMonth',gMonthST),
                  ('base64Binary',Base64BinaryST), ('hexBinary',HexBinaryST),
                  ('anyURI',URIReferenceST),
                  ('NOTATION',NOTATIONST),('QName',QNameST)])

# $Log: AbInitio.py,v $
# Revision 1.11  2005-06-08 16:16:11  ht
# q&d add of precisionDecimal
#
# Revision 1.10  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.9  2004/04/01 13:31:42  ht
# work on final/block a bit
#
# Revision 1.8  2004/02/10 13:25:39  ht
# handle non-numeric float/double literals
#
# Revision 1.7  2003/06/06 17:02:23  ht
# fix element default vs mixed bug
#
# Revision 1.6  2003/03/30 16:22:38  ht
# move facet restriction checking to SimType
#
# Revision 1.5  2003/01/20 12:23:45  ht
# try to improve date canonicalisation
#
# Revision 1.4  2002/12/01 21:54:58  ht
# add and inherit idt (identity constraint type) to type defs
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/09/23 21:29:45  ht
# Facet restrict check returns facet if OK,
# handles pattern specially to implement intersection
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
# Revision 1.4  2002/06/12 18:46:19  ht
# restructure in preparation for allowing either normal form to be reflected
#
# Revision 1.3  2002/05/27 16:11:42  ht
# working on new restore
#
# Revision 1.2  2002/05/25 21:54:31  ht
# make new sources split actually work
#
# Revision 1.1  2002/05/24 22:33:14  ht
# split out of XMLSchema

