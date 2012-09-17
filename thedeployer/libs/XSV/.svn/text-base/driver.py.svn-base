"""Top-level invocation of schema-validity assessment"""

# $Id: driver.py,v 1.23 2006-11-03 16:50:41 ht Exp $

import tempfile
import traceback
import time
import re
import sys
import codecs
import os
import types
from urlparse import urljoin, urlunsplit

from XSV.infoset.XMLInfoset import Element, Namespace, \
                                   infosetSchemaNamespace, Document
from XSV.infoset.PSVInfoset import NamespaceSchemaInformation, compareSFSComps

import XSV.infoset.indNorm.reflect
indNorm=XSV.infoset.indNorm
from XSV.compile import XMLSchemaInstanceNS as xsi
from XSV.compile import XMLSchemaNS
from XSV.infoset.PSVInfoset import psviSchemaNamespace

from XSV.compile.SSchema import SSchema
from XSV.compile.Schema import Schema
from XSV.compile.QName import QName
from XSV.compile import init as XMLSchemaInit
from XSV.infoset.SchemaFiles import safeReadXML, doSchemaLocs
from XSV.validate.validateElement import validate

from XSV.compile.SchemaError import where as addWhere
from XSV.compile.SchemaError import shouldnt

vss=XSV.__version__.split()
vs="XSV %d.%d-%d of %s %s"%(XSV.major_version,XSV.minor_version,
                                      XSV.release,vss[5],vss[6])

xsvNS=XSV.xsvNS

def runitAndShow(en,rns=[],k=0,style=None,enInfo=None,outfile=None,dw=1,
                 timing=0,reflect=0,independent=0,reflect2=0,scanForLocs=0,
                 useDTD=0,topType=None,topElt=None,derefNSNs=1,control=2,
                 baseURI=None,preserveRedirect=0,serialise=0):
  if timing:
    timing=time.time()
  (res,encoding,errs,factory)=runit(en,rns,k,timing,independent,reflect,
                                    reflect2,scanForLocs, useDTD,
                                    topType, topElt, derefNSNs, dw,
                                    control,baseURI,preserveRedirect,serialise)
  if timing:
    sys.stderr.write("Finished:         %6.2f\n"%(time.time()-timing))
  if not encoding:
    encoding='UTF-8'
  if outfile:
    try:
      outf=open(outfile,"w")
    except:
      sys.stderr.write("couldn't open %s for output, falling back to stderr"%
                       outfile)
      outf=sys.stderr
  else:
    outf=sys.stderr
  if encoding!='UTF-8':
    es=" encoding='%s'"%encoding
  else:
    es=""
  outf.write("<?xml version='1.0'%s?>\n"%es)
  if style:
    outf.write( "<?xml-stylesheet type='text/xsl' href='%s'?>\n"%style)
  if enInfo:
    for (k,v) in enInfo.items():
      res.newAttr(k,v)
  if errs:
    res.newAttr("crash","true")
  res.indent("",1)
  outfu=codecs.getwriter('utf8')(outf)
  res.printme(outfu,[],[])
  outf.write("\n")
  if outfile:
    outfu.close()
  else:
    outfu.reset()
  if reflect and not errs:
    dumpInfoset(sys.stdout,reflect,factory,independent,control)
  if reflect2 and not errs:
    dumpInfoset("infoset-after",reflect2,factory,0,control)
  if serialise and not errs:
    serialiseInfoset(sys.stdout,factory.docElt.parent,1)
  if errs:
    return ''.join(map(lambda es:_eJoin(es),errs))
  else:
    return

def _eJoin(s):
  return ''.join(s)

