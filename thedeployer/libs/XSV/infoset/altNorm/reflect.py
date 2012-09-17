"""Alternating normal form: Marshal instances to XML doc in ANF"""

__version__="$Revision: 1.7 $"
# $Id: reflect.py,v 1.7 2004-10-04 11:36:47 ht Exp $

import types

from XSV.infoset import XMLInfoset
from XSV.infoset import PSVInfoset

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
from XSV.compile.Facet import Facet
from XSV.compile.Component import Component
from XSV.compile.AbInitio import AbInitio
from XSV.compile.SimpleType import SimpleType
from XSV.compile.Type import Type

from XSV.compile.SchemaError import shouldnt

from XSV.compile import XMLSchemaNS

xsiNamespace = XMLInfoset.xsiNamespace

# ----------- PSVI reflection ----------------

psviSchemaNamespace = PSVInfoset.psviSchemaNamespace
InformationItem = XMLInfoset.InformationItem
Document = XMLInfoset.Document
Namespace = XMLInfoset.Namespace
Characters = XMLInfoset.Characters
infosetSchemaNamespace = XMLInfoset.infosetSchemaNamespace

def setup():
  SimpleType.reflectedName='simpleTypeDefinition'
  SimpleType.reflectionOutMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('baseTypeDefinition','component',1,'basetype'),
                   ('primitiveTypeDefinition','component',1,'primitiveType'),
                   ('facets','special',0,'facetsReflect'),
                   # XXX
                   ('fundamentalFacets','special',0, 'fundamentalFacetsReflect'),
                   # XXX
                   ('final','list',0,'final'),
                   ('variety','string',0,'variety'),
                   ('itemTypeDefinition','component',1,'itemType'),
                   ('memberTypeDefinitions','components',1,'memberTypes'),
                   ('annotations','components',0,'annotations') # not per REC,
                                                                # but correct
                   )

  del(List.reflectionOutMap)
  del(List.reflectedName)
  del(Union.reflectionOutMap)
  del(Union.reflectedName)
  del(AbInitio.reflectionOutMap)
  del(Key.reflectedName)
  del(Keyref.reflectedName)
  del(Unique.reflectedName)
  AbInitio.reflectedName='simpleTypeDefinition'

  ComplexType.reflectedName='complexTypeDefinition'
  ComplexType.reflectionOutMap=(('name','string',1,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('baseTypeDefinition','component',1,'basetype'),
                   ('derivationMethod','string',1,'derivationMethod'),
                   ('final','list',0,'final'),
                   ('abstract','boolean',0,'abstract'),
                   ('attributeUses','special',0,'attributesReflect'),
                   ('attributeWildcard','special',1,'attributeWildcardReflect'),
                   ('contentType','special',0,'contentTypeReflect'),
                   ('prohibitedSubstitutions','list',
                    0,'prohibitedSubstitutions'),
                   ('annotations','components',0,'annotations'))

  Group.reflectedName='modelGroup'
  Group.reflectionOutMap=(('compositor','string',0,'compositor'),
                   ('particles','components',0,'particles'),
                   ('annotation','component',1,'annotation'))

  Particle.reflectedName='particle'
  Particle.reflectionOutMap=(('minOccurs','string',0,'minOccurs'),
                   ('maxOccurs','string',0,'maxOccurs'),
                   ('minOccurs','special',0,'occursReflect'), # hack,
                                                              # for rebuild only
                   ('term','component',1,'term'))

  Wildcard.reflectedName='wildcard'
  Wildcard.reflectionOutMap=(('namespaceConstraint','special',
                    0,'wildcardNamespaceReflect'),
                   ('processContents','string',0,'processContents'),
                   ('annotation','component',1,'annotation'))

  Element.reflectedName='elementDeclaration'
  Element.reflectionOutMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('typeDefinition','component',1,'typeDefinition'),
                   ('scope','special',1,'scopeReflect'),
                   ('valueConstraint','special',1,'vcReflect'),
                   ('nillable','boolean',0,'nullable'),
                   ('identityConstraintDefinitions','special',
                    0,'icsReflect'),
                   ('substitutionGroupAffiliation','component',1,'equivalenceClassAffiliation'),
                   ('substitutionGroupExclusions','list',0,'final'),
                   ('disallowedSubstitutions','list',
                    0,'prohibitedSubstitutions'),
                   ('abstract','boolean',0,'abstract'),
                   ('annotation','component',1,'annotation'))

  AttributeUse.reflectedName='attributeUse'
  AttributeUse.reflectionOutMap=(('required','boolean',0,'minOccurs'),
                   ('attributeDeclaration','component',1,'attributeDeclaration'),
                   ('valueConstraint','special',1,'vcReflect'))

  Attribute.reflectedName='attributeDeclaration'
  Attribute.reflectionOutMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('typeDefinition','component',1,'typeDefinition'),
                   ('scope','special',1,'scopeReflect'),
                   ('valueConstraint','special',1,'vcReflect'),
                   ('annotation','component',1,'annotation'))

  AttributeGroup.reflectedName='attributeGroupDefinition'
  AttributeGroup.reflectionOutMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('attributeUses','components',0, 'attributeDeclarations'),
                   ('attributeWildcard', 'component', 1, 'dummy'), # XXX not done
                   ('annotation','component',1,'annotation'))

  ModelGroup.reflectedName='modelGroupDefinition'
  ModelGroup.reflectionOutMap=(('name','string',0,'name'),
                           ('targetNamespace','string',1,'targetNamespace'),
                           ('annotation','component',1,'annotation'),
                           ('modelGroup','special',0,'mgReflect'))

  Kcons.reflectedName='identityConstraintDefinition'
  Kcons.reflectionOutMap=(('name','string',0,'name'),
                   ('targetNamespace','string',1,'targetNamespace'),
                   ('identityConstraintCategory','string',0,'cname'),
                   ('selector','special',0,'selectorReflect'),
                   ('fields','special',0,'fieldsReflect'),
                   ('referencedKey','component',1,'refer'),
                   ('annotation','component',1,'annotation'))

  AnyAttribute.reflectedName='wildcard'


  Annotation.reflectedName='annotation'
  Annotation.reflectionOutMap=(('applicationInformation','components',0,'appinfo'),
                   ('userInformation','components',0,'documentation'),
                   ('attributes','components',0,'attrs'))



  Facet.reflectionOutMap=None

