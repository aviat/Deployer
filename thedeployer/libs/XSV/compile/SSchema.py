"""Schema compilation: SSchema component"""

__version__="$Revision: 1.25 $"
# $Id: SSchema.py,v 1.25 2007-02-16 14:41:58 ht Exp $

import re
import os
import sys
import types
import traceback
from urlparse import urljoin, urlparse, urlsplit, urlunsplit
from urllib2 import urlopen, Request

import XSV

from XSV.infoset.relNorm import rebuild as relRebuild
from XSV.infoset.indNorm import rebuild as indRebuild
from XSV.infoset.SchemaFiles import safeReadXML, doSchemaLocs

usePyLTXML = XSV.useLTXML()

if usePyLTXML:
  from PyLTXML import Open, Close, NSL_read, NSL_read_namespaces
  from PyLTXML import GetNextBit, GetAttrVal, error, OpenString
  NSL_bad="bad"
  NSL_start_bit="start"
  NSL_empty_bit="empty"
else:
  from XSV.infoset.SAXLTXML import Open, Close, NSL_read, NSL_read_namespaces
  from XSV.infoset.SAXLTXML import GetNextBit, GetAttrVal
  from XSV.infoset.SAXLTXML import NSL_bad, NSL_start_bit, NSL_empty_bit
  from XSV.infoset.SAXLTXML import SXLError
  class error(SXLError):
    def __init__(self):
      SXLError.__init__(self,"shouldn't happen")

from elts.schemaElt import schemaElt

from XSV.compile import XMLSchemaNS, XMLNS, XMLSchemaInstanceNS
from XSV.compile import psviIndMap, auxComponentMap, builtinPats
from XSV.compile.elts.commonElt import commonElt

from SimpleType import SimpleType
from ListFacet import Pattern
from Schema import Schema
from ComplexType import ComplexType
from XSV.validate.validateElement import validate

from SchemaError import whereString

from XSV.compile import eltClasses, AST

_syspat=re.compile("^[^[]* (SYSTEM|PUBLIC) ")
_intpat=re.compile("^[^[]*\[([^\001]*)\]")

_schemaEltDispatch=    {("schema","element"):("group","dds"),
			("all","element"):("group","model"),
			("choice","element"):("group","model"),
			("sequence","element"):("group","model"),
                        ("complexType","element"):"error",
			("group","element"):"error",
			("all","any"):("group","model"),
			("choice","any"):("group","model"),
			("sequence","any"):("group","model"),
                        ("complexType","any"):"error",
			("group","any"):"error",
			("schema","group"):("group","dds"),
			("redefine","group"):("group","dds"),
                        ("restriction","group"):"self",
			("restriction","all"):"self",
			("restriction","choice"):"self",
			("restriction","sequence"):"self",
                        ("extension","group"):"self",
			("extension","all"):"self",
			("extension","choice"):"self",
			("extension","sequence"):"self",
                        ("complexType","group"):"self",
			("complexType","all"):"self",
			("complexType","choice"):"self",
			("complexType","sequence"):"self",
                        "complexContent":"self",
                        "simpleContent":"self",
			("group","group"):("group","model"),
			("group","all"):("group","model"),
			("group","choice"):("group","model"),
			("group","sequence"):("group","model"),
			("all","group"):("group","model"),
			("all","all"):("group","model"),
			("all","choice"):("group","model"),
			("all","sequence"):("group","model"),
			("choice","group"):("group","model"),
			("choice","all"):("group","model"),
			("choice","choice"):("group","model"),
			("choice","sequence"):("group","model"),
			("sequence","group"):("group","model"),
			("sequence","all"):("group","model"),
			("sequence","choice"):("group","model"),
			("sequence","sequence"):("group","model"),
			"anyAttribute":("group","attrs"),
			("attributeGroup","attribute"):("group","attrs"),
			("restriction","attribute"):("group","attrs"),
			("extension","attribute"):("group","attrs"),
			("complexType","attribute"):("group","attrs"),
			("schema","attribute"):("group","dds"),
			"annotation":("group","annot"), # broken for schema
			"documentation":("group","documentation"),
			"appinfo":("group","appinfo"),
			"key":("group","keys"),
			"keyref":("group","keyrefs"),
			"unique":("group","uniques"),
			("attributeGroup","attributeGroup"):("group","attrs"),
			("complexType","attributeGroup"):("group","attrs"),
			("restriction","attributeGroup"):("group","attrs"),
			("extension","attributeGroup"):("group","attrs"),
			("schema","attributeGroup"):("group","dds"),
			("redefine","attributeGroup"):("group","dds"),
			("element","complexType"):"self",
			("element","simpleType"):"self",
			("attribute","simpleType"):"self",
                        "restriction":"self",
                        "extension":"self",
			("restriction","simpleType"):"self",
                        "list":"self",
			("list","simpleType"):"self",
                        "union":"self",
			("union","simpleType"):("group","subTypes"),
			("schema","complexType"):("group","dds"),
			("redefine","complexType"):("group","dds"),
			("schema","simpleType"):("group","dds"),
			("redefine","simpleType"):("group","dds"),
			"maxInclusive":("group","facets"),
			"maxExclusive":("group","facets"),
			"minInclusive":("group","facets"),
			"minExclusive":("group","facets"),
			"enumeration":("group","facets"),
			"fractionDigits":("group","facets"),
			"minFractionDigits":("group","facets"),
			"precision":("group","facets"),
			"lexicalMappings":("group","facets"),
			"totalDigits":("group","facets"),
			"length":("group","facets"),
			"maxLength":("group","facets"),
			"minLength":("group","facets"),
			"pattern":("group","facets"),
			"whiteSpace":("group","facets"),
			"field":("group","fields"),
			"selector":"self"
			}

