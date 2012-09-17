"""Infosets: Reading of XML docs as LTXMLInfosets us PyLTXML"""

__version__="$Revision: 1.11 $"
# $Id: SchemaFiles.py,v 1.11 2006-08-15 16:17:02 ht Exp $

import traceback
import sys
import time
import os

import XSV
from XSV.validate.verror import verror

import XMLInfoset
xsi = XMLInfoset.xsiNamespace

usePyLTXML = XSV.useLTXML()

if usePyLTXML:
  from PyLTXML import OpenStream, Close, NSL_read, NSL_read_all_bits
  from PyLTXML import NSL_read_namespaces, NSL_read_no_consume_prolog
else:
  from SAXLTXML import OpenStream, Close, NSL_read, NSL_read_all_bits
  from SAXLTXML import NSL_read_namespaces, NSL_read_no_consume_prolog

from LTXMLInfoset import documentFromURI, documentFromFile
locChecked = {}

def safeReadXML(ren,res,goal,btlist,
                fragID=None,targetLocalName=None,idAttr=None,baseURI=None):
  try:
    doc=readXML(ren,fragID,targetLocalName,idAttr,baseURI)
  except:
    pfe=res.newDaughter("bug")
    pfe.newText("validator crash during %s reading"%goal)
    ti=sys.exc_info()
    btlist.append(traceback.format_exception(ti[0],ti[1],ti[2]))
    doc=None
  return doc

def readXML(url,fragID=None,targetLocalName=None,idAttr=None,baseURI=None):
  if url:
    doc = documentFromURI(url,fragID,targetLocalName,idAttr)
  else:
    file = OpenStream(sys.stdin,None,baseURI,0,
                 NSL_read+NSL_read_all_bits+NSL_read_namespaces+
                 NSL_read_no_consume_prolog)
    doc = documentFromFile(file,fragID,targetLocalName,idAttr)
    Close(file)
  return doc

_sln=(None,'schemaLocs')

def doSchemaLocs(elt,schema,res,scanForLocs,base,timing,savedstderr=None,
                 useDTD=0,k=0):
  if locChecked.has_key(elt):
    if not scanForLocs or locChecked[elt]:
      return
  locChecked[elt]=scanForLocs
  schemaLocs = findSchemaLocs(elt,schema,scanForLocs)
  someBugs=0
  if schemaLocs:
    showLocs='; '.join(map(lambda p:"%s -> %s"%(p[0] or 'None',p[1]),
                             schemaLocs))
    try:
      av=res.attributes[_sln].normalizedValue
      res.attributes[_sln].normalizedValue="%s; %s"%(av,showLocs)
    except KeyError:  
      res.newAttr('schemaLocs',showLocs)
  for (ns, sl) in schemaLocs:
    sls=schema.sschema.checkinSchema(ns, sl,base,"schemaLoc",useDTD,k,elt)
    if sls is not None:
      someBugs=sls.buggy or someBugs
    else:
      someBugs=1
    if timing:
      os.write(savedstderr,"schema read:      %6.2f\n"%(time.time()-timing))
  return someBugs

def findSchemaLocs(element,schema,recurse=1):
  pairs = []
  for a in element.attributes.values():
    if a.namespaceName == xsi:
      if a.localName == "schemaLocation":
        scls=a.normalizedValue.split()
        while scls:
          if len(scls)>1:
            pairs.append((scls[0], scls[1]))
          else:
            verror(element,"xsi:schemaLocation must be a list with an even number of members: %s"%a.normalizedValue.split(),schema,"???")
          scls=scls[2:]
      elif a.localName == "noNamespaceSchemaLocation":
        pairs.append((None,a.normalizedValue))
  if recurse:
    for c in element.children:
      if isinstance(c, XMLInfoset.Element):
        scl=findSchemaLocs(c,schema)
        if scl:
          pairs = pairs + scl
  return pairs
  

# $Log: SchemaFiles.py,v $
# Revision 1.11  2006-08-15 16:17:02  ht
# fall back to pull-SAX if PyLTXML not available
#
# Revision 1.10  2006/05/10 14:00:28  ht
# use LTXML or SAX as appropriate
#
# Revision 1.9  2004/04/01 12:53:19  ht
# keep track of schemaLoc checked elts to avoid duplicated effort
#
# Revision 1.8  2003/09/01 15:35:10  ht
# switch to OpenStream so we can use baseURI for stdin
#
# Revision 1.7  2003/06/30 21:54:15  ht
# support fragid in schemaLoc, including self
#
# Revision 1.6  2002/10/08 21:12:17  ht
# another typo
#
# Revision 1.5  2002/10/08 21:10:05  ht
# minor
#
# Revision 1.4  2002/10/08 20:50:07  ht
# minor pychecker-discoverd fixes
#
# Revision 1.3  2002/09/23 21:45:03  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:11:22  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 10:23:27  ht
# infoset basics
#