def nsiReflect(self, parent=None):

  nsi = XMLInfoset.Element(parent, psviSchemaNamespace, "namespaceSchemaInformation")
  self.reflectString(nsi, "schemaNamespace", self.schemaNamespace, 1,
                     psviSchemaNamespace)

  comps = XMLInfoset.Element(nsi, psviSchemaNamespace, "schemaComponents")
  nsi.addChild(comps)

  for c in self.schemaComponents:
    comps.addChild(c.reflect(comps,1))

  docs = XMLInfoset.Element(nsi, psviSchemaNamespace, "schemaDocuments")
  nsi.addChild(docs)

  for d in self.schemaDocuments:
    docs.addChild(d.reflect(docs))

  annots = XMLInfoset.Element(nsi, psviSchemaNamespace, "schemaAnnotations")
  nsi.addChild(annots)

  for a in self.schemaAnnotations:
    annots.addChild(a.reflect(annots))

  return nsi

PSVInfoset.NamespaceSchemaInformation.reflect=nsiReflect

def sdReflect(self, parent=None):
  sd = XMLInfoset.Element(parent, psviSchemaNamespace, "schemaDocument")
  self.reflectString(sd, "documentLocation", self.documentLocation, 1,
                     psviSchemaNamespace)
  self.reflectNull(sd, "document",
                     psviSchemaNamespace)
  return sd

PSVInfoset.schemaDocument.reflect=sdReflect

def componentReflect(self,parent,forceFull=0,noID=0):
#  print ('cr',self,self.uid,forceFull,noID)
#  if hasattr(self,'name'):
#    print ('crn',self.name)
  if self.uid and not forceFull:
    # a pointer
#    print ('ptr',self.uid)
    return self.reflectAsPointer(self.uid,parent)
  else:
    e = XMLInfoset.Element(parent, psviSchemaNamespace, self.reflectedName)
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
                        rme[2],psviSchemaNamespace)
      elif rme[1]=='list':
        rel=XMLInfoset.Element(e,psviSchemaNamespace,rme[0])
        e.addChild(rel)
        if len(value)>0:
          rel.addChild(Characters(e,' '.join(value)))
      elif rme[1]=='boolean':
        if str(value) not in ('true','false'):
          if value:
            value='true'
          else:
            value='false'
        e.reflectString(e,rme[0],value,
                        rme[2],psviSchemaNamespace)
      elif rme[1]=='component':
        if value:
          rel=XMLInfoset.Element(e,psviSchemaNamespace,rme[0])
          e.addChild(rel)
          rel.addChild(value.reflect(rel))
        elif rme[2]:
          if rme[2]==1:
            e.reflectNull(e,rme[0],psviSchemaNamespace)
      elif rme[1]=='namedComponent':
        if value:
          if value.uid:
            e.addChild(value.reflectAsPointer(value.uid,e))
          else:
            # if no uid then must be anon, no point naming
            e.addChild(value.reflect(e))
        elif rme[2]:
          e.reflectNull(e,rme[0],psviSchemaNamespace)
      elif rme[1]=='special':
        value(e)
      elif rme[1]=='components':
        if value==None and rme[2]:
          e.reflectNull(e,rme[0],psviSchemaNamespace)
          continue
        rel=XMLInfoset.Element(e,psviSchemaNamespace,rme[0])
        e.addChild(rel)
        for vv in value or []:
          rel.addChild(vv.reflect(rel))