class SSchema(relRebuild.factory):
  useDTD=0
  prepared=0
  current=None                          # the Schema being built
  targetNS=0                            # the target namespace thereof
  rebuilding=0
  derefNSNs=1
  XMLVersion="1.0"                      # will change each episode
  def __init__(self,filename=None,useDump=0):
    # TODO: use the base property in the appropriate infoset
    if ((not filename) or
        (not urlparse(filename)[0])):
      cwd=urlunsplit(('file','',os.getcwd().replace('\\','/')+'/','',''))
      if filename:
        self.base=urljoin(cwd,filename)
      else:
        self.base=cwd
    else:
      self.base=filename
    self.fileNames=[self.base]
    self.schemaStack=[]
    self.eltStack=[]
    self.schemas={}
    self.unprocessedImports={}
    self.processingInclude=0
    self.inputFileMap={}
    self.losingNamespaces={}
    self.knownComps={}
    self.losers=[]
    self.openNow=[]
    self.allowedNamespaces=[]
    self.checkingSchema=0
    self.currentCTC=None
    home='.'
    for p in sys.path:
      if os.path.isfile("%s/%s"%(p or '.','nndump.xml')):
        home=(p or '.')
        break
      if os.path.isfile("%s/XSV/%s"%(p or '.','nndump.xml')):
        home="%s/XSV"%(p or '.')
        break
    home = os.path.abspath(home)
    home=home.replace("\\","/")
    if home[1]==':':
      home='file:///'+home
    self.home=home
    if useDump:
      self.initFromDump("%s/nndump.xml"%home)

  def initFromDump(self,dumpFileName):
    self.prepare()
    self.rebuilding=1
    rds=indRebuild.fromIndFile(dumpFileName,self.psviConstruct)
    if rds is None:
      sys.stderr.write("couldn't initialize from %s!!!\n"%dumpFileName)
      raise error
    for nsi in rds.schemaInformation:
      if nsi.schemaNamespace:
        # xsi is skipped
        if self.schemas.has_key(nsi.schemaNamespace):
          s=self.schemas[nsi.schemaNamespace]
        else:
          s=Schema(self,None)
          s.targetNS=s.targetNamespace=nsi.schemaNamespace
          self.schemas[nsi.schemaNamespace]=s
        s.prepared=1
        for c in nsi.components:
          if c.foundWhere:
            if getattr(s,c.foundWhere).has_key(c.name):
              if not (isinstance(c,SimpleType) and
                      c.name in ('ENTITY','NMTOKEN','Name','language')):
                # they're allowed as they have the original of various patterns
                print ('oops',s,c,c.name)
            else:
              getattr(s,c.foundWhere)[c.name]=c
    self.rebuilding=0
    self.current=None
    self.targetNS=0

  def fromFile(self,filename,frag,targetNS,why,btlist,ne,useDTD=0,keepGoing=0):
    if useDTD:
      self.useDTD=1
    elif self.useDTD:
      useDTD=1
    schema=None
    if self.targetNS!=0:
      # we save the defaults in case an <include>d schema changes them
      self.schemaStack[0:0]=[(self.current,self.targetNS,
                              self.allowedNamespaces,
                              self.processingInclude,
                              self.XMLVersion,
                              self.current and (self.current.errors,
                              self.current.elementFormDefault,
                              self.current.attributeFormDefault,
                              self.current.blockDefault,
                              self.current.finalDefault,
                              self.current.xrpr))]