def runit(en,rns=[],k=0,timing=0,independent=0,reflect=0,
          reflect2=0,scanForLocs=0,useDTD=0,topType=None,
          topElt=None,derefNSNs=1,dw=1,control=2,baseURI=None,
          preserveRedirect=0,serialise=0):
  XMLSchemaInit()
  someBugs=0
  btlist=[]

  ss = s = None

  if ((topType is not None) or
      (topElt is not None)):
    qnp=re.compile("^\{(?P<nsName>.*?)\}(?P<localName>.*)$")
  indNorm.reflect.setup()
  if reflect==2:
    import XSV.infoset.altNorm.reflect
    XSV.infoset.altNorm.reflect.setup()
  if en is not None:
    if baseURI is not None:
      ren=urljoin(baseURI,en)
    else:
      ren=en
  else:
    ren=None
  f=SSchema(ren,not useDTD)
  f.derefNSNs=derefNSNs
  f.dontWarn=dw
  f.errors=0
  
  if baseURI is None:
    base = urlunsplit(('file','',os.getcwd().replace('\\','/')+'/','',''))
    if en is not None:
      ren=f.fileNames[0]
  else:
    base = baseURI
    if en is None:
      f.base = f.fileNames[0] = baseURI

  res=Element(None,xsvNS,"xsv")
  f.resElt=res
  res.newAttr("version",vs)
  if topType is not None:
    res.newAttr("forceDocEltType",topType)
    mres=qnp.match(topType)
    if mres is None:
      typeNsName=None
      typeLocalName=topType
    else:
      (typeNsName,typeLocalName)=mres.group('nsName','localName')
  if topElt is not None:
    res.newAttr("forceDocEltName",topElt)
    mres=qnp.match(topElt)
    if mres is None:
      eltNsName=None
      eltLocalName=topElt
    else:
      (eltNsName,eltLocalName)=mres.group('nsName','localName')
  if independent:
    res.newAttr("target","[standalone schema assessment]")
  else:
    res.newAttr("target",ren or "[stdin]")
    
  if independent:
    rns[0:0]=[ren]
  if rns and rns[0] is not None:
    res.newAttr("schemaDocs",' '.join(rns))

  rdn=tempfile.mktemp("xsverrs")
  redirect=open(rdn,"w+")
  savedstderr=os.dup(2)                        # save stderr
  os.dup2(redirect.fileno(),2)
  if independent:
    e=None
    encoding="UTF-8"
    f.docElt=None
  else:
    doc=safeReadXML(ren,res,"target",btlist)
    if doc is not None:
      e=doc.documentElement
      f.docElt=e
      encoding=doc.characterEncodingScheme
      if timing:
        os.write(savedstderr,"target read:      %6.2f\n"%(time.time()-timing))
      if reflect2:
        dumpInfoset("infoset-before",reflect2,f,0,control)
    else:
      encoding=None
      e=None
      res.newAttr('instanceAssessed',"false")
      registerRawErrors(redirect,res,preserveRedirect)
      # put stderr back
      os.dup2(savedstderr,2)
      return (res,None,btlist,f)

  if topElt is not None:
    if ((e.localName!=eltLocalName) or
        (e.namespaceName!=eltNsName)):
      res.newAttr('instanceAssessed',"false")
      registerRawErrors(redirect,res,preserveRedirect)
      ve=res.newDaughter("invalid")
      ve.newText("document element not {%s}%s as required"%(eltNsName,
                                                            eltLocalName))
      addWhere(ve,e.where)
      # put stderr back
      os.dup2(savedstderr,2)
      return (res,None,btlist,f)
      
  if rns:
    s=f.checkinSchema(0,rns[0],base,"command line",useDTD,k)
    if s is not None:
      someBugs=s.buggy or someBugs
    else:
      someBugs=1
    if timing:
      os.write(savedstderr,"schema read:      %6.2f\n"%(time.time()-timing))
    for rn in rns[1:]:
      ffr=f.checkinSchema(0,rn,base,"command line",useDTD,k)
      if ffr is not None:
        someBugs=ffr.buggy or someBugs
      else:
        someBugs=1
      if timing:
        os.write(savedstderr,"schema read:      %6.2f\n"%(time.time()-timing))
      ss=ss or ffr
  if s is None:
    if ss is not None:
      s=ss
    else:
      s = Schema(f,None)
      s.targetNS='##dummy'

  if not independent:
    someBugs=(doSchemaLocs(e,s,res,scanForLocs,
                           ren or base,timing,savedstderr,useDTD,k) or
              someBugs)
    res.newAttr('docElt',"{%s}%s"%(e.namespaceName,e.localName))
    # TODO: remove the following in favour of a general fallback for unknown
    # namespaces in instances?  No, leave it here, to stop validation
    # altogether if we don't have keepGoing
    if (derefNSNs and e.namespaceName and
        (not f.schemas.has_key(e.namespaceName)) and
        (not f.losingNamespaces.has_key(e.namespaceName))):
      nss=f.checkinSchema(e.namespaceName,e.namespaceName,
                          ren or base,"docElt",useDTD,k,e)
      if nss is not None:
        someBugs=nss.buggy or someBugs
      else:
        f.losingNamespaces[e.namespaceName]=1  
      if timing:
        os.write(savedstderr,
                 "schema read:      %6.2f\n"%(time.time()-timing))

  try:
    ecount=f.prepare()
    if timing:
      os.write(savedstderr,"complete schema prepared: %6.2f\n"%(time.time()-timing))
    if independent:
      for ss in f.schemas.values():
        ss.prepare()
      if timing:
        os.write(savedstderr,"individual namespaces prepared: %6.2f\n"%(time.time()-timing))
  except:
    ecount=-1
    btlist.append(traceback.format_exception(sys.exc_type,
                                             sys.exc_value,
                                             sys.exc_traceback))
    pfe=res.newDaughter("bug")
    pfe.newText("validator crash during complete schema preparation")

  if independent:
    kgm="false"
    kg=0
  else:
    kgm="true"
    kg=1
  if ecount or someBugs:
    if ecount<0:
      kg=0
    else:
      if not k:
        kg=0
    if not kg:
     kgm="false"
  if not kg:
    if independent or ecount<0:
      ecount=f.errors
    for sch in f.schemas.values():
      ecount=ecount+sch.errors
    res.newAttr('instanceAssessed',kgm)
    res.newAttr('schemaErrors',str(ecount))
    registerRawErrors(redirect,res,preserveRedirect)
    # put stderr back
    os.dup2(savedstderr,2)
    return (res,encoding,btlist,f)

  if s is None:
    # any one will do
    s = f.sfors
  
  f.errors=0
  if (e is not None) and (s is not None):
    ttdef=None
    if topType is not None:
      ttn=QName(None,typeLocalName,typeNsName or None)
      if s.vTypeTable.has_key(ttn):
        ttdef=s.vTypeTable[ttn]
        # TODO: this will _not_ override xsi:type on the doc elt, pbly should
      else:
        res.newAttr('instanceAssessed',"false")
        registerRawErrors(redirect,res,preserveRedirect)
        ve=res.newDaughter("invalid")
        ve.newText("no definition found for specified top-level type: {%s}%s"%(typeNsName,
                                                              typeLocalName))
        addWhere(ve,e.where)
        # put stderr back
        os.dup2(savedstderr,2)
        return (res,None,btlist,f)
    res.newAttr('instanceAssessed',kgm)
    try:
      validate(e, s, ttdef)
      e.schemaInformation=collectSchemaInfo(f,reflect)
    except:
      btlist.append(traceback.format_exception(sys.exc_type,
                                               sys.exc_value,
                                               sys.exc_traceback))
      pfe=res.newDaughter("bug")
      pfe.newText("validator crash during validation")
    res.newAttr('instanceErrors',str(s.sschema.errors))
    ec=0
    for sch in f.schemas.values():
      ec=ec+sch.errors
    
    if e.__dict__.has_key('assessedType') and e.assessedType:
      t=e.assessedType
      if t.__dict__.has_key('qname') and t.qname:
        tn=unicode(str(t.qname),'utf-8')
      elif t.name:
        tn=t.name
      else:
        tn='[Anonymous]'
      res.newAttr('rootType',tn)
      res.newAttr('validation','strict')
    else:
      res.newAttr('validation','lax')

    res.newAttr('schemaErrors',str(ec))
    registerRawErrors(redirect,res,preserveRedirect)
    # put stderr back
    os.dup2(savedstderr,2)
    return (res,encoding,btlist,f)

