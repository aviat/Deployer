"""Schema compilation first phase for simpleType elements"""

__version__="$Revision: 1.4 $"
# $Id: simpleTypeElt.py,v 1.4 2003-04-01 18:47:15 ht Exp $

from typeElt import typeElt

from XSV.compile.QName import QName
from XSV.compile.SimpleType import SimpleType
from XSV.compile.Facet import Whitespace

from XSV.compile import XMLSchemaNS

## Note that primitive builtins are _not_ SimpleTypes, see AbInitio.
## SimpleType itself is largely a placeholder:  it has a targetNamespace and
##  may have a name.  In principle it always has a basetype, but in practice
##  may only have a basetypeName, and basetype is filled in lazily.

## It also should have a variety, but this is _also_ lazy, as it may depend
##  on the basetype.

## The real action is in the subComp, which should be an instance of Atomic,
##   List or Union, but may be a Restriction which contains one of these as
##   its actual.  Opportunities for improved efficiency obviously exist, by
##   eliminating one or both indirections once the truth is known.

class simpleTypeElt(typeElt):
  content='textOnly'
  restriction=None
  list=None
  union=None
  final=""
  def init(self,elt):
    basetypeName=None
    if self.restriction is not None:
      derivedBy='restriction'
      if self.restriction.__dict__.has_key('base'):
        basetypeName=QName(self.restriction.base,
                                     elt,self.schema.sschema)
        if (self.restriction.facets and
            basetypeName.local=='anySimpleType' and
            basetypeName.uri==XMLSchemaNS and
            len(self.restriction.facets)>1 and
            not(isinstance(self.restriction.facets[0],Whitespace))):
          self.error("anySimpleType may not be directly restricted with facets")
          basetypeName=QName('string',elt,self.schema.sschema)
    elif self.list is not None:
      derivedBy='list'
      basetypeName=QName(None,'anySimpleType',
                                   XMLSchemaNS)
    elif self.union is not None:
      derivedBy='union'
      basetypeName=QName(None,'anySimpleType',XMLSchemaNS)
    else:
      # no elt for fakes for builtins
      if elt is not None:
        self.error("simpleType must have one of restriction, list or union as a child")
        self.component=SimpleType(self.schema.sschema,self,None,
                                            None,None)
        return
    self.component=SimpleType(self.schema.sschema,
                                        self,derivedBy,basetypeName,
                                        (self.restriction or self.list or
                                         self.union).component)


# $Log: simpleTypeElt.py,v $
# Revision 1.4  2003-04-01 18:47:15  ht
# vacuous simple types have _no_ derivedBy
#
# Revision 1.3  2002/09/23 21:20:18  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:10:28  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