#    print ('dcr',self)
    return e 

def reflectAsPtr(self,ref,parent,name,eltName,relns=psviSchemaNamespace,
                 eltns=psviSchemaNamespace):
  if name is not None:
    e = XMLInfoset.Element(parent, relns, name)
    parent.addChild(e)
    parent=e
  c = XMLInfoset.Element(parent, eltns, eltName)
  if name:
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
  return c

def reflectAIAsPointer(self,ref,parent,name=None):
  return reflectAsPtr(self,ref,parent,name,"simpleTypeDefinition")

def reflectCompAsPointer(self, ref, parent,name=None):
  return reflectAsPtr(self,ref,parent,name,self.reflectedName)

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
Attribute.alwaysNamed=1
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
  res=Component.reflect(self,parent,forceFull,noID)
  if tick:
    self.reflectedName='modelGroupDefinition'
  return res
    
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
# Notation.kind='ntn'

def abInitioReflect(self,parent,force=0):
  if not force:
    # a pointer
    return self.reflectAsPointer(self.name,parent)
  else:
    self.uid=self.name
    e = XMLInfoset.Element(parent, psviSchemaNamespace, 'simpleTypeDefinition')
    idAttr = XMLInfoset.Attribute(e, None, "id", None, self.uid)
    e.addAttribute(idAttr)
    nullAttr = XMLInfoset.Attribute(e, xsiNamespace, "nil", None, "true")
    e.addAttribute(nullAttr)
    return e

AbInitio.reflect=abInitioReflect
AbInitio.uid=None

def scopeReflect(self,parent):
  if self.scope:
    se=XMLInfoset.Element(parent,psviSchemaNamespace,"scope")
    parent.addChild(se)
    if self.scope=='global':
      se.addChild(Characters(se, 'global'))
    else:
      se.addChild(self.scope.reflect(self))
  else:
    parent.reflectNull(parent,'scope',psviSchemaNamespace)

Element.scopeReflect=scopeReflect
Attribute.scopeReflect=scopeReflect

def vcReflect(self,parent):
  if self.valueConstraint:
    vc=XMLInfoset.Element(parent,psviSchemaNamespace,'valueConstraint')
    parent.addChild(vc)
    parent=vc
    vc=XMLInfoset.Element(parent,psviSchemaNamespace,'valueConstraint')
    parent.addChild(vc)
    vc.reflectString(vc,'variety',self.valueConstraint[0],
                     1,psviSchemaNamespace)
    vc.reflectString(vc,'value',self.valueConstraint[1],
                     0,psviSchemaNamespace)
  else:
    parent.reflectNull(parent,'valueConstraint',psviSchemaNamespace)

Element.vcReflect=vcReflect
Attribute.vcReflect=vcReflect
AttributeUse.vcReflect=vcReflect

def icsReflect(self,parent):
  rel=XMLInfoset.Element(parent,psviSchemaNamespace,'identityConstraintDefinitions')
  parent.addChild(rel)
  for kd in self.keys:
    rel.addChild(kd.reflect(rel))
  for ud in self.uniques:
    rel.addChild(ud.reflect(rel))
  for krd in self.keyrefs:
    rel.addChild(krd.reflect(rel))

Element.icsReflect=icsReflect

def KTEntryReflect(self,parent,table):
  kte=XMLInfoset.Element(parent,psviSchemaNamespace,
                         'identityConstraintBinding')
  parent.addChild(kte)
  dfn=XMLInfoset.Element(kte,psviSchemaNamespace,
                         'definition')
  kte.addChild(dfn)
  dfn.addChild(self.reflect(dfn))     # should always be a pointer
  nodeTab=XMLInfoset.Element(kte,psviSchemaNamespace,
                             'nodeTable') # property
  kte.addChild(nodeTab)
  ndTb=XMLInfoset.Element(nodeTab,psviSchemaNamespace,
                          'nodeTable') # thing itself
  nodeTab.addChild(ndTb)
  for (n,v) in table.items():
    ndTb.reflectValue(ndTb,"key",n,0)
    reflectAsPtr(v,v.id,ndTb,"value","element",psviSchemaNamespace
                 ,infosetSchemaNamespace)

Kcons.KTEntryReflect=KTEntryReflect

def adReflect(self,parent):
  tab={}
  for ad in self.attributeDeclarations:
    ad.expand(tab)
  rel=XMLInfoset.Element(parent,psviSchemaNamespace,'attributeDeclarations')
  parent.addChild(rel)
  for vv in tab.values():
    rel.addChild(vv.reflect(rel))

