"""Individual normal form: Reflect instances as XML doc in INF"""

__version__="$Revision: 1.10 $"
# $Id: reflect.py,v 1.10 2005-08-10 20:32:08 ht Exp $

import types

from XSV.infoset import PSVInfoset
from XSV.infoset import XMLInfoset

from XSV.compile.List import List
from XSV.compile.Union import Union
from XSV.compile.ComplexType import ComplexType
from XSV.compile.Group import Group, ModelGroup
from XSV.compile.Particle import Particle
from XSV.compile.Wildcard import Wildcard
from XSV.compile.Element import Element
from XSV.compile.AttributeUse import AttributeUse
from XSV.compile.Attribute import Attribute
from XSV.compile.AttributeGroup import AttributeGroup
from XSV.compile.Annotation import Annotation
from XSV.compile.KCons import Kcons, Key, Keyref, Unique
from XSV.compile.AnyAttribute import AnyAttribute
from XSV.compile.AbInitio import AbInitio
from XSV.compile.DDummy import DumpedSchema, namespaceSchemaInformation
from XSV.compile.DDummy import contentType, namespaceConstraint, valueConstraint
from XSV.compile.DDummy import xpathTemp, schemaDocument
from XSV.compile.Facet import Facet
from XSV.compile.ListFacet import Pattern
from XSV.compile.Component import Component
from XSV.compile.AbInitio import AbInitio
from XSV.compile.SimpleType import SimpleType
from XSV.compile.Type import Type

from XSV.compile import XMLSchemaNS, simpleTypeMap, builtinPats

from XSV.compile.SchemaError import shouldnt

