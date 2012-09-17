"""Schema compilation first phase: initialise element mapping table"""

__version__="$Revision: 1.4 $"
# $Id: Init.py,v 1.4 2005-06-08 16:16:11 ht Exp $

from ignoredElts import notationElt, appinfoElt, documentationElt
from redefineElt import redefineElt
from importElt import importElt
from includeElt import includeElt
from attributeGroupElt import attributeGroupElt
from attributeElt import attributeElt
from annotationElt import annotationElt
from xpathElt import selectorElt, fieldElt
from contentElt import complexContentElt, simpleContentElt
from rulElt import restrictionElt, unionElt, listElt, extensionElt
from simpleTypeElt import simpleTypeElt
from anyAttributeElt import anyAttributeElt
from anyElt import anyElt
from explicitGroupElt import sequenceElt, choiceElt, allElt
from groupElt import groupElt
from idElts import keyrefElt, keyElt, uniqueElt
from elementElt import elementElt
from complexTypeElt import complexTypeElt
from schemaElt import schemaElt
from XSV.compile.Facet import Whitespace, Precision, LexicalMappings
from XSV.compile.ListFacet import Pattern, Enumeration
from XSV.compile.NumFacet import FractionDigits, TotalDigits, MinScale, MaxScale
from XSV.compile.NumFacet import Length, MinLength, MaxLength, MinExclusive
from XSV.compile.NumFacet import MaxInclusive, MinInclusive, MaxExclusive

from XSV.compile import eltClasses

def init():
  for en in ["schema","complexType","element","unique","key","keyref",
             "group","all","choice","sequence","any","anyAttribute","simpleType",
             "restriction","list","union","simpleContent","complexContent",
             "field","selector","annotation","appinfo","documentation",
             "extension","attribute","attributeGroup",
             "include","import","redefine","notation"]:
    eltClasses[en]=eval(en+"Elt")
  for en in [ "Enumeration","Length","Pattern","Precision"]:
    eltClasses[en.lower()]=eval(en)
  for (en,cn) in [("fractionDigits",FractionDigits),
                  ("totalDigits",TotalDigits),
                  ("minScale",MinScale),
                  ("maxScale",MaxScale),
                  ("whiteSpace",Whitespace)]:
    eltClasses[en]=cn

  for rcn in [ "Inclusive","Exclusive","Length" ]:
    for pre in [ "Max", "Min"]:
      eltClasses["%s%s"%(pre.lower(),rcn)]=eval("%s%s"%(pre,rcn))

# $Log: Init.py,v $
# Revision 1.4  2005-06-08 16:16:11  ht
# q&d add of precisionDecimal
#
# Revision 1.3  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.2  2002/09/23 21:20:18  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