AttributeGroup.adReflect=adReflect

def mgReflect(self,parent):
  rel=XMLInfoset.Element(parent,psviSchemaNamespace,'modelGroup')
  # we've been done as an mgd, now let the class defaults through to get
  # us done as an mg
  parent.addChild(rel)
  self.reflectionOutMap=Group.reflectionOutMap
  self.reflectedName='modelGroup'
  name=self.name                        # stop recursion
  self.name=None
  rel.addChild(self.reflect(rel,1,1))
  self.name=name

Group.mgReflect=mgReflect

def wnsReflect(self,parent):
  ns=XMLInfoset.Element(parent,psviSchemaNamespace,'namespaceConstraint')
  parent.addChild(ns)
  parent=ns
  ns=XMLInfoset.Element(parent,psviSchemaNamespace,'namespaceConstraint')
  parent.addChild(ns)
  if self.allowed=='##any':
    ns.reflectString(ns, 'variety', 'any', 0, psviSchemaNamespace)
    ns.reflectNull(ns, 'namespaces', psviSchemaNamespace)
  else:
    if self.negated:
      ns.reflectString(ns, 'variety', 'negative', 0, psviSchemaNamespace)
    else:
      ns.reflectString(ns, 'variety', 'positive', 0, psviSchemaNamespace)
    nss = XMLInfoset.Element(ns, psviSchemaNamespace, 'namespaces')
    ns.addChild(nss)
    first=1
    for nn in self.namespaces:
      if first:
        first=0
      else:
        nss.addChild(Characters(nss, ' '))
      if nn:
        nss.addChild(Characters(nss, nn))
      else:
        nss.addChild(Characters(nss, '##none'))

Wildcard.wildcardNamespaceReflect=wnsReflect

def ctReflect(self,parent):
  if self.contentType:
    ct=XMLInfoset.Element(parent,psviSchemaNamespace,'contentType')
    parent.addChild(ct)
    parent=ct
    ct=XMLInfoset.Element(parent,psviSchemaNamespace,'contentType')
    parent.addChild(ct)
    if self.contentType=='empty':
      ct.reflectString(ct, 'variety','empty',0,psviSchemaNamespace)
      ct.reflectNull(ct,'simpleTypeDefinition',psviSchemaNamespace)
      ct.reflectNull(ct,'particle',psviSchemaNamespace)
    elif self.contentType in ('elementOnly','mixed'):
      ct.reflectString(ct, 'variety',self.contentType,0,psviSchemaNamespace)
      ct.reflectNull(ct,'simpleTypeDefinition',psviSchemaNamespace)
      particle=XMLInfoset.Element(ct, psviSchemaNamespace, 'particle')
      ct.addChild(particle)
      particle.addChild(self.model.reflect(particle))
    else:
      ct.reflectString(ct, 'variety','simple',0,psviSchemaNamespace)
      st=XMLInfoset.Element(ct, psviSchemaNamespace, 'simpleTypeDefinition')
      ct.addChild(st)
      st.addChild(self.model.reflect(st))
      ct.reflectNull(ct,'particle',psviSchemaNamespace)
  else:
    parent.reflectNull(parent,'contentType',psviSchemaNamespace)

ComplexType.contentTypeReflect=ctReflect

def attrsReflect(self,parent):
  rel=XMLInfoset.Element(parent,psviSchemaNamespace,'attributeUses')
  parent.addChild(rel)
  for au in self.attributeDeclarations.values():
    if isinstance(au.attributeDeclaration,Attribute):
      rel.addChild(au.reflect(rel))

ComplexType.attributesReflect=attrsReflect

def awReflect(self,parent):
  wc=None
  for ad in self.attributeDeclarations.values():
    if isinstance(ad.attributeDeclaration,Wildcard):
      wc=ad.attributeDeclaration
      break
  if wc:
    wcp=XMLInfoset.Element(parent,psviSchemaNamespace,'attributeWildcard')
    parent.addChild(wcp)
    wcp.addChild(wc.reflect(wcp))
  else:
    parent.reflectNull(parent,'attributeWildcard',psviSchemaNamespace)

ComplexType.attributeWildcardReflect=awReflect

def selReflect(self,parent):
  selp=XMLInfoset.Element(parent,psviSchemaNamespace,'selector')
  parent.addChild(selp)
  parent=selp
  selp=XMLInfoset.Element(parent,psviSchemaNamespace,'xpath')
  parent.addChild(selp)
  selp.reflectString(selp, 'path',self.selector.str,0,psviSchemaNamespace)

Kcons.selectorReflect=selReflect

def referReflect(self,parent):
  self.reflectAsPointer(self.refer, parent, 'referencedKey')