def setup():
  List.reflectedName='list'
  List.reflectionInMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('atomic','list'),'component',0,'basetype'),
                   ('lvariety','aspecial',0,'varietyReflect'),
                   (('facet','enumeration','fractionDigits', 'minFractionDigits',
                     'precision', 'lexicalMappings','minInclusive',
                     'pattern','whiteSpace'),
                    'esspecial',0,'facetsReflect'),
                   ('final','list',0,'final'),
                   (('atomic','list','union'),'component',1,'itemType'),
                   (('annotation',),'components',0,'annotations') # not per REC,
                                                                # but correct
                   )
  List.reflectionOutMap=List.reflectionInMap

  Union.reflectedName='union'
  Union.reflectionInMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('atomic','union'),'component',0,'basetype'),
                   ('uvariety','aspecial',0,'varietyReflect'),
                   (('facet','enumeration','fractionDigits', 'minFractionDigits',
                     'precision', 'lexicalMappings','minInclusive',
                     'pattern','whiteSpace'),
                    'esspecial',0,'facetsReflect'),
                   ('final','list',0,'final'),
                   (('atomic','list'),'components',1,'memberTypes'),
                   (('annotation',),'components',0,'annotations') # not per REC,
                                                                # but correct
                   )
  Union.reflectionOutMap=Union.reflectionInMap

  ComplexType.reflectedName='complexTypeDefinition'
  ComplexType.reflectionInMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('complexTypeDefinition','atomic','union','list'),
                    'component',1,'basetype'),
                   ('derivationMethod','string',1,'derivationMethod'),
                   ('final','list',0,'final'),
                   ('abstract','boolean',0,'abstract'),
                   (('attributeUse',),'esspecial',1,'attributesReflect'),
                   (('attributeWildcard','wildcard'),
                    'especial',1,'attributeWildcardReflect'),
                   (('contentType',),'especial',0,'contentTypeReflect'),
                   ('prohibitedSubstitutions','list',
                    0,'prohibitedSubstitutions'),
                   (('annotation',),'components',0,'annotations'))
  ComplexType.reflectionOutMap=ComplexType.reflectionInMap

  ModelGroup.reflectedName='modelGroupDefinition'
  ModelGroup.reflectionInMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('annotation',),'component',1,'annotation'),
                   (('modelGroup',),'especial',0,'mgReflect'))
  ModelGroup.reflectionOutMap=ModelGroup.reflectionInMap

  Group.reflectedName='modelGroup'
  Group.reflectionInMap=(('compositor','string',0,'compositor'),
                   (('particle',),
                    'components',0,'particles'),
                   (('annotation',),'component',1,'annotation'))
  Group.reflectionOutMap=Group.reflectionInMap

  Particle.reflectedName='particle'
  Particle.reflectionInMap=(('minOccurs','string',0,'minOccurs'),
                   ('maxOccurs','string',0,'maxOccurs'),
                   ('minOccurs','aspecial',0,'occursReflect'), # hack,
                                                              # for rebuild only
                   (('elementDeclaration','wildcard','modelGroup'),
                    'component',0,'term'))
  Particle.reflectionOutMap=Particle.reflectionInMap

  Wildcard.reflectedName='wildcard'
  Wildcard.reflectionInMap=((('namespaceConstraint',),'especial',
                    0,'wildcardNamespaceReflect'),
                   ('processContents','string',0,'processContents'),
                   (('annotation',),'component',1,'annotation'))
  Wildcard.reflectionOutMap=Wildcard.reflectionInMap

  Element.reflectedName='elementDeclaration'
  Element.reflectionInMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('complexTypeDefinition','atomic','union','list'),
                    'component',1,'typeDefinition'),
                   (('valueConstraint',),'especial',1,'vcReflect'),
                   ('nillable','boolean',0,'nullable'),
                   ('scope','aspecial',1,'scopeReflect'),
                   (('key','unique','keyref'),'esspecial',
                    0,'icsReflect'),
                   (('elementDeclaration',),
                    'component',1,'equivalenceClassAffiliation'),
                   ('substitutionGroupExclusions','list',0,'final'),
                   ('disallowedSubstitutions','list',
                    0,'prohibitedSubstitutions'),
                   ('abstract','boolean',0,'abstract'),
                   (('annotation',),'component',1,'annotation'))
  Element.reflectionOutMap=Element.reflectionInMap

  AttributeUse.reflectedName='attributeUse'
  AttributeUse.reflectionInMap=(('required','boolean',0,'minOccurs'),
                   (('attributeDeclaration',),'component',
                    0,'attributeDeclaration'),
                   (('valueConstraint',),'especial',1,'vcReflect'))
  AttributeUse.reflectionOutMap=AttributeUse.reflectionInMap

  Attribute.reflectedName='attributeDeclaration'
  Attribute.reflectionInMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('scope','aspecial',1,'scopeReflect'),
                   (('atomic','list','union'),'component',1,'typeDefinition'),
                   (('valueConstraint',),'especial',1,'vcReflect'),
                   (('annotation',),'component',1,'annotation'))
  Attribute.reflectionOutMap=Attribute.reflectionInMap

  AttributeGroup.reflectedName='attributeGroupDefinition'
  AttributeGroup.reflectionInMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('attributeUse',),'esspecial',1,'attributesReflect'),
                   (('attributeWildcard','wildcard'),
                    'especial',1,'attributeWildcardReflect'),
                   (('annotation',),'component',1,'annotation'))
  AttributeGroup.reflectionOutMap=AttributeGroup.reflectionInMap

  Annotation.reflectedName='annotation'
  Annotation.reflectionInMap=((('XML.Element',),'components',0,'appinfo'),
                   (('XML.Element',),'components',0,'documentation'),
                   (('XML.Attribute',),'components',0,'attrs'))
  Annotation.reflectionOutMap=Annotation.reflectionInMap

  Key.reflectedName=Key.cname
  Keyref.reflectedName=Keyref.cname
  Unique.reflectedName=Unique.cname
  Kcons.reflectionInMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('selector','xpath'),'especial',0,'selectorReflect'),
                   (('fields','xpath'),'especial',0,'fieldsReflect'),
                   (('key',),'component',1,'refer'),
                   (('annotation',),'component',1,'annotation'))
  Kcons.reflectionOutMap=Kcons.reflectionInMap

  AnyAttribute.reflectedName='wildcard'

  AbInitio.reflectedName='atomic'
  AbInitio.reflectionInMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   (('atomic',),'component',0,'basetype'),
                   (('atomic',),'component',0,'primitiveType'),
                   (('facet','enumeration','fractionDigits', 'minFractionDigits',
                     'precision', 'lexicalMappings', 'minInclusive',
                     'pattern','whiteSpace'),
                    'esspecial',0,'facetsReflect'),
                   # XXX
                   (('fundamentalFacet',),'esspecial',0, 'fundamentalFacetsReflect'),
                   # XXX
                   ('final','list',0,'final'),
                   (('annotation',),'components',0,'annotations') # not per REC,
                                                                # but correct
                   )
  AbInitio.reflectionOutMap=AbInitio.reflectionInMap

  DumpedSchema.reflectionInMap=((('namespaceSchemaInformation',),
                                 'components',0,'schemaInformation'),)
  DumpedSchema.reflectionOutMap=DumpedSchema.reflectionInMap

  namespaceSchemaInformation.reflectionInMap=((('elementDeclaration', 'complexTypeDefinition',
                     'atomic','union','list','attributeDeclaration',
                     'modelGroupDefinition','attributeGroupDefinition',
                     'schemaDocument'),
                    'components',0,'components'),
                   ('schemaNamespace','string',0,'schemaNamespace'))
  namespaceSchemaInformation.reflectionOutMap=namespaceSchemaInformation.reflectionInMap

  contentType.reflectionInMap=(('variety','string',1,'variety'),
                   (('atomic','union','list','particle'),'component',1,'model'))
  contentType.reflectionOutMap=contentType.reflectionInMap

  namespaceConstraint.reflectionInMap=(('variety','string',0,'variety'),
                   ('namespaces','list',1,'namespaces'))
  namespaceConstraint.reflectionOutMap=namespaceConstraint.reflectionInMap

  valueConstraint.reflectionInMap=(('variety','string',0,'variety'),
                   ('value','string',0,'value'))
  valueConstraint.reflectionOutMap=valueConstraint.reflectionInMap

  xpathTemp.reflectionInMap=(('path','string',0,'path'),)
  xpathTemp.reflectionOutMap=xpathTemp.reflectionInMap

  schemaDocument.reflectionInMap=(('documentLocation','string',0,'documentLocation'),)
  schemaDocument.reflectionOutMap=schemaDocument.reflectionInMap

  Facet.reflectionInMap=(('value','string',0,'value'),
                                   ('fixed','boolean',0,'fixed'))
  Facet.reflectionOutMap=Facet.reflectionInMap[0:1]
  simpleTypeMap.update({'list':List,
                        'union':Union,
                        'atomic':AbInitio})

