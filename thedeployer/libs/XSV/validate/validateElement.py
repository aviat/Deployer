"""W3C XML Schema validity assessment: Element"""

__version__="$Revision: 1.23 $"
# $Id: validateElement.py,v 1.23 2005-08-22 12:31:22 ht Exp $

import re
import sys

from XSV.compile.QName import QName, splitQName
from XSV.compile.Element import Element
from XSV.compile.Type import Type
from XSV.compile.SimpleType import SimpleType
from XSV.compile.AbInitio import AbInitio
from XSV.compile.Wildcard import Wildcard
from XSV.compile.FSM import FSMNode, IncrEdge

from XSV.infoset.XMLInfoset import Element as XIElement
from XSV.infoset.XMLInfoset import Characters as XICharacters

from validateAttribute import validateXSIAttrs, validateAttributeTypes, \
                              assignAttributeTypes
from validateKey import validateKeys
from component import validateText
from verror import verror, vwarn
from XSV.compile.SchemaError import whereString

from XSV.compile import XMLSchemaInstanceNS as xsi

_whitespace=None                        # initialised in init()

def validate(element, schema, type=None):
  doc = element.parent
  while isinstance(doc,Element):
    doc = element.parent
  schema.sschema.XMLVersion=doc.version
  if not schema.sschema.__dict__.has_key('errors'):
    schema.sschema.errors=0
  validateElement(element, type, schema)
  return schema.sschema.errors

def validateElement(element, type, schema, eltDecl=None):
  sschema=schema.sschema
  element.idTable=None
  if eltDecl is None and type is None:
    # note if we come from a wildcard that's already failed to find a decl,
    # we don't try again, because eltDecl is 0 in that case
    nsn=element.namespaceName
    eqn=QName(None,element.localName,nsn or None)
    sschema.tryHardForDecl(element.localName,nsn,
                                  'element',schema,element)
    if schema.vElementTable.has_key(eqn):
      eltDecl=schema.vElementTable[eqn]
      if eltDecl is not None:
        type=eltDecl.typeDefinition
  if eltDecl==0:
    eltDecl=None
  validateXSIAttrs(element,schema)
  if isinstance(eltDecl,Element):
     # TODO: is this right if no eltDecl -- think so -- need erratum??
    nullable =  eltDecl.nullable
  else:
    nullable = 1  
  nulled = 0
  if sschema.checkingSchema and element.localName=='import':
    if element.attributes.has_key((None,"namespace")):
      ins=element.attributes[(None,"namespace")].normalizedValue
    else:
      ins=None
    sschema.allowedNamespaces.append(ins)
  if element.attributes.has_key((xsi, "nil")):
    if not nullable:
      verror(element,
             "xsi:nil specified on non-nillable element %s" % element.originalName,
             schema,"cvc-elt.1.1")
      element.assess(sschema,eltDecl)
      return
    nulla=element.attributes[(xsi,"nil")]
    nulled = (nulla.validity=='valid' and
              nulla.schemaNormalizedValue == "true")
  if element.attributes.has_key((xsi, "type")):
    xsitype=None
    typea=element.attributes[(xsi, "type")]
    if typea.validity=='valid':
      t = typea.schemaNormalizedValue;
      (tp,tl) = splitQName(t)
      # because the attribute, a QName, is valid, the prefix, even
      # if it's None, must be bound
      if element.inScopeNamespaces.has_key(tp):
        qt = QName(tp,
                   tl, element.inScopeNamespaces[tp].namespaceName)
      else:
        qt= QName(tp,tl,None)
      if schema.vTypeTable.has_key(qt):
        xsitype=schema.vTypeTable[qt]
        if type is not None and not xsitype.isSubtype(type,type.final):
          verror(element,
             "xsi:type %s is not a subtype of the declared type %s"%(unicode(str(qt),'utf-8'),
                                                                     unicode(str(type.name),'utf-8')),
                 schema,"cvc-elt.2.3")
        elif type is not None:
          vwarn(element,
                "using xsi:type %s instead of original %s" % (unicode(str(qt),'utf-8'),
                                                              unicode(str(type.name),'utf-8')),
                schema)
      else:
        verror(element,"xsi:type %s undefined" % unicode(str(qt),'utf-8'),schema,"cvc-elt.2.2")
    else:
      qt=typea.normalizedValue
    if xsitype is None:
      if type is None:
        vwarn(element,"xsi:type %s didn't yield a type" % unicode(str(qt),'utf-8'),schema)
      else:
        vwarn(element,
              "xsi:type %s didn't yield a type, using original %s" % (unicode(str(qt),'utf-8'),
                                                                      unicode(str(type.name),'utf-8')),
              schema)
    else:
      # TODO: enforce {disallowed substitutions}
      type = xsitype
  element.assessedType = type
  element.lax = lax = type is None
  # might have none in case of recursive call inside <any/>, or at top level,
  # or after errors
  if nulled:
    validateElementNull(element, type, schema)
  if type is not None:
    # TODO: check element is not abstract
    if ((type is not Type.urType) and
        (isinstance(type, AbInitio) or
         isinstance(type, SimpleType))):
      if not nulled:
        validateElementSimple(element, type, schema, eltDecl)
      if isinstance(eltDecl,Element):
        validateKeys(eltDecl,element)
      element.assess(sschema,eltDecl)
      return
    # a complexType
    if type.abstract=='true':
      verror(element,"attempt to use abstract type %s to validate"%unicode(str(type.name),'utf-8'),
             schema,'cvc-complex-type.1')
      element.assess(sschema,eltDecl)
      return
    ad=type.attributeDeclarations
    ps=type.prohibitedSubstitutions
  else:
    ps=[]
    ad={}
  assignAttributeTypes(element, ad, ps, schema, lax)
  idTable=validateAttributeTypes(element, element.attrTable, ad, schema)
  #  print "assigning types for %s" % element.originalName
  if not nulled:
    # we must look at the content model before checking the types, so that
    # we know which children matched <any>
    if type is not None:
      noSubTypes=validateContentModel(element, type, schema, eltDecl)
    idTable=validateChildTypes(element, schema, lax or noSubTypes, idTable)
  if isinstance(eltDecl,Element):
    validateKeys(eltDecl,element)
  element.idTable=idTable
  if sschema.docElt==element:
    checkIDTable(idTable,schema,element)
  element.assess(schema.sschema,eltDecl)
  