Kcons.referReflect=referReflect


def fsReflect(self,parent):
  fsp=XMLInfoset.Element(parent,psviSchemaNamespace,'fields')
  parent.addChild(fsp)
  for f in self.fields:
    xp=XMLInfoset.Element(parent,psviSchemaNamespace,'xpath')
    fsp.addChild(xp)
    xp.reflectString(xp, 'path',f.str,0,psviSchemaNamespace)

Kcons.fieldsReflect=fsReflect

def ptReflect(self,parent):
  if self.primitiveType:
    self.primitiveType.reflectAsPointer(self.primitiveType.name,parent,
                                        'primitiveTypeDefinition')
  else:
    parent.reflectNull(parent,'primitiveTypeDefinition',psviSchemaNamespace)

SimpleType.primitiveTypeReflect=ptReflect

def facetsReflect(self,parent):
  ff=XMLInfoset.Element(parent,psviSchemaNamespace,"facets")
  parent.addChild(ff)
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
      f=XMLInfoset.Element(ff,psviSchemaNamespace,fn)
      ff.addChild(f)
      if type(fval)==types.ListType:
        for vl in fval:
          f.reflectValue(f,"value",vl,0)
      else:
        f.reflectValue(f,"value",fval,0)
      f.reflectBoolean(f,"fixed",facet.fixed,0,psviSchemaNamespace)
      if facet.annotation:
          rel=XMLInfoset.Element(f,psviSchemaNamespace,'annotation')
          f.addChild(rel)
          rel.addChild(facet.annotation.reflect(rel))
      else:
        f.reflectNull(f,'annotation',psviSchemaNamespace)

SimpleType.facetsReflect=facetsReflect

def fundamentalFacetsReflect(self,parent):
  ff=XMLInfoset.Element(parent,psviSchemaNamespace,"fundamentalFacets")
  parent.addChild(ff)
  # XXX

SimpleType.fundamentalFacetsReflect=fundamentalFacetsReflect

def finalReflect(self,parent):
  ff=XMLInfoset.Element(parent,psviSchemaNamespace,"final")
  parent.addChild(ff)
  # Don't understand why this was here . . . now bypassed by 'list' in map

SimpleType.finalReflect=finalReflect

def elementReflect(self, parent=None):
#  sys.stderr.write("using new reflect on %s, %s\n" % (self,parent));
#  sys.stderr.write("%s" % self.__dict__);
  if self.schemaInformation or self.hasKey:
    # we are a validation start, or keyed, so we need an ID _before_ recursion
    self.id=gensym().id                          # for others to point to
  if self.schemaInformation:
    # we need to build all the top-level defns also
    info = reflectSchemaInfo(self.schemaInformation,self.reflectSchemaControl)

  element = self.oldReflect(parent,not self.schemaNormalizedValue)

  if self.schemaInformation or self.hasKey:
    element.addAttribute(XMLInfoset.Attribute(element, None, "id", None, self.id))
  if self.schemaInformation and info is not None:
    element.addChild(info)
    info.parent=element
  else:
    self.reflectNull(element, "schemaInformation", psviSchemaNamespace)

  self.reflectString(element, "validationAttempted",
                     self.validationAttempted, 1,
                       psviSchemaNamespace)

  if self.validationContext:
    reflectAsPtr(self,self.validationContext.id,element,
                 "validationContext","element",psviSchemaNamespace,
                 infosetSchemaNamespace)
  else:
    self.reflectNull(element,"validationContext",psviSchemaNamespace)

  self.reflectString(element, "validity", self.validity, 1,
                       psviSchemaNamespace)

  errorCode = XMLInfoset.Element(element, psviSchemaNamespace, "schemaErrorCode")
  element.addChild(errorCode)
  if self.errorCode:
    for err in self.errorCode:
      errorCode.addChild(Characters(errorCode, err))
  else:
    nullAttr = XMLInfoset.Attribute(errorCode, xsiNamespace, "nil", None, "true")
    errorCode.addAttribute(nullAttr)

  self.reflectString(element, "schemaNormalizedValue", self.schemaNormalizedValue, 1,
                       psviSchemaNamespace)

  self.reflectNull(element, "schemaSpecified", psviSchemaNamespace) # XXX
  
  if self.typeDefinition:         # XXX
    typeDefinition = XMLInfoset.Element(element, psviSchemaNamespace, "typeDefinition")
    element.addChild(typeDefinition)
    typeDefinition.addChild(self.typeDefinition.reflect(typeDefinition))
  else:
    self.reflectNull(element, "typeDefinition",
                       psviSchemaNamespace)

  self.reflectString(element, "memberTypeDefinition", self.memberTypeDefinition, 1,
                       psviSchemaNamespace)

