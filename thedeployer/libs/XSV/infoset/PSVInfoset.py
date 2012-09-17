"""Infosets: Additional Infoitems for PSVI"""

__version__="$Revision: 1.1 $"
# $Id: PSVInfoset.py,v 1.1 2002-06-28 10:23:27 ht Exp $

# XXX todo: schemaSpecified, notation, idIdrefTable, identityConstraintTable
#     fundamental facets, final for simple types, identityConstraintDefinitions

#### To think about: stop dumping scope if not 'global', restore from above
####              use name+tns as keys for top-level components, instead of uid

import XMLInfoset

Element = XMLInfoset.Element
Attribute = XMLInfoset.Attribute
psviSchemaNamespace = "http://www.w3.org/2001/05/PSVInfosetExtension"

class NamespaceSchemaInformation(XMLInfoset.InformationItem):

  def __init__(self, schema):
    self.schemaNamespace = schema.targetNS
    self.schemaComponents=[]
    for tab in (schema.typeTable,schema.elementTable,schema.attributeTable,
                schema.groupTable,schema.attributeGroupTable):
      self.schemaComponents=self.schemaComponents+tab.values()
    self.schemaAnnotations=schema.annotations
    self.schemaDocuments = map(lambda l:schemaDocument(l),
                               schema.locations)
    # we could save the document elements of each schema . . .

class schemaDocument(XMLInfoset.InformationItem):

  def __init__(self, location, document=None):
    self.documentLocation = location
    self.document = document


def compareSFSComps(c1,c2):
  # order by class and name
  if c1.reflectedName is c2.reflectedName:
    if c1.name<c2.name:
      return -1
    else:
      return 1
  elif c1.reflectedName<c2.reflectedName:
    return -1
  else:
    return 1

Element.validationAttempted = None
Element.validationContext = None
Element.validity = None
Element.errorCode = None
Element.schemaNormalizedValue = None
Element.typeDefinition = None
Element.memberTypeDefinition = None
Element.typeDefinitionType = None
Element.typeDefinitionNamespace = None
Element.typeDefinitionAnonymous = None
Element.typeDefinitionName = None
Element.memberTypeDefinitionNamespace = None
Element.memberTypeDefinitionAnonymous = None
Element.memberTypeDefinitionName = None
Element.elementDeclaration = None
Element.null = 0
Element.schemaInformation = None

Attribute.validationAttempted = None
Attribute.validationContext = None
Attribute.validity = None
Attribute.errorCode = None
Attribute.schemaNormalizedValue = None
Attribute.typeDefinition = None
Attribute.memberTypeDefinition = None
Attribute.typeDefinitionType = None
Attribute.typeDefinitionNamespace = None
Attribute.typeDefinitionAnonymous = None
Attribute.typeDefinitionName = None
Attribute.memberTypeDefinitionNamespace = None
Attribute.memberTypeDefinitionAnonymous = None
Attribute.memberTypeDefinitionName = None
Attribute.attributeDeclaration = None

# $Log: PSVInfoset.py,v $
# Revision 1.1  2002-06-28 10:23:27  ht
# infoset basics
#