def collectSchemaInfo(f,r):
  sforsi=NamespaceSchemaInformation(f.schemas[XMLSchemaNS])
  if r:
    sforsi.schemaComponents.sort(compareSFSComps) # ensure mgds
                                                     # are first
  si=[sforsi,NamespaceSchemaInformation(f.schemas[xsi])]
  for (ns,s) in f.schemas.items():
    if ns not in (XMLSchemaNS,xsi):
      si.append(NamespaceSchemaInformation(s))
  return si

def registerRawErrors(redirect,res,preserveRedirect=0):
  sys.stderr.flush()
  if redirect.tell(): 
    redirect.seek(0)
    ro=res.newDaughter("XMLMessages")
    try:
      o="\n%s"%redirect.read().decode("utf-8")
    except UnicodeError:
      redirect.seek(0)
      o="\n%s"%redirect.read().decode("iso-8859-1") # wrong, but what can you do?
    ro.newText(o)
  redirect.close()
  if not preserveRedirect:
    try:
      os.remove(redirect.name)
    except:
      pass

def serialiseInfoset(fileOrName,document,useSNV):
  if type(fileOrName) is types.FileType:
    close=0
    ff=fileOrName
  else:
    close=1
    ff = open(fileOrName, "w")
  #document.indent("",1)
  ffu=codecs.getwriter('utf8')(ff)
  document.printme(ffu,useSNV)
  if close:
    ffu.close()
  else:
    ffu.reset()


def dumpInfoset(fileOrName,reflect,factory,independent=0,control=2):
  if independent:
    if reflect==2:
      shouldnt("ind reflection of instance")
    r=Document(None)
    e=Element(r,psviSchemaNamespace,"schema")
    r.addChild(e)
    si=collectSchemaInfo(factory,1)
    indNorm.reflect.assignAllUIDs(si)
    indNorm.reflect.reflectAllComponents(e,si)
    e.inScopeNamespaces["i"]=Namespace("i", xsi)
    e.inScopeNamespaces["x"]=Namespace("x", XMLSchemaNS)
    e.inScopeNamespaces[None]=Namespace(None, infosetSchemaNamespace)
  elif factory.docElt is None:
    # fatal schema errors, can't reflect yet
    return
  else:
    r = factory.docElt.parent.reflect(None,control)
  close=0
  r.documentElement.inScopeNamespaces["p"]=Namespace("p",
                                                     psviSchemaNamespace)
  if type(fileOrName) is types.FileType:
    ff=fileOrName
  else:
    close=1
    ff = open(fileOrName, "w")
  r.indent("",1)
  ffu=codecs.getwriter('utf8')(ff)
  r.printme(ffu)
  if close:
    ffu.close()
  else:
    ffu.reset()
  