#      if targetNS!=self.current.targetNS:
 #       if self.schemas.has_key(targetNS):
  #        self.current=self.schemas[targetNS]
   #     else:
    #      self.current=None
      self.processingInclude=(why=='include' or why=='redefine')
      if self.current:
        self.current.errors=0
    self.targetNS=targetNS
    fullFile=filename
    layErr=None
    if fullFile is None:
      self.fileNames[0:0]=[self.fileNames[0]]
    else:
      self.fileNames[0:0]=[fullFile]
    if (filename is not None
        and useDTD):
      # TODO: frag?
      vres=0
      sdoc=1
      try:
        if type(fullFile)==types.UnicodeType:
          fullFile=fullFile.encode('utf_8')
        f=Open(fullFile,NSL_read|NSL_read_namespaces)
        if f is not None:
          if usePyLTXML:
            dts=f.doctype.doctypeStatement
          else:
            # HACK!
            dts='xs:schema PUBLIC "-//W3C//DTD XMLSCHEMA 200102//EN" "XMLSchema.dtd"'
          if dts is not None and _syspat.match(dts):
            # let them use their own doctype
            ff=None
            fake=None
          else:
            intDecls=""
            if dts is not None:
              mres=_intpat.match(dts)
              if mres:
                intDecls=mres.group(1)
            prefs=[]
            scpFound=0
            b=GetNextBit(f)
            while (b and b.type not in (NSL_start_bit,NSL_empty_bit)):
              if b.type==NSL_bad:
                b=None
                break
              b=GetNextBit(f)
            if b is None:
              sys.stderr.write("%s has no elements???\n"%fullFile)
              raise error
            for (key,val) in b.item.nsdict.items():
              if val==XMLSchemaNS:
                scpFound=1
                scp=key
              elif key=='xml' and val==XMLNS:
                continue
              else:
                prefs.append(key)
            if not scpFound:
              sys.stderr.write("document element of %s is not in namespace %s\n"%(fullFile,XMLSchemaNS))
              raise error
            if scp!='xs':
              if scp:
                pref="%s:"%scp
                pds="\n<!ENTITY %"+" s ':%s'>\n<!ENTITY %% p '%s:'>"%(scp,scp)
              else:
                pref=""
                pds="\n<!ENTITY % s ''>\n<!ENTITY % p ''>"
            else:
              pds=""
              pref="xs:"
            ns=""
            for p in prefs:
              if p:
                ns=ns+"\n<!ATTLIST %sschema xmlns:%s CDATA #IMPLIED>"%(pref,p)
            if pds or ns or intDecls:
              fake1="<!DOCTYPE %sschema SYSTEM '%s/XMLSchema.dtd'"%(pref,
                                                                    self.home)
              fake2=" [%s"%pds;
              fake3="%s\n%s]>\n"%(ns, intDecls)
              fake=fake1+fake2+fake3
            else:
              fake="<!DOCTYPE %sschema SYSTEM '%s/XMLSchema.dtd'>\n"%(pref,
                                                                      self.home)
            fake=fake+"<%sschema/>"%pref
            ff=OpenString(fake,
                                  NSL_read|NSL_read_namespaces)
          if ff or not fake:
            try:
              res=relRebuild.factory.fromFile(self,_schemaEltDispatch,
                                   {"finalDefault":"ignore",
                                    "blockDefault":"ignore",
                                    "elementFormDefault":"ignore",
                                    "attributeFormDefault":"ignore",
                                    "nillable":"nullable"},
                                   _lookup,"instance","variable",None,
                                   XMLSchemaNS,
                                   fullFile,
                                   (XMLSchemaNS,"schema"),ff)
            except relRebuild.LayerError,layErr:
              res=None
          else:
            res=None
        else:
          res=None
      except error:
        res=None
    else:
      # Use dumped/reloaded schema for schemas
      sdoc=safeReadXML(fullFile,ne,"schema",btlist,
                       frag,"schema","id",self.base)
      res=None
      vres=0
      if sdoc is not None:
        selt=sdoc.documentElement
        if (selt.localName=='schema' and
            selt.namespaceName==XMLSchemaNS):
          if selt.attributes.has_key((None,'targetNamespace')):
            ntns=selt.attributes[(None,'targetNamespace')].normalizedValue
          else:
            ntns=None
          self.allowedNamespaces=[XMLSchemaNS,ntns]
        else:
          # will fail lower down anyway
          ntns=0
        if ntns in (XMLSchemaNS,
                    XMLSchemaInstanceNS,XMLNS):
          ne.newAttr('outcome','redundant')
          schema=self.schemas[selt.attributes[(None,'targetNamespace')].normalizedValue]
        else:
          oerrs=self.errors
          stns=self.targetNS
          self.targetNS=ntns            # so the doSchemaLocs will push
          slerrs=doSchemaLocs(selt,self.sfors,ne,0,
                                          filename,None,None,
                                          useDTD,keepGoing)
          self.targetNS=stns
          self.checkingSchema=1
          vres=validate(selt,self.sfors)+slerrs-oerrs
          self.checkingSchema=0
          if ((not vres) or keepGoing):
            try:
              res=relRebuild.factory.fromFile(self,_schemaEltDispatch,
                                   {"finalDefault":"ignore",
                                    "blockDefault":"ignore",
                                    "elementFormDefault":"ignore",
                                    "attributeFormDefault":"ignore",
                                    "nillable":"nullable"},
                                   _lookup,"instance","variable",None,
                                   XMLSchemaNS,
                                   None,
                                   (XMLSchemaNS,"schema"),None,
                                         sdoc.documentElement)
            except relRebuild.LayerError,layErr:
              pass
    if ((sdoc is None) or
        ((schema is None) and ((not isinstance(res,schemaElt)) or
                               vres))):
      xe=ne.newDaughter("notASchema")
      xe.newAttr('filename',fullFile)
      if layErr:
        xe.newAttr('lowLevelErrorMsg',str(layErr))
      if vres:
        xe.newAttr('errors','%s'%vres)
    if res is not None:
      schema=res.component
      vres=vres+schema.errors
      if vres:
        schema.buggy=1
      schema.locations.append(fullFile)
    else:
      self.losers.append(fullFile)
    # schema is a an instance of schema, if present
    self.fileNames=self.fileNames[1:]
    if self.schemaStack:
      self.current=self.schemaStack[0][0]
      (self.current,self.targetNS,
       self.allowedNamespaces,
       self.processingInclude,
       self.XMLVersion,
       currentStuff) = self.schemaStack[0]
      if self.current:
        (self.current.errors,
         self.current.elementFormDefault,
         self.current.attributeFormDefault,
         self.current.blockDefault,
         self.current.finalDefault,
         self.current.xrpr)=currentStuff
      self.schemaStack=self.schemaStack[1:]