InformationItem = XMLInfoset.InformationItem
Document = XMLInfoset.Document
Namespace = XMLInfoset.Namespace
xsiNamespace = XMLInfoset.xsiNamespace
infosetSchemaNamespace = XMLInfoset.infosetSchemaNamespace
psviSchemaNamespace = PSVInfoset.psviSchemaNamespace

def informationitemReflect(self, parent=None):
  XMLInfoset.Element(parent, infosetSchemaNamespace, "XXX")

InformationItem.reflect=informationitemReflect

def reflectString(self, parent, name, value, nullable, ns=None):
  if value is None:
    if not nullable:
      help()
  else:
    attr = XMLInfoset.Attribute(parent, ns, name, None, value)
    parent.addAttribute(attr)

InformationItem.reflectString=reflectString

def reflectNull(self, parent, name, ns=None):
  e = XMLInfoset.Element(parent, ns or infosetSchemaNamespace, name)
  parent.addChild(e)
  nullAttr = XMLInfoset.Attribute(e, xsiNamespace, "nil", None, "true")
  e.addAttribute(nullAttr)

InformationItem.reflectNull=reflectNull

def reflectBoolean(self, parent, name, value, nullable, ns=None):
#    sys.stderr.write("reflecting boolean %s, nullable=%s\n" % (value, nullable))
  if value != None:
    if value:
      value = "true"
    else:
      value = "false"
  self.reflectString(parent, name, value, nullable)

InformationItem.reflectBoolean=reflectBoolean

def documentReflect(self, parent=None, control=0):

  doc = Document(None, None, "yes")

  document = XMLInfoset.Element(doc, infosetSchemaNamespace, "document", None, None,
                     {None:Namespace(None, infosetSchemaNamespace),
                      "i":Namespace("i", xsiNamespace),
                      "xs":Namespace("xs",
                                     "http://www.w3.org/2001/XMLSchema"),
                      "xml":Namespace("xml",
                                      "http://www.w3.org/XML/1998/namespace")})
  doc.addChild(document)

  self.children[0].reflect(document)

  for e in self.unparsedEntities:
    e.reflect(document)

  for n in self.notations:
    n.reflect(document)


  self.reflectString(document, "baseURI", self.baseURI, 1)

  self.reflectString(document, "characterEncodingScheme", self.characterEncodingScheme, 1)

  self.reflectString(document, "standalone", self.standalone, 1)

  self.reflectString(document, "version", self.version, 1)

  self.reflectBoolean(document, "allDeclarationsProcessed", self.allDeclarationsProcessed, 0)

  return doc