# $Log: driver.py,v $
# Revision 1.23  2006-11-03 16:50:41  ht
# base URI YET AGAIN
#
# Revision 1.22  2006/08/15 16:12:53  ht
# use xsvNS
#
# Revision 1.21  2005/10/10 14:07:11  ht
# another unicode bug
#
# Revision 1.20  2005/03/16 09:22:20  ht
# move SchemaValidationError
#
# Revision 1.19  2004/10/04 11:34:28  ht
# yet another baseURI patch
#
# Revision 1.18  2004/08/31 15:12:12  ht
# add serialisation support,
# fix baseURI stuff yet again
#
# Revision 1.17  2004/04/01 12:47:02  ht
# add -e flag for preserving captured stderr
#
# Revision 1.16  2003/09/03 13:08:27  ht
# global error count fix?
#
# Revision 1.15  2003/09/01 15:31:45  ht
# support baseURI arg't to runit(AndShow)
#
# Revision 1.14  2003/04/01 20:19:15  ht
# cutAndPaste error
#
# Revision 1.13  2003/03/30 20:05:46  ht
# give command-line control over amount of schema material reflected
#
# Revision 1.12  2003/03/25 14:55:43  ht
# no attr sort on xsv
#
# Revision 1.11  2003/02/14 09:36:24  ht
# add -N switch to supress derefing namespace names
#
# Revision 1.10  2003/01/20 12:22:33  ht
# try to handle Unicode-broken error output
#
# Revision 1.9  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.8  2002/11/08 15:08:04  ht
# change version string stuff
#
# Revision 1.7  2002/11/04 13:33:12  ht
# read error output as utf-8
#
# Revision 1.6  2002/09/23 21:47:52  ht
# move to string methods from string library
#
# Revision 1.5  2002/09/23 13:51:30  ht
# use utf8 codec for output
#
# Revision 1.4  2002/09/02 16:07:22  ht
# remove all globals, not needed anymore
#
# Revision 1.3  2002/09/01 21:21:22  ht
# implement top-level elt, type constraint
#
# Revision 1.2  2002/09/01 19:22:57  ht
# get reflection working,
# start support for explicit type or elt
#
# Revision 1.1  2002/06/28 09:39:17  ht
# XSV as package: top level
#
# Revision 1.106.2.25.2.6  2002/06/15 18:59:35  ht
# separate in and out maps makes refl switching easier
#
# Revision 1.106.2.25.2.5  2002/06/13 21:04:13  ht
# get namespace vars sorted out
#
# Revision 1.106.2.25.2.4  2002/06/12 18:46:20  ht
# restructure in preparation for allowing either normal form to be reflected
#
# Revision 1.106.2.25.2.3  2002/06/10 14:39:33  ht
# conservative about min/max types
#
# Revision 1.106.2.25.2.2  2002/05/25 21:52:46  ht
# accommodate to splitting of XMLSchema.py
#
# Revision 1.106.2.25.2.1  2002/05/24 20:57:41  ht
# accommodate to split in uid assignment,
# chunkedChildren->children
#
# Revision 1.106.2.25  2002/05/14 19:34:51  ht
# accommodate changes to facet storage; implement facets on list and
# union
#
# Revision 1.106.2.24  2002/04/28 13:21:48  ht
# default addrs needed a validity context
#
# Revision 1.106.2.23  2002/04/23 12:15:24  ht
# support -i -r, dump only infoset
#
# Revision 1.106.2.22  2002/01/11 16:40:28  ht
# fix reporting of builtin-root-type
#
# Revision 1.106.2.21  2001/12/07 20:43:15  ht
# typo
#
# Revision 1.106.2.20  2001/12/03 17:29:35  ht
# Remove decl/type args from validate
# Change default for nullable when decl is absent to true
# Use 0 for decl to indicate that decl has been looked for without success
# Change reporting, aborting behaviour of failed xsi:type
# Remove special search for docElt decl
#
# Revision 1.106.2.19  2001/11/29 11:00:00  ht
# catch missing eltDecl in type assignment
#
# Revision 1.106.2.18  2001/11/27 15:33:12  ht
# fix key upward merge bug
#
# Revision 1.106.2.17  2001/11/23 17:04:12  ht
# use decl when found for wildcard
#
# Revision 1.106.2.16  2001/11/21 12:42:06  ht
# restructure FSM label again
#
# Revision 1.106.2.15  2001/11/19 11:28:36  ht
# oops -- back out debugging patches
#
# Revision 1.106.2.14  2001/11/18 20:29:52  ht
# big cleanup of all tests etc. to avoid unnecessary AttributeErrors
#
# Revision 1.106.2.13  2001/11/16 20:43:36  ht
# abandon assignChildTypes in favour of doing it during parsing
#
# Revision 1.106.2.12  2001/11/09 15:45:05  ht
# Distinguish cases where we know what namespace a schema should have
#   from those where we don't
# Notice imports when validating schema documents
# Check QName namespaces against imports when validating schema
# documents
#
# Revision 1.106.2.11  2001/11/01 17:07:43  ht
# fix bug introduced in previous base fix
#
# Revision 1.106.2.10  2001/11/01 13:46:25  ht
# fix various mistakes wrt base for schema docs
#
# Revision 1.106.2.9  2001/10/31 14:31:31  ht
# todo note
#
# Revision 1.106.2.8  2001/10/28 17:39:15  ht
# remove ungrounded use of useDTD
#
# Revision 1.106.2.7  2001/10/26 13:52:34  ht
# include -D in usage
#
# Revision 1.106.2.6  2001/10/26 10:52:36  ht
# use atol, not atoi
#
# Revision 1.106.2.5  2001/10/13 00:58:33  ht
# more bug/error accounting fixup
#
# Revision 1.106.2.4  2001/10/12 22:49:55  ht
# propagate keepGoing info,
# catch backtrace in right place
#
# Revision 1.106.2.3  2001/10/03 20:11:04  ht
# merge in key fix from main line,
# add -D flag to turn on useDTD and propagate it through
#
# Revision 1.106.2.2  2001/09/24 11:57:31  ht
# dont go for ns attrs lookup off an attribute
#
# Revision 1.106.2.1  2001/09/14 11:10:58  ht
# accommodate to factory renaming and related changes
#
# Revision 1.107  2001/09/24 12:24:55  ht
# implement upward merging of keytabs
#
# Revision 1.106  2001/09/03 16:31:12  ht
# update schemaLocs correctly
#
# Revision 1.105  2001/08/30 16:12:04  ht
# accommodate shift to real reference to key/unique by QName
# update some key(ref) messages accordingly
#
# Revision 1.104  2001/08/17 14:38:24  ht
# cover all file opening with redirect,
# only check schemaLoc on root and when about to lose,
# also check ns uri if new and about to lose
#
# Revision 1.103  2001/08/10 20:16:03  ht
# complete regularisation of schema doc processing
#
# Revision 1.102  2001/08/10 17:34:32  ht
# begin regularising all reading of schema files
#
# Revision 1.101  2001/07/07 12:10:19  ht
# handle removal of schemaNormalizedValue on error in list/union/list of
# union cases
#
# Revision 1.100  2001/07/07 11:42:21  ht
# error message bug
#
# Revision 1.99  2001/07/06 10:02:16  ht
# handle attribute default/fixed better, with type and decl
#
# Revision 1.98  2001/06/16 11:56:53  ht
# protect a read
#
# Revision 1.97  2001/06/09 19:14:08  ht
# implement (most of) fixed/default for elements
# support RDDL for command line, xsi:schemaLoc and namespace URIs
#
# Revision 1.96  2001/06/04 16:05:29  ht
# no namespace == no prefix == None
#
# Revision 1.95  2001/05/07 08:38:12  ht
# and again reflect2
#
# Revision 1.94  2001/05/07 08:34:56  ht
# fix reflect2 binding bug
#
# Revision 1.93  2001/04/24 13:29:48  ht
# (PSV)Infoset reorganisation
#
# Revision 1.92  2001/04/12 10:54:04  ht
# raise multiple key error
#
# Revision 1.91  2001/04/10 14:41:49  ht
# fix bug handling unknown xsi attrs
#
# Revision 1.90  2001/04/07 11:19:51  ht
# log target reading crash better
#
# Revision 1.89  2001/04/04 20:56:30  ht
# implement -i switch to do forced schema assessment independent of any instance
#
# Revision 1.88  2001/03/17 12:11:13  ht
# merge v2001 back in to main line
#
# Revision 1.87  2001/02/16 16:38:43  richard
# fix key/keyref/unique field code
#
# Revision 1.86  2001/02/12 11:34:46  ht
# catch unbound prefix in xsi:type
#
# Revision 1.85.2.5  2001/03/15 11:37:59  ht
# check for and rule out use of abstract types
#
# Revision 1.85.2.4  2001/02/24 23:47:56  ht
# handle unbound prefix in xsi:type
# fix typo in assess
#
# Revision 1.85.2.3  2001/02/17 23:33:11  ht
# assignAttrTypes sets a.type to the use if there is one
# so either valueConstraint can be used
#
# Revision 1.85.2.2  2001/02/14 17:01:11  ht
# merge attr use back in to v2001 line
#
# Revision 1.85.2.1.2.1  2001/02/07 17:34:28  ht
# use AttrUse to supply defaults
#
# Revision 1.85.2.1  2001/02/07 14:30:01  ht
# change NS to 2001, implement null->nil
#
# Revision 1.85  2001/02/07 09:23:24  ht
# report low-level failure correctly
#
# Revision 1.84  2001/02/06 14:20:41  ht
# accommodate to earlier XPath construction for fields/selector
#
# Revision 1.83  2001/02/06 11:30:51  ht
# merged infoset-based back to mainline
#
# Revision 1.74.2.26  2001/01/15 14:18:55  ht
# improve wildcard error msg
#
# Revision 1.74.2.25  2001/01/03 19:13:19  ht
# accommodate to change of exception with LTXMLInfoset
#
# Revision 1.74.2.24  2001/01/03 11:57:52  ht
# fix xsi:type bugs
#
# Revision 1.74.2.23  2000/12/23 13:08:21  ht
# fix spelling of whiteSpace,
# add -p file switch for profiling
#
# Revision 1.74.2.22  2000/12/22 18:33:54  ht
# add whitespace processing,
# fix some bugs?
#
# Revision 1.74.2.21  2000/12/21 18:29:38  ht
# accommodate to .facets and real facets
#
# Revision 1.74.2.20  2000/12/16 12:10:29  ht
# add logging of relevant declaration to elt/attr assess
#
# Revision 1.74.2.19  2000/12/14 14:21:59  ht
# fix bug in e-o error msg
#
# Revision 1.74.2.18  2000/12/13 23:30:09  ht
# add -r switch to produce reflected output
#
# Revision 1.74.2.17  2000/12/12 17:33:06  ht
# get builtin-schemas out first, sort AbInitios to the front,
# more details in content-model error messages,
# set null property
#
# Revision 1.74.2.16  2000/12/08 18:08:42  ht
# install schemaInformation on validation root,
# assign type defn as such to typeDefinition property
#
# Revision 1.74.2.15  2000/12/08 15:16:07  ht
# put the docElt in the factory,
# use it for reflection at the end,
# and to implement validationContext
#
# Revision 1.74.2.14  2000/12/07 13:18:42  ht
# work around null vs "" for missing namespace name
#
# Revision 1.74.2.13  2000/12/07 10:20:48  ht
# handle xsi: attrs cleanly
#
# Revision 1.74.2.12  2000/12/06 22:43:11  ht
# make assess a method on Element,
# add one on Attribute,
# refer to the latter from the former
#
# Revision 1.74.2.11  2000/12/06 09:21:05  ht
# add psv infoset namespace URI to reflected docapplyschema.py
#
# Revision 1.74.2.10  2000/12/04 22:31:03  ht
# stubs for schemaNormalizedValue in place
#
# Revision 1.74.2.9  2000/12/04 22:09:00  ht
# remove convert,
# accommodate change to importing XML,
# put attribute verror on right item
#
# Revision 1.74.2.8  2000/12/04 13:30:42  ht
# merge in main line fixes thru 1.82
#
# Revision 1.74.2.7  2000/10/13 12:48:42  richard
# more infoset contributions
#
# Revision 1.74.2.6  2000/10/02 13:33:28  richard
# update values for validity property
#
# Revision 1.74.2.5  2000/09/29 17:18:09  richard
# More towards PSV infoset
#
# Revision 1.74.2.4  2000/09/29 16:45:27  richard
# correct errorCode setting
#
# Revision 1.74.2.3  2000/09/29 16:04:24  richard
# More towards PSV infoset
#
# Revision 1.74.2.2  2000/09/29 14:16:15  ht
# towards PSVI contributions
#
# Revision 1.74.2.1  2000/09/27 17:21:20  richard
# Changes for infoset-based
#
# Revision 1.77  2000/09/28 15:54:50  ht
# schema error count includes all errors, not just those found at prep
# time
#
# Revision 1.76  2000/09/28 15:09:14  ht
# try catching and returning any crashes
#
# Revision 1.75  2000/09/28 08:41:57  ht
# add usage message
# add -o outfile cmd line arg
#
# Revision 1.82  2000/10/31 16:30:47  ht
# validate subordinate elements with eltdecl if available
# return schema error count if not attempting instance validation
#
# Revision 1.81  2000/10/27 15:33:30  ht
# Output timing info if -t on command line
#
# Revision 1.80  2000/10/18 15:54:58  ht
# make effort to check 'fixed' attribute values
#
# Revision 1.79  2000/10/17 13:35:41  ht
# put switch on warnings, default is don't
#
# Revision 1.78  2000/10/17 12:45:15  ht
# try to catch and log all crashes
# replace stale reference to atribute.characters
#
# Revision 1.77  2000/09/28 15:54:50  ht
# schema error count includes all errors, not just those found at prep
# time
#
# Revision 1.76  2000/09/28 15:09:14  ht
# try catching and returning any crashes
#
# Revision 1.75  2000/09/28 08:41:57  ht
# add usage message
# add -o outfile cmd line arg
#
# Revision 1.74  2000/09/27 13:48:47  richard
# Use infoset-like names for slots (now provided in XML.py) to reduce
# differences with infoset-based version.
#
# Revision 1.73  2000/09/27 12:22:22  richard
# correct element.name to element.local in an error message
#
# Revision 1.72  2000/09/26 14:29:36  richard
# Oops, didn't change AbInitio to XMLSchema.AbInitio when moving methods
#
# Revision 1.71  2000/09/26 14:05:28  richard
# Move checkString methods from XMLSchema.py, because they may need to look
# at *instance* in-scope namespaces
#
# Revision 1.70  2000/09/26 13:38:49  ht
# protect against undefined list itemType/union memberType
#
# Revision 1.69  2000/09/23 11:17:31  ht
# merge in CR branch
#