def checkIDTable(idTable,schema,docElt):
  for (key,val) in idTable.items():
    l=len(val)
    if l is 0:
      verror(docElt,"id %s referred to but never declared"%key,schema,
             "cvc-id.1")
    elif l is not 1:
      verror(val[1],"duplicate id %s, first appearance was %s"%(key,
                                                                whereString(val[0].where)),
             schema,
             "cvc-id.2")

def validateElementNull(element, type, schema):
  if len(element.children) != 0:
    verror(element,"element %s is nilled but is not empty" % element.originalName,
           schema,"cvc-elt.1.2.1")
  else:
    element.null=1
  # TODO: should check for fixed value constraint

def validateElementSimple(element, type, schema, declaration):
  # check that:
  #   it has no attributes (except xsi: ones)
  #   it has one pcdata child, and if so
  #     the text of the pcdata matches the type
  if element.attributes:
    for a in element.attributes.values():
      if a.namespaceName != xsi:
        verror(element,
               "element {%s}%s with simple type not allowed attributes"%
               (element.namespaceName, element.localName),
               schema,"cvc-elt.4.1.1")
        return
#  verror(element,"xxx {%s}%s with simple type"%(element.namespaceName, element.localName),schema,"yy")

  return validateTextModel(element, type, schema, declaration)

def assignChildTypes(children, elementTable, extendable, schema, lax):
  # look up each child tag and record the type
  # (it may not be an error if it is not declared; we don't know that
  #  until we see what it matches in the content model)
  # TODO: extendable
  for child in children:
    if isinstance(child,XIElement):
      qname = QName(None,child.localName,child.namespaceName or None)
      if elementTable.has_key(qname):
        decl=elementTable[qname]
        child.type = decl.typeDefinition
        child.eltDecl = decl
      elif lax and child.namespaceName and schema.vElementTable.has_key(qname):
        decl=schema.vElementTable[qname]
        child.type=decl.typeDefinition
        child.eltDecl=decl
      else:
	child.type = None
        child.eltDecl=None
  return 1