Document.reflect=documentReflect

def elementReflect(self, parent,dumpChars=1):

  element = XMLInfoset.Element(parent, infosetSchemaNamespace, "element")
  parent.addChild(element)

  self.reflectString(element, "namespaceName", self.namespaceName, 1)

  self.reflectString(element, "localName", self.localName, 0)

  self.reflectString(element, "prefix", self.prefix, 1)


  for a in self.attributes.values():
    a.reflect(element)

  if self.namespaceAttributes:
    for a in self.namespaceAttributes.values():
      a.reflect(element)

  for c in self.children:
    if (not dumpChars) and isinstance(c,XMLInfoset.Characters):
      pass
    c.reflect(element)

  if self.inScopeNamespaces:
    for a in self.inScopeNamespaces.values():
      a.reflect(element)

  self.reflectString(element, "baseURI", self.baseURI, 1)

  return element

XMLInfoset.Element.reflect=elementReflect

def charactersReflect(self, parent):
  tt=XMLInfoset.Element(parent,infosetSchemaNamespace,"text")
  parent.addChild(tt)
  self.reflectString(tt,"content",self.characters,0)

XMLInfoset.Characters.reflect=charactersReflect

def attributeReflect(self, parent=None):
  attribute = XMLInfoset.Element(parent, infosetSchemaNamespace, "attribute")
  parent.addChild(attribute)

  self.reflectString(attribute, "namespaceName", self.namespaceName, 1)

  self.reflectString(attribute, "localName", self.localName, 0)

  self.reflectString(attribute, "prefix", self.prefix, 1)

  self.reflectString(attribute, "normalizedValue", self.normalizedValue, 1)

  self.reflectBoolean(attribute, "specified", self.specified, 0)

  self.reflectString(attribute, "attributeType", self.attributeType, 1)

  self.reflectString(attribute, "references", None, 1) # not implemented

  return attribute

XMLInfoset.Attribute.reflect=attributeReflect

def namespaceReflect(self, parent=None):
  namespace = XMLInfoset.Element(parent, infosetSchemaNamespace, "namespace")
  parent.addChild(namespace)
  self.reflectString(namespace, "prefix", self.prefix, 1)

  self.reflectString(namespace, "namespaceName",
                     self.namespaceName, 0)

Namespace.reflect=namespaceReflect

def nsiReflect(self, parent=None):

  nsi = XMLInfoset.Element(parent, psviSchemaNamespace, "namespaceSchemaInformation")
  parent.addChild(nsi)

  self.reflectString(nsi, "schemaNamespace", self.schemaNamespace, 1)

  for c in self.schemaComponents:
    c.reflect(nsi,1)

  for d in self.schemaDocuments:
    d.reflect(nsi)

  for a in self.schemaAnnotations:
    a.reflect(nsi)

PSVInfoset.NamespaceSchemaInformation.reflect=nsiReflect

def sdReflect(self, parent=None):
  sd = XMLInfoset.Element(parent, psviSchemaNamespace, "schemaDocument")
  parent.addChild(sd)

  self.reflectString(sd, "documentLocation", self.documentLocation, 1)

PSVInfoset.schemaDocument.reflect=sdReflect

def componentReflect(self,parent,forceFull=0,noID=0):
  if self.uid and not forceFull:
    # a pointer
    self.reflectAsPointer(self.uid,parent)
  else:
    e = XMLInfoset.Element(parent, psviSchemaNamespace, self.reflectedName)
    parent.addChild(e)

    if self.needsId and not forceFull:
      self.assignUid()
    if self.uid and not noID:
      idAttr = XMLInfoset.Attribute(e, None, "id", None, self.uid)
      e.addAttribute(idAttr)
    for rme in self.reflectionOutMap:
      # reflectionMap entries: (compPropertyName,valueType,nullable,
      #                         pythonPropertyName)
#      print ('rme',rme)
      value=getattr(self,rme[3])