#    self.reflectString(element, "typeDefinitionType", self.typeDefinitionType, 1)

#    self.reflectString(element, "typeDefinitionNamespace",
#                       self.typeDefinitionNamespace, 1,
#                       psviSchemaNamespace)

#    self.reflectBoolean(element, "typeDefinitionAnonymous",
#                        self.typeDefinitionAnonymous, 1,
#                       psviSchemaNamespace)

#    self.reflectString(element, "typeDefinitionName", self.typeDefinitionName, 1,
#                       psviSchemaNamespace)

#    self.reflectString(element, "memberTypeDefinitionNamespace",
#                       self.memberTypeDefinitionNamespace, 1,
#                       psviSchemaNamespace)

#    self.reflectBoolean(element, "memberTypeDefinitionAnonymous",
#                        self.memberTypeDefinitionAnonymous, 1,
#                       psviSchemaNamespace)

#    self.reflectString(element, "memberTypeDefinitionName",
#                       self.memberTypeDefinitionName, 1,
#                       psviSchemaNamespace)

  if self.elementDeclaration:
    ee = XMLInfoset.Element(element, psviSchemaNamespace, "declaration")
    element.addChild(ee)
    ee.addChild(self.elementDeclaration.reflect(ee))
  else:
    self.reflectNull(element, "declaration",
                       psviSchemaNamespace)

  self.reflectBoolean(element, "nil", self.null, 1,
                       psviSchemaNamespace)


  self.reflectNull(element, "notation", psviSchemaNamespace) # XXX
  self.reflectNull(element, "idIdrefTable", psviSchemaNamespace) # XXX
  if self.keyTabs:
    ee = XMLInfoset.Element(element, psviSchemaNamespace,
                            "identityConstraintTable")
    element.addChild(ee)
    for (key,table) in self.keyTabs.items():
      key.KTEntryReflect(ee,table)
  else:
    self.reflectNull(element, "identityConstraintTable", psviSchemaNamespace)
  return element

XMLInfoset.Element.psvReflect = elementReflect
XMLInfoset.Element.hasKey = 0

def reflectSchemaInfo(schemaInformation,labelOnly=0):
  # two passes -- assign names, to avoid internal defn's of named stuff
  for i in schemaInformation:
    for c in i.schemaComponents:
      if isinstance(c,Component):
        c.assignUid()
  if labelOnly==2:
    return
  info=XMLInfoset.Element(None, psviSchemaNamespace, "schemaInformation")
  for i in schemaInformation:
    if labelOnly!=1 or i.schemaNamespace!=XMLSchemaNS:
      info.addChild(i.reflect(info))
  return info

class gensym:
  
  nextid = 1

  def __init__(self):
    self.id = "g%s" % gensym.nextid
    gensym.nextid = gensym.nextid + 1

def attributeReflect(self, parent=None):
#  sys.stderr.write("using new reflect on %s, %s\n" % (self,parent));
#  sys.stderr.write("%s" % self.__dict__);
  attribute = self.oldReflect(parent)

  self.reflectString(attribute, "validationAttempted",
                     self.validationAttempted, 1,
                       psviSchemaNamespace)

  if self.validationContext:
    reflectAsPtr(self,self.validationContext.id, attribute,
                 "validationContext","element",psviSchemaNamespace,
                 infosetSchemaNamespace)
  else:
    self.reflectNull(attribute,"validationContext",psviSchemaNamespace)

  self.reflectString(attribute, "validity", self.validity, 1,
                       psviSchemaNamespace)

  errorCode = XMLInfoset.Element(attribute, psviSchemaNamespace, "schemaErrorCode")
  attribute.addChild(errorCode)
  if self.errorCode:
    for err in self.errorCode:
      errorCode.addChild(Characters(errorCode, err))
  else:
    nullAttr = XMLInfoset.Attribute(errorCode, xsiNamespace, "nil", None, "true")
    errorCode.addAttribute(nullAttr)

  self.reflectString(attribute, "schemaNormalizedValue", self.schemaNormalizedValue, 1,
                       psviSchemaNamespace)

  self.reflectNull(attribute, "schemaSpecified", psviSchemaNamespace) # XXX
  
  if self.typeDefinition:         # XXX
    typeDefinition = XMLInfoset.Element(attribute,
                             psviSchemaNamespace, "typeDefinition")
    attribute.addChild(typeDefinition)
    typeDefinition.addChild(self.typeDefinition.reflect(typeDefinition))
  else:
    self.reflectNull(attribute, "typeDefinition",
                       psviSchemaNamespace)

  self.reflectString(attribute, "memberTypeDefinition", self.memberTypeDefinition, 1,
                       psviSchemaNamespace)

#    self.reflectString(attribute, "typeDefinitionType", self.typeDefinitionType, 1,
#                       psviSchemaNamespace)