def validateContentModel(element, type, schema, declaration):
  # trace a path through the content model
  # if a child matches an <any tag=... type=...> we need to indicate
  # that that child should be validated with its xsd:type if it has one
  # if a child matches some other kind of <any> we need to indicate
  # that it's not an error if we can't find its type

#  print "validating model for %s content type %s" % (element.originalName, type.contentType)
  if type.contentType == "empty":
    return validateEmptyModel(element, type, schema)
  elif type.contentType == "textOnly":
    return validateTextModel(element, type.model, schema, declaration)
  else:
    return validateElementModel(element, type.fsm,
                         type.contentType == "mixed", schema, declaration)

def validateEmptyModel(element, type, schema):
  if len(element.children) != 0:
    verror(element,"element %s must be empty but is not" % element.originalName,schema,
           "cvc-complex-type.1.2")
    return 1
  return 0

def validateTextModel(element, type, schema,declaration=None):
  # check that:
  #   it has one pcdata child, and if so
  #     the text of the pcdata matches the type
  name = element.localName
  text=None
  bogus=0
  if declaration is not None:
    vc=declaration.valueConstraint
  else:
    vc=None
  for child in element.children:
    if isinstance(child,XICharacters):
      if not text:
        text=child.characters
      else:
        text=text+child.characters
    elif isinstance(child,XIElement):
      verror(element,
             "element {%s}%s with simple type not allowed element children"%
             (element.namespaceName,name),schema,"cvc-complex-type.1.2.2")
      # TODO: mark this (and any others) as not validated
      return 1
  else:
    if not text:
      if vc is not None:
        if declaration.typeDefinition.simple()!=type:
          # xsi type was used, need to revalidate vc
          # TODO: should use canonical form of vcv, not original
          res=validateText(type,vc[1],element,element)
          if res is not None:
            verror(element,
                   "default doesn't satisfy xsi:type: %s%s"%(vc[1],res),
                   schema,"cvc-element.5.1.1")
        text=vc[1] # TODO: should use canonical form of vcv, not original
      else:
        text=""
    res=validateText(type,text, element, element)
    if res is not None:
      verror(element,"element content failed type check: %s%s"%(text,res),
             schema,"cvc-complex-type.1.2.2")
    elif (vc and vc[0]=='fixed' and element.actualValue!=declaration.vcv):
      verror(element,"fixed value did not match: %s!=%s"%(element.schemaNormalizedValue,vc[1]),schema,"cvc-element.5.2.2.2")
      res=1
    if res is not None:
      try:
        del element.schemaNormalizedValue
      except AttributeError:
        pass
      try:
        del element.actualValue
      except AttributeError:
        pass
    return 0
  