#      print ('vv',self,value)
      if rme[1]=='string':
        e.reflectString(e,rme[0],value,
                        rme[2])
      elif rme[1]=='list':
        if len(value)>0:
          e.reflectString(e,rme[0],' '.join(value),rme[2])
      elif rme[1]=='boolean':
        if str(value) not in ('true','false'):
          if value:
            value='true'
          else:
            value='false'
        e.reflectString(e,rme[0],value,
                        rme[2])
      elif rme[1]=='component':
        if value is not None:
          value.reflect(e)
        elif rme[2]:
          pass
      elif rme[1] in ('aspecial','especial','esspecial'):
        value(e)
      elif rme[1]=='components':
        if value is None and rme[2]:
          continue
        for vv in value or []:
          vv.reflect(e)

def reflectAsPtr(self,ref,parent,eltName,eltns=psviSchemaNamespace):
  c = XMLInfoset.Element(parent, eltns, eltName)
  parent.addChild(c)
  refAttr = XMLInfoset.Attribute(c, None, "ref", None, ref)
  c.addAttribute(refAttr)
  nilAttr = XMLInfoset.Attribute(c, xsiNamespace, "nil", None, "true")
  c.addAttribute(nilAttr)
  if self.alwaysNamed:
    nAttr = XMLInfoset.Attribute(c, None, "name", None, self.name)
    c.addAttribute(nAttr)
    if self.targetNamespace is not None:
      nsAttr = XMLInfoset.Attribute(c, None, "tns", None, self.targetNamespace)
      c.addAttribute(nsAttr)

def reflectAIAsPointer(self,ref,parent):
  return reflectAsPtr(self,ref,parent,"atomic")

def reflectCompAsPointer(self, ref, parent=None):
  return reflectAsPtr(self,ref,parent,self.reflectedName)

Component.reflectAsPointer=reflectCompAsPointer
AbInitio.reflectAsPointer=reflectAIAsPointer
Component.reflect=componentReflect
Component.needsId=0
Component.alwaysNamed=0
AbInitio.alwaysNamed=0
ComplexType.needsId=1 # only nested Elts, Attrs, CTs and STs need Ids
SimpleType.needsId=1
Element.needsId=1
Attribute.needsId=1
Pattern.needsId=1                       # because they have big patterns
Pattern.uids=None
Attribute.alwaysNamed=1                 # Because typelocal-table is built right away
Kcons.needsId=1

def modelReflect(self,parent,forceFull=0,noID=0):
  tick=0
  if self.name:
    if (not forceFull) and self.id:
      # forward reference to model group defn
      self.reflectedName='modelGroup'
      tick=1
    else:
      self.reflectionOutMap=ModelGroup.reflectionOutMap
  Component.reflect(self,parent,forceFull,noID)
  if tick:
    self.reflectedName='modelGroupDefinition'
    
Group.reflect=modelReflect

allPrefixes={'xsd':XMLSchemaNS,
             'xsi':xsiNamespace}
allNSs={xsiNamespace:'xsi',
        XMLSchemaNS:'xsd'}

def assignUid(self):
  cnn=None
  nn=self.name
  if self.targetNamespace:
    if allNSs.has_key(self.targetNamespace):
      cnn="%s.."%allNSs[self.targetNamespace]
    elif (self.xrpr and self.xrpr.elt and self.xrpr.elt.namespaceDict):
      for (n,v) in self.xrpr.elt.namespaceDict.items():
        # note that this namespaceDict is a Mapper hack from layer.py
        if v==self.targetNamespace:
          if n!=None and (not allPrefixes.has_key(n)):
            allNSs[self.targetNamespace]=n
            allPrefixes[n]=self.targetNamespace
            cnn="%s.."%n
          break
    if cnn:
      if ((isinstance(self,Element) or
           isinstance(self,Attribute)) and self.scope!='global'):
        # avoid spurious conflicts
        nn="%s.%s"%(nn,self.id)
    else:
      n="x%d"%self.id
      allNSs[self.targetNamespace]=n
      allPrefixes[n]=self.targetNamespace
      cnn="%s.."%n
  else:
    cnn=""
    if nn:
      nn="%s.%s"%(nn,self.id)
  self.uid="%s%s.%s"%(cnn,self.kind,nn or "_anon_%s"%self.id)

Component.uid=None
Component.assignUid=assignUid
Type.kind='type'
Element.kind='elt'
Attribute.kind='attr'
Group.kind='mg'
AttributeGroup.kind='ag'
Kcons.kind='idCons'
Facet.kind='f'
Pattern.reflectedName='pattern'
# Notation.kind='ntn'