# Revision 1.68  2000/09/23 11:14:26  ht
# towards merge in CR branch
#
# Revision 1.66.2.3  2000/09/21 09:14:33  ht
# property name change
#
# Revision 1.66.2.2  2000/09/11 12:23:27  ht
# Move to branch: more debug in vv crash
#
# Revision 1.68  2000/09/03 15:57:23  ht
# more debug in vv crash

# Revision 1.67  2000/09/11 12:59:09  ht
# allow stdin,
# fix stupid bug missing third schema on command line

# Revision 1.67  2000/08/31 11:48:41  ht
# Direct support for validating lists and unions

# Revision 1.66  2000/08/22 13:11:30  ht
# handle type w/o qname as document validation type
# remove special treatment for AbInitio simple types on elements,
# thereby fixing list validation bug

# Revision 1.66.2.3  2000/09/21 09:14:33  ht
# property name change
#
# Revision 1.66.2.2  2000/09/11 12:23:27  ht
# Move to branch: more debug in vv crash
#
# Revision 1.68  2000/09/03 15:57:23  ht
# more debug in vv crash
#
# Revision 1.67  2000/08/31 11:48:41  ht
# Direct support for validating lists and unions
#

# Revision 1.66  2000/08/22 13:11:30  ht
# handle type w/o qname as document validation type
# remove special treatment for AbInitio simple types on elements,
# thereby fixing list validation bug
#
# Revision 1.65  2000/07/12 09:31:58  ht
# try harder to always have a schema
#
# Revision 1.64  2000/07/10 14:39:02  ht
# prepare for fileinfo to runit
#
# Revision 1.63  2000/07/05 09:05:37  ht
# change name to PyLTXML
#
# Revision 1.62  2000/07/03 09:37:38  ht
# bail out if textonly has elt daughter(s)
# add missing import
#
# Revision 1.61  2000/06/27 09:25:51  ht
# attempt to handle interaction between xsi:type and <any>
#
# Revision 1.60  2000/06/24 11:17:07  ht
# fix bug in unqualified xsi:type
#
# Revision 1.59  2000/06/22 10:31:33  ht
# Bug in unique processing -- broke on missing field
#
# Revision 1.58  2000/06/20 08:07:42  ht
# merge xmlout branches back in to main line
#