#    elif hasattr(self,'sfors') and self.sfors:
#      self.current=self.sfors
#      self.targetNS=self.current.targetNS
    else:
      self.current=None
      self.targetNS=0
    return schema

  def prepare(self):
    # before we do anything serious, check if we need to
    # bootstrap the schema for schema
    if self.schemas.has_key(XMLSchemaNS):
      # we're validating a schema with a (purported) schema for schemas,
      # or we're running useDTD=0
      sfors=self.schemas[XMLSchemaNS]
      self.sfors=sfors
      if ((not sfors.typeTable.has_key('string')) or
          (not sfors.typeTable['string'].__dict__.has_key('basetype')) or
          (sfors.typeTable['string'].basetype is None) or
          sfors.typeTable['string'].basetype.name is not AST):
        # need the ab-initio types
        sfors.targetNS=XMLSchemaNS
        self.current=sfors
        self.targetNS=XMLSchemaNS
        sfors.doBuiltIns(self)
    else:
      self.initSforS()
    self.sfors.nsdict={'xs':XMLSchemaNS}
    sforsi=Schema(self,None)
    self.schemas[XMLSchemaInstanceNS]=sforsi
    self.sforsi=sforsi
    sforsi.targetNS=XMLSchemaInstanceNS
    self.current=sforsi
    self.targetNS=XMLSchemaInstanceNS
    sforsi.installInstanceAttrs(self)
    sforsi.prepared=1
    self.current=self.sfors
    self.targetNS=XMLSchemaNS
    ec=0
    for sch in self.schemas.values():
      ec=ec+sch.errors
    self.prepared=1
    return ec

  def initSforS(self):
    sfors=Schema(self,None)
    self.schemas[XMLSchemaNS]=sfors
    self.sfors=sfors
    sfors.targetNS=XMLSchemaNS
    self.current=sfors
    self.targetNS=XMLSchemaNS
    sfors.doBuiltIns(self)

  def schemaFile(self,filename,base,reason,noRDDL=0):
    # normalize and get file: in there if needed
    base=urlunsplit(urlsplit(base,'file'))
    full=urljoin(base,filename)
    if self.inputFileMap.has_key(full):
      return self.inputFileMap[full]
    else:
      self.inputFileMap[full]=None
      res=self.schemaFile1(full,reason,noRDDL)
      self.inputFileMap[full]=res
      return res

  def schemaFile1(self,full,reason,noRDDL):
    # sniff the file to see what it's like
    em=None
    while full is not None:
      ffull=full
      try:
        if type(full)==types.UnicodeType:
          full=full.encode('utf_8')
        (s,l,p,q,frag)=urlsplit(full)
        if frag=="":
          frag=None
        else:
          full=urlunsplit((s,l,p,q,""))
        if s!="file":
          # allow for redirects
          ou=urlopen(Request(full,None,{"Accept":"application/xml, text/xml; q=0.9, */*"}))
          full=ou.geturl()
          ou.close()
        f=Open(full,
                       NSL_read|NSL_read_namespaces)
      except error:
        full=None
        em="couldn't open"
        break
      except IOError:
        full=None
        em="couldn't open"
        break
      b=GetNextBit(f)
      while (b and b.type not in (NSL_start_bit,NSL_empty_bit)):
        if b.type==NSL_bad:
          b=None
          break
        b=GetNextBit(f)
      if b is None:
        sys.stderr.write("%s has no elements???\n"%full)
        raise error # error
      nsdict=b.item.nsdict
      if ((not noRDDL) and
          frag is None and
          b.item.llabel=="html" and
          b.item.nsuri=="http://www.w3.org/1999/xhtml"):
        # may be RDDL file
        rddl=0
        for (key,val) in nsdict.items():
          if val=="http://www.rddl.org/":
            rddl=1
            break
        if rddl:
          ne=reason.newDaughter("importAttempt")
          ne.newAttr('URI',full)
          ne.newAttr('outcome','RDDL')
          b=GetNextBit(f)
          while b:
            if ((b.type==NSL_start_bit or b.type==NSL_empty_bit) and
                b.item.llabel=="resource" and
                b.item.nsuri=="http://www.rddl.org/"):
              # this is somewhat tedious
              for (p,n) in b.item.nsdict.items():
                if n=="http://www.w3.org/1999/xlink":
                  break
              else:
                p=""                    # hack to fail
              if GetAttrVal(b.item,"%s:role"%p)==XMLSchemaNS:
                newf=GetAttrVal(b.item,"%s:href"%p)
                if newf:
                  full=urljoin(full,newf)
                else:
                  em="RDDL resource for W3C XML Schema lacked an xlink:href"
                  full=None
                break
            elif b.type==NSL_bad:
              Close(f)
              raise error
            b=GetNextBit(f)
          else:
            full=None
            em="Recognised as RDDL, but no W3C XML Schema resource found"
        else:
          em="Not recognised as W3C XML Schema or RDDL: %s"%b.item.label
          full=None
      elif b.item.llabel=="schema":
        if (b.item.nsuri==XMLSchemaNS and
            (frag is None or GetAttrVal(b.item,"id")==frag)):
          Close(f)
          return (full,
                  GetAttrVal(b.item,"targetNamespace"),
                  frag)
        em="Root was <schema>, but not in W3C XML Schema namespace: %s (was %s)"%(XMLSchemaNS,b.item.nsuri)
        full=None
      elif frag is not None:
        b=GetNextBit(f)
        while b:
          if ((b.type==NSL_start_bit or b.type==NSL_empty_bit) and
              b.item.llabel=="schema" and
              GetAttrVal(b.item,"id")==frag):
            if b.item.nsuri==XMLSchemaNS:
              Close(f)
              return (full,
                      GetAttrVal(b.item,"targetNamespace"),
                      frag)
            em="<schema id=\"%s\"> found, but not in W3C XML Schema namespace: %s (was %s)"%(frag,XMLSchemaNS,b.item.nsuri)
            full=None
          elif b.type==NSL_bad:
            Close(f)
            raise error
          b=GetNextBit(f)
      else:
        em="Not recognised as W3C XML Schema or RDDL: %s"%b.item.label
        full=None
    try:
      Close(f)
    except:
      pass
    ne=reason.newDaughter("notASchema")
    ne.newAttr('filename',ffull)
    if em:
      ne.newText(em)

  def checkinSchema(self,namespace,location,base,why,useDTD=0,keepGoing=0,
                    elt=None):
    ne=self.resElt.newDaughter("schemaDocAttempt")
    ne.newAttr('source',why)
    if namespace!=0 and namespace is not None:
      ne.newAttr('namespace',namespace)
    if location is None:
      fullLoc='[stdin]'
      ne.newAttr('base',base)
    else:
      fullLoc=urljoin(base,location)
    ne.newAttr('URI',fullLoc)
    including=(why=='include' or why=='redefine')
    res=None
    btlist=[]
    try:
      if location is None:
        res=self.fromFile(None,None,namespace,why,btlist,ne,useDTD,keepGoing)
      else:
        lres=self.schemaFile(location,base,ne,including)
        if lres:
          (loc,fileTargetNamespace,frag)=lres
          if (loc in self.openNow or
              (self.schemas.has_key(namespace) and
              (loc in self.schemas[namespace].locations))):
            # TODO: allow multiple frags per doc
            ne.newAttr('outcome','redundant')
            # i.e. we've seen this before for this namespace or it's in play now
            return self.schemas[namespace]
          if loc in self.losers:
            # TODO: allow multiple frags per doc
            ne.newAttr('outcome','failed already')
            return
          if (namespace!=0 and
              namespace!=fileTargetNamespace and
              ((not including) or fileTargetNamespace)): # allow for chameleon
            ne.newAttr('outcome',
                       "Failure: targetNamespace mismatch: %s expected, %s found" %
                            (namespace,fileTargetNamespace))
            if elt:
              sa=ne.attributes[(None,'source')]
              sa.normalizedValue="%s, %s"%(sa.normalizedValue,
                                          whereString(elt.where))
            return
          if frag is not None:
            xloc="%s#%s"%(loc,frag)
          else:
            xloc=loc
          if xloc!=fullLoc:
            ne.newAttr('trueURI',xloc)
          self.openNow[0:0]=[loc]
          res=self.fromFile(loc,frag,namespace,why,btlist,ne,useDTD,keepGoing)
    except:
      pfe=self.resElt.newDaughter("bug")
      errstr=''.join(traceback.format_exception(sys.exc_type,
                                                    sys.exc_value,
                                                    sys.exc_traceback))
      pfe.newText("validator crash during %s:\n%s"%(why,errstr))
    self.openNow=self.openNow[1:]
    if ((res is not None) and
        not res.buggy and
        not ne.attributes.has_key((None,'outcome'))):
      # last clause is to avoid being fooled by sfors redundancy lower down
      ne.newAttr('outcome','success')
    else:
      if not ne.attributes.has_key((None,'outcome')):
        ne.newAttr('outcome','failure')
      for err in btlist:
        pfe=self.resElt.newDaughter("bug")
        errstr=''.join(err)
        pfe.newText("validator crash during %s:\n%s"%(why, errstr))
    return res

  def tryHardForDecl(self,localName,namespace,kind,schema,item):
    if ((not self.schemas.has_key(namespace)) or
        (kind=='element' and
         not self.schemas[namespace].elementTable.has_key(localName)) or
        (kind=='attribute' and
         self.schemas[namespace].attributeTable.has_key(localName))):
      # first try xsi:schemaLoc
      # TODO: schemaLoc not allowed after first appearance of NS it 'addresses'
      if kind=='element':
        sbs=self.resElt.attributes[(None,"target")].normalizedValue
        if sbs=='[stdin]':
          sbs=self.base
        doSchemaLocs(item,schema,self.resElt,0,sbs,None)
      if (self.derefNSNs and namespace and
          (not self.schemas.has_key(namespace)) and
          (not self.losingNamespaces.has_key(namespace))):
        # now try namespace name (will be cheap if tried before)
        self.checkinSchema(namespace,
                           namespace,
                           self.base,
                           "new namespace",0,0,item)

  def psviConstruct(self,name,attrs):
    rrm=None
    try:
      iClass=psviIndMap[name]
      # print ('pc',name,iClass)
      if iClass is None:
        # means skip it altogether
        return None
      if type(iClass)==types.TupleType:
        # cheat for subclasses types, e.g. SimpleType, KCons
        # print 'tt'
        rrm=iClass[1].reflectionInMap
        if iClass[1].__dict__.has_key('reflectedName'):
          rrn=iClass[1].reflectedName
        else:
          rrn=None
        iClass=iClass[0]
        # print ('pc2',name,iClass,rrn,rrm)
    except KeyError, n:
      # print ('ke',n)
      iClass=auxComponentMap[name]
    # should prune all the non-ref'ed IDs out
    ref=indRebuild.av(attrs,'ref')
    if ref:
      if self.knownComps.has_key(ref):
        # print ('known ref',ref)
        val=self.knownComps[ref]
        val.reffed=1
        return val
      elif self.sfors.typeTable.has_key(ref):
        # print ('prim ref',ref)
        val=self.sfors.typeTable[ref]
        val.reffed=1
        return val
      elif (ref[0:10]=='xsd..type.' and
            ref[10]!='_' and
            self.sfors.typeTable.has_key(ref[10:])):
        val=self.sfors.typeTable[ref[10:]]
        val.reffed=1
        # print ('type ref',ref,val)
      elif ref[0:5]=='bip..':
        pat=Pattern(self,None)
        pat.value=builtinPats[int(ref[5:6])]
        return pat
      else:
        # forward ref,
        # put in in identified anyway, right thing will happen
        # print ('forward ref',ref)
        val=iClass(self,None)
        self.knownComps[ref]=val
        val.reffed=1
        name=indRebuild.av(attrs,'name')
        if name is not None:
          # Forward refs to attrs come here, because
          # they need their names right away to build
          # typedef-local attr dictionary
          val.name=name
          val.targetNamespace=indRebuild.av(attrs,'tns')
      return val
    else:
      id=indRebuild.av(attrs,'id')
      if id:
        if self.knownComps.has_key(id):
