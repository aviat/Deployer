"""W3C XML Schema validity assessment: Attributes"""

__version__="$Revision: 1.8 $"
# $Id: validateAttribute.py,v 1.8 2005-08-22 12:31:22 ht Exp $

from XSV.infoset.XMLInfoset import Attribute as XIAttribute

from XSV.compile.Wildcard import Wildcard
from XSV.compile.QName import QName
from XSV.compile.Attribute import Attribute
from XSV.compile.AttributeUse import AttributeUse
from component import validateText

from verror import verror

from XSV.compile import XMLSchemaInstanceNS as xsi

def validateXSIAttrs(element,schema):
  for a in element.attributes.values():
    if a.namespaceName == xsi:
      if a.localName not in ('type','nil','schemaLocation','noNamespaceSchemaLocation'):
        verror(element,"unknown xsi attribute %s" % a.localName,schema,
               "cvc-complex-type.1.3")
        a.type=None
      else:
        a.type=schema.sschema.sforsi.attributeTable[a.localName]
        res=validateText(a.type.typeDefinition,
                         a.normalizedValue,a,element)
        a.assessedType = a.type.typeDefinition
        if res is not None:
          verror(element,
                 "attribute type check failed for %s: %s%s"%(a.localName,
                                                             a.normalizedValue,
                                                             res),
                 schema,'cvc-attribute.1.2',0,None,a)
        else:
          a.schemaNormalizedValue=a.normalizedValue
      a.assess(schema.sschema,a.type)

def assignAttributeTypes(element, attrdefs, extendable, schema, lax):
  # look up each attribute in attrdefs and assign its type
  # error if attr declaration is not found and type is not extendable
#  print "assigning attrs for %s {%s}%s" % (element.originalName, element.namespaceName, element.localName)
#  print "declared attrs are:"
#  for zz in attrdefs.keys():
#    if isinstance(zz, QName):
#      print "{%s}%s " % (zz.uri, zz.local)
#    else:
#      print zz
  element.attrTable={}
  for a in element.attributes.values():
#    print "assigning attr %s {%s}%s,%s,%s" % (a.originalName, a.namespaceName, a.localName,lax,attrdefs.has_key("#any"))
    ansn=a.namespaceName
    an=QName(None,a.localName,ansn or None)
    element.attrTable[an]=a
    if ansn == xsi:
      continue
    elif attrdefs.has_key(an):
      a.type = attrdefs[an]
    elif lax:
      if ansn:
        schema.sschema.tryHardForDecl(a.localName,ansn,'attribute',schema,a)
        if schema.vAttributeTable.has_key(an):
          a.type=schema.vAttributeTable[an]
        else:
          a.type=None
      else:
        a.type=None
    elif (attrdefs.has_key("#any") and
          attrdefs["#any"].attributeDeclaration.allows(ansn or None)):
      a.type = attrdefs["#any"].attributeDeclaration
    else:
      verror(element,"undeclared attribute %s" % unicode(str(an),'utf-8'),schema,
               "cvc-complex-type.1.3")
      a.type = None
  return

def validateAttributeTypes(element,attrs, attrdefs, schema):
  # check that each attribute matches its type
  # check that all required attributes are present
  for (adq,ad) in attrdefs.items():
    if not attrs.has_key(adq):
      if ad.minOccurs==1:
        verror(element,"required attribute %s not present"%unicode(str(adq),'utf-8'),schema,
               'cvc-complex-type.1.4')
      vc=ad.valueConstraint
      if ((vc is None) and
          isinstance(ad.attributeDeclaration,Attribute)):
        vc=ad.attributeDeclaration.valueConstraint
      if vc is not None:
        na=XIAttribute(element,adq.uri,adq.local,None,
                                        vc[1], # hack, not called for by REC
                                        0)
        na.actualValue=ad.vcv
        na.schemaNormalizedValue=vc[1]  # should be canon val for actualVal
        na.assessedType=na.typeDefinition=ad.attributeDeclaration.typeDefinition
        na.attributeDeclaration=ad.attributeDeclaration
        na.validity='valid'
        na.validationAttempted='full'
        na.validationContext=schema.sschema.docElt
        element.addAttribute(na)
  idTable={}
  xss=schema.sschema.sfors
  for (an,a) in attrs.items():
    if an.uri==xsi:
      # handled already
      continue
    elif a.type is not None:
      if isinstance(a.type,AttributeUse):
        ad=a.type.attributeDeclaration
        td=ad.typeDefinition
        if a.type.valueConstraint is None:
          vc=ad.valueConstraint
        else:
          vc=a.type.valueConstraint
      else:
        ad=a.type
        if not isinstance(ad,Wildcard):
          td=ad.typeDefinition
          vc=ad.valueConstraint
        else:
          vc=None
      if isinstance(ad,Wildcard):
        res=ad.validate(a,schema,'attribute',element)
      else:
        if td is not None:
          res=validateText(td,a.normalizedValue,a,element)
          if res is None:
            a.assessedType = td
            if td.idt:
              if td.idt is 3:
                for ids in a.actualValue:
                  idTable[ids]=[]
              elif td.idt is 2:
                idTable[a.actualValue]=[]
              elif td.idt is 1:
                idTable[a.actualValue]=[element]
            if (vc is not None) and vc[0]=='fixed':
              if a.actualValue!=a.type.vcv:
                verror(element,"fixed value did not match for attribute %s: %s!=%s"%(unicode(str(an),'utf-8'),
                                                                                     a.normalizedValue,vc[1]),schema,"cvc-attribute.1.3")
        else:
          res=None
      if res is not None:
        verror(element,"attribute type check failed for %s: %s%s"%(unicode(str(an),'utf-8'),
                                                                   a.normalizedValue,
                                                                   res),
               schema,'cvc-attribute.1.2',0,None,a)
        a.schemaNormalizedValue=None
    else:
      ad=None
    a.assess(schema.sschema,ad)
  return idTable


# $Log: validateAttribute.py,v $
# Revision 1.8  2005-08-22 12:31:22  ht
# better, i hope, handling of displaying non-ascii qnames
#
# Revision 1.7  2003/03/29 11:36:47  ht
# assessedType on defaulted attrs
#
# Revision 1.6  2003/01/20 12:26:22  ht
# avoid actualValue if not there
#
# Revision 1.5  2002/12/01 21:48:51  ht
# validate ID/IDREF/IDREFS
#
# Revision 1.4  2002/11/25 14:59:11  ht
# make sure vcv is touched when default is used, to force type check etc.
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:47:42  ht
# validation sub-package version
#