#    self.reflectString(attribute, "typeDefinitionNamespace",
#                       self.typeDefinitionNamespace, 1,
#                       psviSchemaNamespace)

#    self.reflectBoolean(attribute, "typeDefinitionAnonymous",
#                        self.typeDefinitionAnonymous, 1,
#                       psviSchemaNamespace)

#    self.reflectString(attribute, "typeDefinitionName", self.typeDefinitionName, 1,
#                       psviSchemaNamespace)

#    self.reflectString(attribute, "memberTypeDefinitionNamespace",
#                       self.memberTypeDefinitionNamespace, 1,
#                       psviSchemaNamespace)

#    self.reflectBoolean(attribute, "memberTypeDefinitionAnonymous",
#                        self.memberTypeDefinitionAnonymous, 1,
#                       psviSchemaNamespace)

#    self.reflectString(attribute, "memberTypeDefinitionName",
#                       self.memberTypeDefinitionName, 1,
#                       psviSchemaNamespace)

  if self.attributeDeclaration:
    aa = XMLInfoset.Element(attribute, psviSchemaNamespace, "declaration")
    attribute.addChild(aa)
    aa.addChild(self.attributeDeclaration.reflect(aa))
  else:
    self.reflectNull(attribute, "declaration",
                       psviSchemaNamespace)

  return attribute

XMLInfoset.Attribute.psvReflect = attributeReflect

def reflectValue(self, parent, name, value, nullable):
  if nullable and value == None:
    return self.reflectNull(parent, name, None) # None was ns???
  else:
    e = XMLInfoset.Element(parent, psviSchemaNamespace, name)
    parent.addChild(e)
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
      e.addChild(Characters(e, value))
    return e

XMLInfoset.Element.reflectValue=reflectValue

# ----------- vanilla reflection ------------

def InformationItemReflect(self, parent=None):
  return XMLInfoset.Element(parent, infosetSchemaNamespace, "XXX")

InformationItem.reflect=InformationItemReflect


def InformationItemReflectString(self, parent, name, value, nullable, ns=None):
#    sys.stderr.write("reflecting string %s, nullable=%s\n" % (value, nullable))
  if nullable and value == None:
    return self.reflectNull(parent, name, ns)
  else:
    e = XMLInfoset.Element(parent, ns or infosetSchemaNamespace, name)
    parent.addChild(e)
    if len(value) > 0:
      e.addChild(Characters(e, value))
    return e

InformationItem.reflectString=InformationItemReflectString


def InformationItemReflectNull(self, parent, name, ns=None):
  e = XMLInfoset.Element(parent, ns or infosetSchemaNamespace, name)
  parent.addChild(e)
  nullAttr = XMLInfoset.Attribute(e, xsiNamespace, "nil", None, "true")
  e.addAttribute(nullAttr)

InformationItem.reflectNull=InformationItemReflectNull


def InformationItemReflectBoolean(self, parent, name, value, nullable, ns=None):
#    sys.stderr.write("reflecting boolean %s, nullable=%s\n" % (value, nullable))
  if value != None:
    if value:
      value = "true"
    else:
      value = "false"
  return self.reflectString(parent, name, value, nullable, ns)

InformationItem.reflectBoolean=InformationItemReflectBoolean


def DocumentReflect(self, parent=None, reflectSchemaControl=0):

  doc = Document(None, None, "yes")

  document = XMLInfoset.Element(doc, infosetSchemaNamespace, "document", None, None,
                     {None:Namespace(None, infosetSchemaNamespace),
                      "xsi":Namespace("xsi", xsiNamespace),
                      "xml":Namespace("xml",
                                      "http://www.w3.org/XML/1998/namespace")})
  doc.addChild(document)

  children = XMLInfoset.Element(document, infosetSchemaNamespace, "children")
  document.addChild(children)

  for c in self.children:
    c.reflectSchemaControl=reflectSchemaControl
    cc = c.reflect(children)
    if isinstance(cc, InformationItem):
      children.addChild(cc)
    elif cc is not None:
      for ccc in cc:
        children.addChild(ccc)

#    docel =  Element(document, infosetSchemaNamespace, "documentElement")
#    document.addChild(docel)
#    XXX
  self.reflectString(document, "documentElement", None, 1) # fix me

  notations = XMLInfoset.Element(document, infosetSchemaNamespace, "notations")
  document.addChild(notations)
  for n in self.notations:
    nn = n.reflect(notations)
    notations.addChild(nn)

  unparsed = XMLInfoset.Element(document,
                                infosetSchemaNamespace, "unparsedEntities")
  document.addChild(unparsed)
  for e in self.unparsedEntities:
    ee = e.reflect(unparsed)
    unparsed.addChild(ee)

  self.reflectString(document, "baseURI", self.baseURI, 1)

  self.reflectString(document, "characterEncodingScheme", self.characterEncodingScheme, 1)

  self.reflectString(document, "standalone", self.standalone, 1)

  self.reflectString(document, "version", self.version, 1)

  self.reflectBoolean(document, "allDeclarationsProcessed", self.allDeclarationsProcessed, 0)

  return doc