#          print ('forward-reffed comp',id)
          # there were forward references to this
          val=self.knownComps[id]
          val.name=val.targetNamespace=None
        else:
#          print ('new comp',id,val,val.__dict__.has_key('variety'))
          val=iClass(self,None)
          self.knownComps[id]=val
      else:
        val=iClass(self,None)
      if rrm is not None:
        val.reflectionInMap=rrm
        if rrn:
          val.reflectedName=rrn
      if iClass is ComplexType:
        val.saveCTC=self.currentCTC
        self.currentCTC=val
      return val

def _lookup(eltName):
  if eltClasses.has_key(eltName):
    return eltClasses[eltName]
  else:
    return userClass

class userClass(commonElt):
  def init(self,elt):
    # must be inside documentation or appinfo == a bug
    self.error("Undeclared element in XML Schema namespace used in documentation")

# $Log: SSchema.py,v $
# Revision 1.25  2007-02-16 14:41:58  ht
# improve nndump failure behaviour
#
# Revision 1.24  2006/08/15 16:17:19  ht
# fall back to pull-SAX if PyLTXML not available
#
# Revision 1.23  2005/08/10 20:30:10  ht
# better debugging output
#
# Revision 1.22  2005/06/09 12:53:50  ht
# make base file: in two places
#
# Revision 1.21  2005/06/08 16:15:26  ht
# use publicised accept header
#
# Revision 1.20  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.19  2004/10/13 08:42:54  ht
# convert LayerError properly
#
# Revision 1.18  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.17  2004/08/31 15:12:12  ht
# add serialisation support,
# fix baseURI stuff yet again
#
# Revision 1.16  2004/08/18 08:44:37  ht
# dump patterns properly
#
# Revision 1.15  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.14  2003/09/01 15:34:05  ht
# fix arg't count error in stdin call to fromFile
# use baseURI more/better
#
# Revision 1.13  2003/07/01 15:56:22  ht
# use redirected URL if there is one
#
# Revision 1.12  2003/06/30 21:54:15  ht
# support fragid in schemaLoc, including self
#
# Revision 1.11  2003/04/01 18:48:27  ht
# catch schema bogus elts in documentation cleanly
#
# Revision 1.10  2003/02/14 09:49:18  ht
# detect home via nndump.xml, not XMLSchema.dtd
#
# Revision 1.9  2003/02/14 09:37:36  ht
# add switch to supress derefing namespace names,
# allow for stdin in schema-only mode
#
# Revision 1.8  2003/01/21 23:21:58  ht
# fix infinite loop in some bogus schema doc cases
#
# Revision 1.7  2002/11/27 13:53:38  ht
# rule out some dangerous placements for element and any
#
# Revision 1.6  2002/11/04 13:34:19  ht
# protect against unicode filenames
#
# Revision 1.5  2002/10/03 13:53:19  ht
# fix nndump.xml location search to work with monolithic executable
#
# Revision 1.4  2002/09/23 21:35:43  ht
# move to string methods from string library
#
# Revision 1.3  2002/09/23 13:56:16  ht
# update duplicate check
#
# Revision 1.2  2002/09/02 16:09:25  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