# Revision 1.57  2000/05/18 08:01:25  ht
# fix bug in handling of xsi:type
#
# Revision 1.56  2000/05/14 12:19:34  ht
# add context to checkSting calls
#
# Revision 1.55  2000/05/11 11:55:57  ht
# just better handling of lax validation from other branch
#
# Revision 1.54.2.16  2000/06/15 16:03:20  ht
# cover several missing definition cases
#
# Revision 1.54.2.15  2000/06/03 16:29:30  ht
# oops, removing debugging comment
#
# Revision 1.54.2.14  2000/06/03 13:45:55  ht
# catch arity bug in xsi:schemaLoc
#
# Revision 1.54.2.13  2000/05/30 09:35:43  ht
# fix encoding bug when things break down altogether
#
# Revision 1.54.2.12  2000/05/29 08:46:53  ht
# strong enforcement of nullable
# add error codes to all errors
# remove remaining __class__ tests
# change error reporting wrt disallowed content
#
# Revision 1.54.2.11  2000/05/24 20:46:47  ht
# make validateText a method, split across SimpleType and AbInitio
#
# Revision 1.54.2.10  2000/05/24 12:03:28  ht
# modest effort to validate list types
# fix bug in noNamespaceSchemaLocation handling at validation time
#
# Revision 1.54.2.9  2000/05/22 16:11:52  ht
# use OpenStream, take more control of encoding
#
# Revision 1.54.2.8  2000/05/18 17:37:40  ht
# parameterise stylesheet,
# remove formatting from xsv:xsv attributes,
# add namespace decl
#
# Revision 1.54.2.7  2000/05/18 07:59:48  ht
# fix xsi:type validation bug
#
# Revision 1.54.2.6  2000/05/16 16:31:11  ht
# fix bug handling un-typed element declarations == urType validation
#
# Revision 1.54.2.5  2000/05/14 12:29:59  ht
# merge QName checking from main branch
#
# Revision 1.54.2.4  2000/05/12 15:15:01  ht
# process keys even if type is simple,
# add a few codes to get started
#
# Revision 1.54.2.3  2000/05/11 13:59:11  ht
# convert verror/vwarn to produce elements
# eliminate a few special error outputs in favour of special
# sub-elements
#
# Revision 1.54.2.2  2000/05/11 11:14:00  ht
# more error protection
# handle lax recursively and at the start
#
# Revision 1.54.2.1  2000/05/10 11:36:47  ht
# begin converting to XML output
#
# Revision 1.56  2000/05/14 12:19:34  ht
# add context to checkSting calls
#
# Revision 1.55  2000/05/11 11:55:57  ht
# just better handling of lax validation from other branch
#
# Revision 1.54  2000/05/09 14:52:52  ht
# Check for strings in a way that works with or without 16-bit support
#
# Revision 1.53  2000/05/09 12:27:58  ht
# replace our hack with python's url parsing stuff
# make f global for debugging
#
# Revision 1.52  2000/05/05 15:15:45  richard
# wrong (?) elt arg to verror in validateKeyRefs
#
# Revision 1.51  2000/05/04 07:56:35  ht
# Fix typo in opportunistic attribute validation
#
# Revision 1.50  2000/05/01 15:07:00  richard
# bug fix schema -> key.schema
#
# Revision 1.49  2000/05/01 10:05:43  ht
# catch various missing file errors more gracefully
#
# Revision 1.48  2000/04/28 15:40:01  richard
# Implement xsi:null (still don't check nullable)
#
# Revision 1.47  2000/04/28 15:11:23  richard
# allow xsi: attributes on simple type
# moved eltDecl code up validateElement ready for implementing xsi:null
#
# Revision 1.46  2000/04/27 09:41:18  ht
# remove raw types from error messages
#
# Revision 1.45  2000/04/27 09:30:21  ht
# check that inputs are actually schemas,
# remove schema arg to doImport, checkInSchema
#
# Revision 1.44  2000/04/26 13:00:40  ht
# add copyright
#
# Revision 1.43  2000/04/24 20:46:40  ht
# cleanup residual bugs with massive rename,
# rename Any to Wildcard,
# replace AnyAttribute with Wildcard,
# get validation of Wildcard working in both element and attribute contexts
#
# Revision 1.42  2000/04/24 15:08:34  ht
# minor glitches, tiny.xml works again
#
# Revision 1.41  2000/04/24 15:00:09  ht
# wholesale name changes -- init. caps for all classes,
# schema.py -> XMLSchema.py
#
# Revision 1.40  2000/04/24 11:09:17  ht
# make version string universally available
#
# Revision 1.39  2000/04/24 10:06:59  ht
# add version info to message
#
# Revision 1.38  2000/04/24 10:02:39  ht
# change invocation message
#
# Revision 1.37  2000/04/24 09:41:43  ht
# clean up invocation some more, add k arg't to runit
#
# Revision 1.36  2000/04/21 09:32:21  ht
# another dose of resolveURL
# use tiny only if run from command line
#
# Revision 1.35  2000/04/20 22:12:43  ht
# use resolveURL on input, schemaLocs
#
# Revision 1.34  2000/04/20 15:45:08  ht
# better handling of use of ns uri for loc
#
# Revision 1.33  2000/04/20 14:26:59  ht
# merge in private and comp branches
#
# Revision 1.32.2.5  2000/04/20 14:25:54  ht
# merge in comp branch
#
# Revision 1.32.2.4.2.9  2000/04/20 14:22:39  ht
# manage document validation schema creation and search better
#
# Revision 1.32.2.4.2.8  2000/04/20 12:03:21  ht
# Remove a few lingering effectiveTypes
# Allow better for absent types etc.
#
# Revision 1.32.2.4.2.7  2000/04/14 21:18:27  ht
# minor attr names/path changes to track schema
#
# Revision 1.32.2.4.2.6  2000/04/13 23:04:39  ht
# allow for urType as simple type (?)
# track Any->AnyWrap change
#
# Revision 1.32.2.4.2.5  2000/04/12 17:29:37  ht
# begin work on model merger,
#
# Revision 1.32.2.4.2.4  2000/04/11 18:13:17  ht
# interpolate attributeUse between complexType and attributeDeclaration,
# parallel to particle
#
# Revision 1.32.2.4.2.3  2000/04/10 15:48:46  ht
# put modest attribute validation in place
#
# Revision 1.32.2.4.2.2  2000/04/09 16:13:26  ht
# working on complex type, attribute;
# back out component.qname
#
# Revision 1.32.2.4.2.1  2000/04/05 12:12:36  ht
# accommodate changes in schema.py
#
# Revision 1.32.2.4  2000/04/01 18:01:25  ht
# various minor compatibility fixes
#
# Revision 1.32.2.3  2000/03/25 12:12:27  ht
# restructure error handling/reporting;
# allow for switching 208 on and off
#
# Revision 1.32.2.2  2000/03/21 15:57:23  ht
# fix bug in skip,
# allow 208 override
#
# Revision 1.32.2.1  2000/03/20 17:22:52  ht
# better coverage of <any>, including beginning of processcontents
#
# Revision 1.33  2000/03/20 17:20:53  ht
# better coverage of <any>, including beginning of processcontents
#
# Revision 1.32  2000/03/08 15:28:46  ht
# merge private branches back into public after 20000225 release
#
# Revision 1.31.2.3  2000/02/24 23:40:32  ht
# fix any bug
#
# Revision 1.31.2.2  2000/02/21 09:18:13  ht
# bug in <any> handling
#
# Revision 1.31.2.1  2000/02/08 21:43:39  ht
# fork private branch to track internal drafts
# change calling sequence of checkinSchema
#
# Revision 1.31.1.1  2000/02/08 13:54:25  ht
# fork branch for non-public changes
# calling sequence to checkinSchema changed
#
# Revision 1.31  2000/01/13 16:55:42  richard
# Finally do something with xsi:type
#
# Revision 1.30  2000/01/10 17:36:34  richard
# changes for xsi:schemaLocation
#
# Revision 1.29  2000/01/08 23:33:50  ht
# towards support for xsi:schemaLocation
#
# Revision 1.28  2000/01/08 12:07:38  ht
# Change command-line arg sequence in preparation for use of schemaLocation!!!!!
# Add debug printout for schemaLocation for now
#
# Revision 1.27  2000/01/07 17:08:26  richard
# start on xsi:type
#
# Revision 1.26  2000/01/06 14:59:38  ht
# fix command line bug, display args on entry
#
# Revision 1.25  2000/01/06 14:38:56  ht
# detect cross-scope keyref and signal error
#
# Revision 1.24  2000/01/03 17:02:37  ht
# Include result of sub-ordinate key checking in overall result
# Accommodate new calling sequence for xpath.find
# add Log and Id
#
#