def abInitioReflect(self,parent,force=0):
  if force:
    e = XMLInfoset.Element(parent, psviSchemaNamespace, 'atomic')
    parent.addChild(e)
    idAttr = XMLInfoset.Attribute(e, None, "id", None, self.uid)
    e.addAttribute(idAttr)
    nullAttr = XMLInfoset.Attribute(e, xsiNamespace, "nil", None, "true")
    e.addAttribute(nullAttr)
  else:
    # a pointer
    self.reflectAsPointer(self.uid,parent)

AbInitio.reflect=abInitioReflect

def aiAssign(self):
  self.uid=self.name

AbInitio.assignUid=aiAssign
AbInitio.uid=None
def scopeReflect(self,parent):
  if self.scope is not None:
    if self.scope=='global':
      parent.reflectString(parent,'scope','global',0)
    else:
      parent.reflectString(parent,'scope','local',0)

Element.scopeReflect=scopeReflect
Attribute.scopeReflect=scopeReflect

def vcReflect(self,parent):
  if self.valueConstraint is not None:
    vc=XMLInfoset.Element(parent,psviSchemaNamespace,'valueConstraint')
    parent.addChild(vc)
    vc.reflectString(vc,'variety',self.valueConstraint[0],
                     1)
    vc.reflectString(vc,'value',self.valueConstraint[1],
                     0)

Element.vcReflect=vcReflect
Attribute.vcReflect=vcReflect
AttributeUse.vcReflect=vcReflect

def icsReflect(self,parent):
  for kd in self.keys:
    kd.reflect(parent)
  for ud in self.uniques:
    ud.reflect(parent)
  for krd in self.keyrefs:
    krd.reflect(parent)

Element.icsReflect=icsReflect

def adReflect(self,parent):
  tab={}
  for ad in self.attributeDeclarations:
    ad.expand(tab)
  for vv in tab.values():
    vv.reflect(parent)

AttributeGroup.adReflect=adReflect

def mgReflect(self,parent):
  self.reflectionOutMap=Group.reflectionOutMap
  self.reflectedName='modelGroup'
  name=self.name                        # stop recursion
  self.name=None
  self.reflect(parent,1,1)
  self.name=name

Group.mgReflect=mgReflect

def wnsReflect(self,parent):
  ns=XMLInfoset.Element(parent,psviSchemaNamespace,'namespaceConstraint')
  parent.addChild(ns)
  if self.allowed=='##any':
    ns.reflectString(ns, 'variety', 'any', 0)
  else:
    if self.negated:
      ns.reflectString(ns, 'variety', 'negative', 0)
    else:
      ns.reflectString(ns, 'variety', 'positive', 0)
    if len(self.namespaces)>0:
      ns.reflectString(ns,'namespaces',' '.join(map(lambda n:n or '##none',
                                                       self.namespaces)),0)

Wildcard.wildcardNamespaceReflect=wnsReflect

def ctReflect(self,parent):
  if self.contentType is not None:
    ct=XMLInfoset.Element(parent,psviSchemaNamespace,'contentType')
    parent.addChild(ct)
    if self.contentType=='empty':
      ct.reflectString(ct, 'variety','empty',0)
    elif self.contentType in ('elementOnly','mixed'):
      ct.reflectString(ct, 'variety',self.contentType,0)
      self.model.reflect(ct)
    else:
      ct.reflectString(ct, 'variety','simple',0)
      self.model.reflect(ct)

ComplexType.contentTypeReflect=ctReflect

def attrsReflect(self,parent):
  for au in self.attributeDeclarations.values():
    if isinstance(au.attributeDeclaration,Attribute):
      au.reflect(parent)

ComplexType.attributesReflect=attrsReflect

def agAttrsReflect(self,parent):
  for au in self.attributeDeclarations:
    if isinstance(au.attributeDeclaration,Attribute):
      au.reflect(parent)

AttributeGroup.attributesReflect=agAttrsReflect

def awReflect(self,parent):
#  wc=None
#  for ad in self.attributeDeclarations.values():
#    if isinstance(ad.attributeDeclaration,Wildcard):
#      wc=ad.attributeDeclaration
#      break
  if self.attributeDeclarations.has_key('#any'):
    self.attributeDeclarations['#any'].attributeDeclaration.reflect(parent)

