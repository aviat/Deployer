"""Infosets: Expose (Py)LTXML as vanilla infoset"""

__version__="$Revision: 1.2 $"
# $Id: SAXMLInfoset.py,v 1.2 2006-05-10 13:56:19 ht Exp $

from XMLInfoset import *

from xml.sax.saxutils import prepare_input_source
from xml.sax import make_parser
from xml.sax.handler import feature_validation, feature_namespaces
from xml.sax.handler import feature_namespace_prefixes, ContentHandler

import types

Parsers=["xml.sax.drivers2.drv_pyexpat"]

def documentFromURI(uri,fragID=None,targetLocalName=None,idAttr=None):
  if type(uri)==types.UnicodeType:
    uri=uri.encode('utf_8')
  source = prepare_input_source(uri)
  doc = documentFromSource(source,fragID,targetLocalName,idAttr)
  # who closes the input?
  return doc

def documentFromSource(source,fragID=None,targetLocalName=None,idAttr=None,
                     includedDefaultedAttrs=1):
  if not includedDefaultedAttrs:
    raise Exception, "Oops, excluding defaulted attributes not supported yet"
  d = Document(None)
  p = make_parser(Parsers)
  p.setFeature(feature_namespaces,True)
  #p.setFeature(feature_validation,True)
  p.setFeature(feature_namespace_prefixes,True)
  #try:
    # property document-xml-version is defined by SAX, but not obviously supported by xml.sax.handler
    # property document_encoding _is_ supported by xml.sax.handler
    #d.version = file.XMLVersion
  #except error:
  d.version = "1.0"
  #ents = file.doctype.entities
  #for ename in ents.keys():
    #pass                                # for now
  handler=SAXMLInfoset(d,includedDefaultedAttrs,
                       fragID,targetLocalName,idAttr)
  #handler.loc=p # setDocumentLocator never called by "xml.sax.drivers2.drv_xmlproc"
  p.setContentHandler(handler)
  p.parse(source)
  return d

class SAXMLInfoset(ContentHandler):
  def __init__(self,doc,ida,fragID,targetLocalName,idAttr):
    ContentHandler.__init__(self)
    self.stack = []
    self.current = doc
    doc.inScopeNamespaces = None
    self.ida = ida
    self.fragID = fragID
    self.targetLocalName = targetLocalName
    self.idAttr = idAttr
    self.inscopens = {"xml":
                      Namespace("xml",
                                "http://www.w3.org/XML/1998/namespace")}
    self.nsDirty = False
    if fragID is not None:
      self.skipping = 1
    else:
      self.skipping = 0

  def setDocumentLocator(self,loc):
    # Not called by "xml.sax.drivers2.drv_xmlproc" :-(
    self.loc=loc

  def startElementNS(self,name,qname,attrs):
    if self.skipping is 2:
      return
    if self.skipping is 1:
      # looking for hit
      if name[1]==self.targetLocalName:
        try:
          val = attrs.getValueByQName(self.idAttr)
        except KeyError:
          val = None
        if val == self.fragID:
          # got it, current better be doc
          e = self.elementFromEvent(name,qname,attrs)
          self.skipping = e
        else:
          return
      else:
        return
    else:
      e = self.elementFromEvent(name,qname,attrs)
    self.current.addChild(e)
    self.stack.append(self.current)
    self.current=e
    self.nsDirty=False
    
  def endElementNS(self,name,qname):
    # should be position of end tag. . .
    if self.skipping is 2 or self.skipping is 1:
      return
    self.current.where2 = ('unnamed entity',self.loc.getLineNumber(),self.loc.getColumnNumber(),
                           self.loc.getSystemId())
    #print ('>', name, self.current.where2)
    if self.skipping is self.current:
      # end of frag we were to focus on
      self.skipping = 2
    self.current=self.stack.pop()
    self.inscopens = self.current.inScopeNamespaces
    self.nsDirty=False

  def startPrefixMapping(self,prefix,uri):
    #print ('bind',prefix,uri)
    if self.skipping is 2:
      return
    try:
      ns = self.inscopens[prefix]
      if (ns.prefix==prefix and
          ns.namespaceName==uri):
        return
    except KeyError:
      pass
    if not self.nsDirty:
      self.inscopens=self.inscopens.copy()
      self.nsDirty=True
    self.inscopens[prefix]=Namespace(prefix,uri)

  def characters(self,content):
    if self.skipping is 2 or self.skipping is 1:
      return
    t = Characters(self.current, content, False)
    t.where = ('unnamed entity',self.loc.getLineNumber(),self.loc.getColumnNumber()+1,self.loc.getSystemId())
    self.current.addChild(t)

  def ignorableWhitespace(self,content):
    if self.skipping is 2:
      return
    t = Characters(self.current, content, True)
    t.where = ('unnamed entity',self.loc.getLineNumber(),self.loc.getColumnNumber()+1,self.loc.getSystemId())
    self.current.addChild(t)

  def elementFromEvent(self,name,qname,atts):
    nsname = name[0]
    localname = name[1]
    cpos = qname.find(':')
    if cpos<0:
      prefix = None
    else:
      prefix=qname[0:cpos]
    baseuri = self.loc.getSystemId()                        # XXX change when xml:base implemented
    #if file.doctype.elementTypes.has_key(bit.label):
#    spec = file.doctype.elementTypes[bit.label]
#  else:
    spec = None
    e = Element(self.current, nsname, localname, prefix, baseuri, self.inscopens)
    e.originalName = qname
    e.where = ('unnamed entity',self.loc.getLineNumber(),self.loc.getColumnNumber()+1,baseuri)
    #print ('<', qname, e.where)
    for aname in atts.getQNames():
      cpos = aname.find(':')
      if cpos<0:
        prefix = None
      else:
        prefix=aname[0:cpos]
      (ansname , alocalname) = atts.getNameByQName(aname)
      a = Attribute(e, ansname, alocalname, prefix, atts.getValueByQName(aname))
      e.addAttribute(a)
      a.originalName = aname
    return e

# $Log: SAXMLInfoset.py,v $
# Revision 1.2  2006-05-10 13:56:19  ht
# works for regression test
#
# Revision 1.1  2006/05/10 11:08:57  ht
# converted from LTXMLInfoset
#
# Revision 1.8  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.7  2004/07/01 13:19:06  ht
# pass through XML version if available
#
# Revision 1.6  2003/09/01 15:40:01  ht
# allow non-build of defaulted attrs
#
# Revision 1.5  2003/06/30 21:54:15  ht
# support fragid in schemaLoc, including self
#
# Revision 1.4  2002/11/04 13:35:04  ht
# protect against unicode uri name
#
# Revision 1.3  2002/10/08 20:50:07  ht
# minor pychecker-discoverd fixes
#
# Revision 1.2  2002/09/23 21:45:03  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 10:23:27  ht
# infoset basics
#