Document.reflect=DocumentReflect


def ElementReflect(self, parent=None, dumpChars=1):

  element = XMLInfoset.Element(parent, infosetSchemaNamespace, "element")

  self.reflectString(element, "namespaceName", self.namespaceName, 1)

  self.reflectString(element, "localName", self.localName, 0)

  self.reflectString(element, "prefix", self.prefix, 1)

  children = XMLInfoset.Element(element, infosetSchemaNamespace, "children")
  element.addChild(children)

  for c in self.children:
    if (not dumpChars) and isinstance(c,Characters):
      continue
    cc = c.reflect(children)
    if isinstance(cc, InformationItem):
      children.addChild(cc)
    elif cc is not None:
      for ccc in cc:
        children.addChild(ccc)

  attributes = XMLInfoset.Element(element, infosetSchemaNamespace, "attributes")
  element.addChild(attributes)

  for a in self.attributes.values():
    aa = a.reflect(attributes)
    attributes.addChild(aa)

  namespaceAttributes = XMLInfoset.Element(element, infosetSchemaNamespace,
                           "namespaceAttributes")
  element.addChild(namespaceAttributes)

  if self.namespaceAttributes:
    for a in self.namespaceAttributes.values():
      aa = a.reflect(namespaceAttributes)
      namespaceAttributes.addChild(aa)

  inScopeNamespaces = XMLInfoset.Element(element, infosetSchemaNamespace,
                           "inScopeNamespaces")
  element.addChild(inScopeNamespaces)

  if self.inScopeNamespaces:
    for a in self.inScopeNamespaces.values():
      aa = a.reflect(inScopeNamespaces)
      inScopeNamespaces.addChild(aa)

  self.reflectString(element, "baseURI", self.baseURI, 1)

  return element

XMLInfoset.Element.reflect=ElementReflect


def CharactersReflect(self, parent=None):
#    print "reflecting chars %s" % self.characters
  clist = []
  for char in self.characters:

    c = XMLInfoset.Element(parent, infosetSchemaNamespace, "character")
    clist.append(c)

    self.reflectString(c, "characterCode", "%s" % ord(char), 0)

    self.reflectBoolean(c, "elementContentWhitespace",
                       self.elementContentWhitespace, 0)

  return clist

Characters.reflect=CharactersReflect


def AttributeReflect(self, parent=None):
  attribute = XMLInfoset.Element(parent, infosetSchemaNamespace, "attribute")

  self.reflectString(attribute, "namespaceName", self.namespaceName, 1)

  self.reflectString(attribute, "localName", self.localName, 0)

  self.reflectString(attribute, "prefix", self.prefix, 1)

  self.reflectString(attribute, "normalizedValue", self.normalizedValue, 1)

  self.reflectBoolean(attribute, "specified", self.specified, 0)

  self.reflectString(attribute, "attributeType", self.attributeType, 1)

  self.reflectString(attribute, "references", None, 1) # not implemented

  return attribute

XMLInfoset.Attribute.reflect=AttributeReflect


def NamespaceReflect(self, parent=None):
  namespace = XMLInfoset.Element(parent, infosetSchemaNamespace, "namespace")

  self.reflectString(namespace, "prefix", self.prefix, 1)

  self.reflectString(namespace, "namespaceName",
                     self.namespaceName, 0)

  return namespace

Namespace.reflect=NamespaceReflect

XMLInfoset.Element.oldReflect = XMLInfoset.Element.reflect
XMLInfoset.Element.reflect = XMLInfoset.Element.psvReflect

XMLInfoset.Attribute.oldReflect = XMLInfoset.Attribute.reflect
XMLInfoset.Attribute.reflect = XMLInfoset.Attribute.psvReflect

# $Log: reflect.py,v $
# Revision 1.7  2004-10-04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.6  2003/03/30 20:05:46  ht
# give command-line control over amount of schema material reflected
#
# Revision 1.5  2003/03/30 18:17:07  ht
# add support for (alternating) reflection of key tables
#
# Revision 1.4  2002/10/08 20:30:33  ht
# minor uba fixed?
#
# Revision 1.3  2002/09/23 21:45:03  ht
# move to string methods from string library
#
# Revision 1.2  2002/08/21 08:57:09  ht
# reorder and change module level and get working
#
# Revision 1.1  2002/06/28 09:46:26  ht
# part of package now
#
