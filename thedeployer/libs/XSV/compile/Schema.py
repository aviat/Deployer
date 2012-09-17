"""Schema compilation: Schema component"""

__version__="$Revision: 1.12 $"
# $Id: Schema.py,v 1.12 2007-02-16 15:49:34 ht Exp $

from VMapping import VMapping

from Facet import Whitespace
from NumFacet import MinLength
from Type import Type
from QName import QName
from Particle import Particle
from Wildcard import AnyAny
from AttributeUse import AttributeUse

from elts.simpleTypeElt import simpleTypeElt
from elts.rulElt import restrictionElt, listElt
from elts.attributeElt import attributeElt
from elts.attributeGroupElt import attributeGroupElt

from XSV.compile import XMLSchemaNS
from XSV.compile import abInitioTypes, builtinTypeNames, builtinLists

from SchemaError import shouldnt, where

_instanceAttrs=[('nil','boolean'),('type','QName'),
               ('noNamespaceSchemaLocation','anyURI')]

_instanceLists=[('schemaLocation','anyURI')]

class Schema:
  annotations=[]
  buggy=0
  prepared=0
  errors=0
  elementFormDefault=attributeFormDefault=finalDefault=blockDefault=None
  def __init__(self,sschema,xrpr):
    # note that unlike other components, this one is built _before_ processing
    # the children of the elt it corresponds to
    self.xrpr=xrpr
    self.sschema=sschema
    self.errors=0
    self.locations=[]
    if xrpr is not None:
      # these are needed during schema accumulation
      self.maybeSetVar('targetNS','targetNamespace',None)
      self.maybeSetVar('elementFormDefault','elementFormDefault','unqualified')
      self.maybeSetVar('attributeFormDefault','attributeFormDefault',
                       'unqualified')
      self.maybeSetVar('finalDefault','finalDefault','')
      self.maybeSetVar('blockDefault','blockDefault','')
      if self.targetNS=="":
        self.error("Empty string is not allowed as value of targetNamespace",
                   xrpr.elt)
        self.targetNS=None
      if (sschema.processingInclude and
          self.targetNS!=sschema.targetNS and
          (not self.targetNS)):
          # chameleon include, OK
          self.targetNS=sschema.targetNS
          sschema.processingInclude=2
      sschema.targetNS=self.targetNS
      if sschema.schemas.has_key(self.targetNS):
        shouldnt('oldcopy')
        oldSchema=sschema.schemas[self.targetNS]
        # use real tables, we're ephemeral
        self.locations=oldSchema.locations       # broken
        sschema.current=oldSchema
        self.typeTable=oldSchema.typeTable
        self.elementTable=oldSchema.elementTable
        self.attributeTable=oldSchema.attributeTable
        self.groupTable=oldSchema.groupTable
        self.attributeGroupTable=oldSchema.attributeGroupTable
        self.vTypeTable=oldSchema.vTypeTable
        self.vElementTable=oldSchema.vElementTable
        self.vAttributeTable=oldSchema.vAttributeTable
        self.vGroupTable=oldSchema.vGroupTable
        self.vAttributeGroupTable=oldSchema.vAttributeGroupTable
        # copy defaults (they've been saved, will be restored)
        oldSchema.elementFormDefault=self.elementFormDefault
        oldSchema.attributeFormDefault=self.attributeFormDefault
        oldSchema.blockDefault=self.blockDefault
        oldSchema.finalDefault=self.finalDefault
        return
      else:
        sschema.schemas[self.targetNS]=self      
        sschema.current=self
    # either we're the first for this NS, or we're the FIRST
    self.typeTable={}
    self.elementTable={}
    self.attributeTable={}
    self.groupTable={}
    self.attributeGroupTable={}
    self.keyUniqueTable={}
    self.vTypeTable=VMapping(self, "typeTable")
    self.vElementTable=VMapping(self, "elementTable")
    self.vAttributeTable=VMapping(self, "attributeTable")
    self.vGroupTable=VMapping(self, "groupTable")
    self.vKeyUniqueTable=VMapping(self, "keyUniqueTable")
    self.vAttributeGroupTable=VMapping(self, "attributeGroupTable")
  
  def __unicode__(self):
    types=map(str,self.typeTable.values())
    groups=map(str, self.groupTable.values())
    attributeGroups=map(str, self.attributeGroupTable.values())
    elts=map(str,self.elementTable.values())
    attrs=map(str,self.attributeTable.values())
    return "{Target:%s}{Types:%s}{Groups:%s}{AttrGroups:%s}{Elements:%s}{Attributes:%s}"%(self.targetNS,''.join(types),''.join(groups),''.join(attributeGroups),''.join(elts),''.join(attrs))

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def maybeSetVar(self,varName,attrName,default):
    if self.xrpr.elt.hasAttrVal(attrName):
      setattr(self,varName,self.xrpr.elt.attrVal(attrName))
    else:
      setattr(self,varName,default)

  def doBuiltIns(self,sschema):
    self.doAbInitios(sschema)
    # TODO: implement fixed facets
    for (bitn,basen,facets,idt) in builtinTypeNames:
      fake=simpleTypeElt(sschema,None)
      fake.name=bitn
      fake.restriction=restrictionElt(sschema,None)
      fake.restriction.init(None)
      fake.init(None)
      fake.component.basetypeName=QName(None,basen,XMLSchemaNS)
      fake.component.variety='atomic'
      fake.component.idt=idt
      bit=fake.restriction.component
      bit.builtin=1
      bit.rootName=fake.component.basetype.rootName
      self.typeTable[bitn]=fake.component
      for (fc,fv) in facets:
        nf=fc(sschema,None)
        fake.restriction.facets[fc.name]=nf
        if fc.name=="pattern":
          nf.stringValue=fv
        else:
          nf.value=fv
    for (bitn,basen,idt) in builtinLists:
      fake=simpleTypeElt(sschema,None)
      fake.name=bitn
      fake.list=listElt(sschema,None)
      fake.list.init(None)
      fake.init(None)
      fake.component.basetype=Type.urSimpleType
      fake.component.variety='list'
      fake.list.component.itemtypeName=QName(None,basen,XMLSchemaNS)
      wf=Whitespace(sschema,None)
      wf.value='collapse'
      wf.fixed=1
      mf=MinLength(sschema,None)
      mf.value=1
      fake.component.facets={'whiteSpace':wf,'minLength':mf}
      fake.component.idt=idt
      self.typeTable[bitn]=fake.component
    ap=Particle(sschema,None,
                          AnyAny(sschema,None),None)
    ap.term.processContents='lax'
    ap.occurs=(0,None)
    if not Type.urType.model.term.particles:
      Type.urType.model.term.particles.append(ap)
      au=AttributeUse(sschema,None,
                                AnyAny(sschema,None),'optional')
      au.attributeDeclaration.processContents='lax'
      Type.urType.attributeDeclarations={'#any':au}
    else:
      shouldnt('dbl ur')
    self.typeTable['anyType']=Type.urType
    Type.urSimpleType.schema=Type.urType.schema=self
    Type.urSimpleType.sschema=Type.urType.sschema=sschema
    ws=Whitespace(sschema,None)
    ws.value="preserve"
    Type.urSimpleType.facets['whiteSpace']=ws
    self.typeTable['anySimpleType']=Type.urSimpleType

  def doAbInitios(self,sschema):
    wsf1=Whitespace(sschema,None)
    wsf1.value="collapse"
    wsf1.fixed="true"
    wsf2=Whitespace(sschema,None)
    wsf2.value="preserve"
    for (ain,ait) in abInitioTypes:
      aiti=ait(sschema)
      aiti.rootName=ain
      aiti.basetype=Type.urSimpleType
      if ain=='string':
        aiti.facets['whiteSpace']=wsf2
      else:
        aiti.facets['whiteSpace']=wsf1
      self.typeTable[ain]=aiti

  def installInstanceAttrs(self,sschema):
    sschema.eltStack=['a']              # hack
    for (attrn,basen) in _instanceAttrs:
      fake=attributeElt(sschema,None)
      fake.name=attrn
      fake.type=basen
      fake.init(None)
      fake.component.typeDefinitionName=QName(None,basen,
                                                        XMLSchemaNS)
      self.attributeTable[attrn]=fake.component
    for (attrn,itemn) in _instanceLists:
      fake=attributeElt(sschema,None)
      fake.name=attrn
      fake.simpleType=simpleTypeElt(sschema,None)
      fake.simpleType.list=listElt(sschema,None)
      fake.simpleType.list.init(None)
      fake.simpleType.list.component.itemtypeName=QName(None,itemn,
                                                                  XMLSchemaNS)
      fake.simpleType.init(None)
      fake.simpleType.component.variety='list'
      fake.simpleType.component.basetype=Type.urSimpleType
      fake.init(None)
      wf=Whitespace(sschema,None)
      wf.value='collapse'
      wf.fixed=1
      fake.simpleType.component.facets={'whiteSpace':wf}
      self.attributeTable[attrn]=fake.component
    sschema.eltStack=[]              # hack
    ap=Particle(sschema,None,
                          AnyAny(sschema,None),None)
    ap.term.processContents='lax'
    ap.occurs=(0,None)

  def prepare(self):
    if self.prepared:
      return
    # try to touch everything that might cause errors
    cool=1
    for i in self.typeTable.values():
      if isinstance(i,Type):
        cool=i.prepare() and cool
    for tab in (self.elementTable, self.attributeTable,
                self.groupTable, self.attributeGroupTable):
      for i in tab.values():
        cool=i.prepare() and cool
    self.prepared=1
    return cool

  def error(self,message,elt=None,warning=0,extras=None):
    # should have code argument to identify SRC/COS
    if warning:
      if self.sschema.dontWarn:
        return
      ee=self.sschema.resElt.newDaughter("schemaWarning")
    else:
      ee=self.sschema.resElt.newDaughter("schemaError")
    if self.sschema.prepared:
      ee.newAttr("phase","instance")
    else:
      ee.newAttr("phase","schema")
    if not warning:
      self.errors=self.errors+1
    if elt is not None:
      where(ee,elt.where)
    ee.newText(message)
    if extras:
      ee.children=ee.children+extras

# $Log: Schema.py,v $
# Revision 1.12  2007-02-16 15:49:34  ht
# handle schema warnings as warnings
#
# Revision 1.11  2005/11/01 10:03:07  ht
# minLength=1 for builtin lists
#
# Revision 1.10  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.9  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.8  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.7  2004/06/30 10:46:10  ht
# get facet inheritance working properly for builtins
#
# Revision 1.6  2002/12/01 21:54:59  ht
# add and inherit idt (identity constraint type) to type defs
#
# Revision 1.5  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.4  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.3  2002/09/23 21:35:43  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:09:25  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