ComplexType.attributeWildcardReflect=awReflect

def agAwReflect(self,parent):
  for au in self.attributeDeclarations:
    if isinstance(au.attributeDeclaration,Wildcard):
      au.attributeDeclaration.reflect(parent)
      return

AttributeGroup.attributeWildcardReflect=agAwReflect

def selReflect(self,parent):
  selp=XMLInfoset.Element(parent,psviSchemaNamespace,'xpath')
  parent.addChild(selp)
  selp.reflectString(selp, 'path',self.selector.str,0)

Kcons.selectorReflect=selReflect

def referReflect(self,parent):
  self.reflectAsPointer(self.refer, parent, 'referencedKey')

Kcons.referReflect=referReflect

def fsReflect(self,parent):
  for f in self.fields:
    xp=XMLInfoset.Element(parent,psviSchemaNamespace,'xpath')
    parent.addChild(xp)
    xp.reflectString(xp, 'path',f.str,0)

Kcons.fieldsReflect=fsReflect

def ptReflect(self,parent):
  if self.primitiveType is not None:
    self.primitiveType.reflectAsPointer(self.primitiveType.name,parent)

SimpleType.primitiveTypeReflect=ptReflect

def facetsReflect(self,parent):
  if self.variety=='atomic':
    auth=self.primitiveType
  elif self.variety=='list':
    auth=List
  elif self.variety=='union':
    auth=Union
  else:
    shouldnt('bogusv: %s'%self.variety)
  for fn in auth.allowedFacets:
    if self.facets.has_key(fn):
      facet=self.facets[fn]
    else:
      facet=None
    if (facet is not None and facet.value is not None):
      fval=facet.value
      if type(fval)==types.ListType:
        if fn=='pattern':               # hack to save megaspace
          if facet.uids is not None:
            # a pointer
            for uid in facet.uids:
              facet.reflectAsPointer(uid,parent)
          else:
            if facet.uids is None:
              facet.id=facet.fid
              facet.assignUid()
              n=1
              facet.uids=[]
              for vl in fval:
                if vl in builtinPats:
                  nuid="bip..%d"%builtinPats.index(vl)
                  facet.reflectAsPointer(nuid,parent)
                else:
                  f=facetReflect(parent,fn,vl)
                  nuid="%s..%d"%(facet.uid,n)
                  idAttr = XMLInfoset.Attribute(f, None, "id", None, nuid)
                  f.addAttribute(idAttr)
                facet.uids.append(nuid)
                n=n+1
        else:
          for vl in fval:
            f=facetReflect(parent,fn,vl)
      else:
        f=facetReflect(parent,fn,fval)
        f.reflectBoolean(f,"fixed",facet.fixed,0)
      if facet.annotation is not None:
        # note hack for list-vals -- annotation on last one
        facet.annotation.reflect(f)

def facetReflect(parent,name,value):
  f=XMLInfoset.Element(parent,psviSchemaNamespace,name)
  parent.addChild(f)
  if value is not None:
    if name=="precision":
      if value:
        value="true"
      else:
        value="false"
    elif name=="lexicalMappings":
      value=" ".join(value)
    elif type(value) not in (types.StringType,types.UnicodeType):
      value=str(value)
    if len(value) > 0:
      if type(value) not in (types.StringType,types.UnicodeType):
        value=str(value)
    f.reflectString(f,"value",value,0)
  return f

SimpleType.facetsReflect=facetsReflect

def fundamentalFacetsReflect(self,parent):
  pass
  # XXX

SimpleType.fundamentalFacetsReflect=fundamentalFacetsReflect