def validateElementModel(element, fsm, mixed, schema, declaration):
  #  print "validating element model for %s" % element.originalName
  if fsm is None:
    return
  fsm.initCounters()
  n = fsm.startNode
  #sys.stdout.write("|%s"%n.id)
  text = None
  qname = None
  for c in element.children:
    if isinstance(c,XICharacters):
      if mixed:
        if not text:
          text=c.characters
        else:
          text=text+c.characters
      elif not _whitespace.match(c.characters):
	verror(element,
               "text not allowed: |%s|" % c.characters,
               schema,"cvc-complex-type.1.2.3")
	return 1
    elif isinstance(c,XIElement):
      l=n.edges
      i=len(l)-1
      while i>=0:
        e=l[i]
        m = e.match(c)
        if m is not None:
          # success
          n = m
          #sys.stdout.write("-%s->%s"%(unicode(e),m.id))
          if e.__class__ is IncrEdge:
            l=m.edges
            i=len(l)-1
            continue
          if e.decl is not None:
            if isinstance(e.decl, Wildcard):
              c.type = e.decl
              c.eltDecl=None                # not used so don't leave around
              c.strict = (e.decl.processContents == 'strict')
            else:
              c.strict = 1
              c.eltDecl=e.decl
              c.type = c.eltDecl.typeDefinition
          else:
            c.strict = 1
            c.type = None
          break
        i=i-1
      else:
        allowed=[]
        c.type=None
        for e in n.edges:
          eq=unicode(str(e),'utf-8')
          if eq!="L":
            allowed.append(eq)
        fx=fsm.asXML()
        verror(c,
               "element %s not allowed here (%s) in element %s, expecting [%s]:\n"%
               (unicode(str(QName(None, c.localName, c.namespaceName or None)),'utf-8'), n.id,
                unicode(str(QName(None,element.localName,element.namespaceName or None)),'utf-8'),
               ",".join(allowed)),
               schema,"cvc-complex-type.1.2.4",0,fx,element)
        return 1
  l=n.edges
  i=len(l)-1
  # Must go backwards, to get ++ edges first
  #sys.stdout.write("$$")
  while i>=0:
    e=l[i]
    x=e.matchEnd()
    if x is None:
      #sys.stdout.write("N")
      i=i-1
      continue
    if x.__class__ is FSMNode:
      n=x
      #sys.stdout.write("-%s->%s"%(unicode(e),x.id))
      l=x.edges
      i=len(l)-1
      continue
    if x==True:
      #sys.stdout.write("-%s->|\n"%unicode(e))
      break
    if x==False:
      #sys.stdout.write("F")
      i=i-1
      continue
    #sys.stdout.write("e")
    verror(element,x.errmsg,schema,"cvc-complex-type.1.2.4")
    i=i-1
  else:
    allowed=[]
    for e in n.edges:
      eq=unicode(str(e),'utf-8')
      if eq!="L":
        allowed.append(eq)
    fx=fsm.asXML()
    verror(element,
           "content of %s is not allowed to end here (%s), expecting %s:\n"%
           (element.originalName,n.id,allowed),
           schema,"cvc-complex-type.1.2.4",1,fx)
  if declaration is not None:
    vc=declaration.valueConstraint
  else:
    vc=None
  if vc is not None:
    if qname:
      # there were element children
      if vc[0]=='fixed':
        verror(element,
               "element content not allowed with 'fixed' value constraint'",
               schema,"cvc-element.5.2.2.1")
    else:
      # empty or only text
      if text is None:
        element.schemaNormalizedValue=element.actualValue=vc[1]
      else:
        # content
        if vc[0]=='fixed':
          if text==vc[1]:
            element.schemaNormalizedValue=element.actualValue=vc[1]
          else:
            verror(element,
                   "fixed value did not match: %s!=%s"%(text,vc[1]),
                   schema,"cvc-element.5.2.2.2")
  return 0 

def validateChildTypes(element, schema, lax, idTable):
  # validate each child element against its type, if we know it
  # report an error if we don't know it and it's not in <any>
  v = 1
  for child in element.children:
    if isinstance(child,XIElement):
      if child.__dict__.has_key('type') and child.type is not None:
        if child.eltDecl is not None:
          validateElement(child,child.type,schema,child.eltDecl)
        else:
          # child.type is actually a wildcard
          child.type.validate(child,schema,'element',element)
      elif lax:
        # TODO: record impact of missing type in PSVI
        validateElement(child,None,schema) # will be lax because no type
      else:
	verror(child,
               "undeclared element %s"%
               unicode(str(QName(None,child.localName,child.namespaceName or None)),'utf-8'),
               schema,"src-resolve")
      if ((child.assessedType is not None) and
          (child.validity=="valid")):
        td=child.assessedType
        if td.idt:
          if td.idt is 3:
            for ids in child.actualValue:
              if ids not in idTable:
                idTable[ids]=[]
          elif td.idt is 2:
            if child.actualValue not in idTable:
              idTable[child.actualValue]=[]
          elif td.idt is 1:
            try:
              idTable[child.actualValue].append(element)
            except KeyError:
              idTable[child.actualValue]=[element]
        if child.idTable:
          for (key,val) in child.idTable.items():
            try:
              idTable[key].extend(val)
            except KeyError:
              idTable[key]=val
  return idTable

def av(self,child,schema,kind,elt):
  q = QName(None,child.localName,child.namespaceName or None)
  if kind=='element':
    kinde='child'
  else:
    kinde=kind
  vwarn(elt,"allowing %s as %s because it matched wildcard(%s)" %
        (unicode(str(q),'utf-8'),kinde,self.allowed),schema)
  if self.processContents!='skip':
#   print "looking for decl for %s" % child.originalName
    schema.sschema.tryHardForDecl(child.localName,
                                  child.namespaceName,kind,schema,child)
    if schema.sschema.schemas.has_key(child.namespaceName):
      try:
        if kind=='element':
          e = schema.vElementTable[q]
        else:
          e = schema.vAttributeTable[q]
      except KeyError:
        e=None
  #     print "decl for %s is %s" % (child.originalName, e)
      if (e is not None) and (e.typeDefinition is not None):
        vwarn(None,"validating it against %s" %
                unicode(str(e.typeDefinition.name or 'anonymous type'),'utf-8'),
              schema)
        if kind=='element':
          validateElement(child, e.typeDefinition, schema, e)
          return
        else:
          child.assessedType = e.typeDefinition
          res=validateText(e.typeDefinition,child.normalizedValue,
                           child, elt)
          # TODO: check child.vc for fixed
          if res is not None:
            verror(elt,
                   "attribute type check failed for %s: %s%s"%(unicode(str(q),'utf-8'),
                                                               child.normalizedValue,
                                                               res),
                   schema,'cvc-attribute.1.2',0,None,child)
            child.schemaNormalizedValue=None
          return
      elif (self.processContents=='strict' and
            not (kind=='element' and child.attributes.has_key((xsi, "type")))):
        # TODO check this against actual def'n of missing component
        losing=1
      elif kind=='element':
        losing=0
      else:
        # lax attribute, I think
        return
    else:
      schema.sschema.losingNamespaces[child.namespaceName]=1
      if self.processContents=='strict':
        losing=1
      else:
        losing=0
    if losing:
      verror(elt,
             "can't find a type for wildcard-matching %s %s" %(kinde,
                                                               unicode(str(q),'utf-8')),
             schema,
             "src-resolve")
    if kind=='element':
      vwarn(None,"validating it %sly"%self.processContents,schema)
      validateElement(child,None,schema,0)

def init():
  global _whitespace
  _whitespace = re.compile("^[ \t\r\n]*$")
  Wildcard.validate=av

# $Log: validateElement.py,v $
# Revision 1.23  2005-08-22 12:31:22  ht
# better, i hope, handling of displaying non-ascii qnames
#
# Revision 1.22  2005/04/15 13:51:19  ht
# MaxEdge is gone
#
# Revision 1.21  2005/04/14 11:47:55  ht
# fix tracer
#
# Revision 1.20  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.19  2004/06/30 10:44:29  ht
# fix bug in ID checking for elements
#
# Revision 1.18  2004/05/18 18:02:07  ht
# changed min check to plain guard
#
# Revision 1.17  2004/05/17 17:31:16  ht
# plus-edge approach to numeric exponents working?
#
# Revision 1.16  2004/05/16 16:41:19  ht
# cul-de-sac wrt counters
#
# Revision 1.15  2004/05/12 15:12:39  ht
# working on counters
#
# Revision 1.14  2004/04/01 13:32:08  ht
# work on final/block a bit
#
# Revision 1.13  2004/01/31 14:14:43  ht
# fix bug in error allocation/reporting when strict fails
#
# Revision 1.12  2004/01/31 11:42:51  ht
# improve PSVI in lax+no decl case
#
# Revision 1.11  2003/08/18 16:27:33  ht
# Improve error recovery after content-model failure
#
# Revision 1.10  2003/04/22 15:16:39  ht
# fix error message after preceding fix
#
# Revision 1.9  2003/04/01 18:46:18  ht
# clean up anyed eltDecl
#
# Revision 1.8  2003/01/22 11:27:11  ht
# protect against missing fsm
#
# Revision 1.7  2002/12/01 21:48:51  ht
# validate ID/IDREF/IDREFS
#
# Revision 1.6  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.5  2002/11/11 20:03:00  ht
# handle allowed specially to get unicode right
#
# Revision 1.4  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.3  2002/09/02 16:12:48  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.2  2002/09/01 21:22:42  ht
# allow type-def to be passed in from top
#
# Revision 1.1  2002/06/28 09:47:42  ht
# validation sub-package version
#