def elementReflect(self, parent=None):
#  sys.stderr.write("using new reflect on %s, %s\n" % (self,parent));
#  sys.stderr.write("%s" % self.__dict__);
  if self.schemaInformation is not None:
    # we are a validation start, so we need an ID _before_ recursion
    self.id=gensym().id                          # for others to point to
    # we need to build all the top-level defns also
    # two passes -- assign names, to avoid internal defn's of named stuff
    assignAllUIDs(self.schemaInformation)
  if self.schemaNormalizedValue:
    mixed=0
  elif self.typeDefinition:
    mixed=self.typeDefinition.contentType=='mixed'
  else:
    mixed=1
  element = self.oldReflect(parent,mixed)

  if self.schemaInformation is not None:
    element.addAttribute(XMLInfoset.Attribute(element, None, "id", None, self.id))
    reflectAllComponents(element,self.schemaInformation)
  self.reflectString(element, "validationAttempted",
                     self.validationAttempted, 1,
                     psviSchemaNamespace)

  if self.validationContext is not None:
    self.reflectString(element,"validationContext",self.validationContext.id,0,
                       psviSchemaNamespace)

  self.reflectString(element, "validity", self.validity, 1,
                     psviSchemaNamespace)

  if self.errorCode:
    self.reflectString(element,
                       "schemaErrorCode",'\n'.join(self.errorCode),1,
                       psviSchemaNamespace)

  self.reflectString(element, "schemaNormalizedValue", self.schemaNormalizedValue, 1,
                     psviSchemaNamespace)

  if self.typeDefinition:         # XXX
    self.typeDefinition.reflect(element)

  self.reflectString(element, "memberTypeDefinition", self.memberTypeDefinition, 1,
                     psviSchemaNamespace)

  if self.elementDeclaration is not None:
    self.elementDeclaration.reflect(parent)

  self.reflectBoolean(element, "nil", self.null, 1,
                       psviSchemaNamespace)

XMLInfoset.Element.psvReflect = elementReflect

class gensym:
  
  nextid = 1

  def __init__(self):
    self.id = "g%s" % gensym.nextid
    gensym.nextid = gensym.nextid + 1

def reflectAllComponents(element,schemaInformation):
  for i in schemaInformation:
    i.reflect(element)

def assignAllUIDs(schemaInformation):
  for i in schemaInformation:
    for c in i.schemaComponents:
      if (isinstance(c,Component) or
          isinstance(c,AbInitio)):
        c.assignUid()


def attributeReflect(self, parent=None):
  attribute = self.oldReflect(parent)

  self.reflectString(attribute, "validationAttempted",
                     self.validationAttempted, 1,
                     psviSchemaNamespace)

  if self.validationContext is not None:
    self.reflectString(attribute,
                       "validationContext",self.validationContext.id,0,
                       psviSchemaNamespace)

  self.reflectString(attribute, "validity", self.validity, 1,
                     psviSchemaNamespace)

  if self.errorCode:
    self.reflectString(attribute,
                       "schemaErrorCode",'\n'.join(self.errorCode),1,
                       psviSchemaNamespace)

  self.reflectString(attribute, "schemaNormalizedValue", self.schemaNormalizedValue, 1,
                     psviSchemaNamespace)

  if self.typeDefinition is not None:         # XXX
    self.typeDefinition.reflect(attribute)

  self.reflectString(attribute, "memberTypeDefinition", self.memberTypeDefinition, 1,
                     psviSchemaNamespace)

  if self.attributeDeclaration is not None:
    self.attributeDeclaration.reflect(attribute)

XMLInfoset.Attribute.psvReflect = attributeReflect

XMLInfoset.Element.oldReflect = XMLInfoset.Element.reflect
XMLInfoset.Element.reflect = XMLInfoset.Element.psvReflect

XMLInfoset.Attribute.oldReflect = XMLInfoset.Attribute.reflect
XMLInfoset.Attribute.reflect = XMLInfoset.Attribute.psvReflect


# $Log: reflect.py,v $
# Revision 1.10  2005-08-10 20:32:08  ht
# comment
#
# Revision 1.9  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.8  2004/08/18 08:44:38  ht
# dump patterns properly
#
# Revision 1.7  2003/04/01 18:46:10  ht
# allow (but ignore) control arg to reflect doc
#
# Revision 1.6  2002/11/25 14:57:33  ht
# get fake variety early
#
# Revision 1.5  2002/10/08 20:32:16  ht
# fix one more XMLInfoset qualification, remove pointless statement
#
# Revision 1.4  2002/09/23 21:45:03  ht
# move to string methods from string library
#
# Revision 1.3  2002/09/23 14:03:14  ht
# fix an attr group dumping bug,
# set up so pattern facets are shared where possible to save on big built-in patterns
#
# Revision 1.2  2002/08/21 08:58:05  ht
# simpleTypeMap hack, attr bug
#
# Revision 1.1  2002/06/28 09:46:07  ht
# part of package now
#
