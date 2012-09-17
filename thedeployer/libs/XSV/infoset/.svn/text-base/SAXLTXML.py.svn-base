"""Simulate PyLTXML using SAX pull"""

__version__="$Revision: 1.3 $"
# $Id: SAXLTXML.py,v 1.3 2007-02-16 14:41:14 ht Exp $

from PullFromSAX import ASyncPullFromSAX
from xml.sax.handler import feature_validation, feature_namespaces
from xml.sax.handler import feature_namespace_prefixes, ContentHandler
from xml.sax.saxutils import prepare_input_source as p_i_s
import sys
import os

Parsers=["xml.sax.drivers2.drv_pyexpat"]

NSL_read = 0x01
NSL_read_all_bits = 0x02
NSL_read_strict = 0x04
NSL_read_no_expand = 0x08
NSL_read_no_consume_prolog = 0x10
NSL_read_no_normalise_attributes = 0x20
NSL_read_declaration_warnings = 0x40
NSL_read_validate = 0x80
NSL_read_namespaces = 0x10000
NSL_read_defaulted_attributes = 0x20000
NSL_read_relaxed_any = 0x40000
NSL_read_allow_undeclared_nsattributes = 0x80000
NSL_read_flags = 0xf00ff

class SAXLTXML(ASyncPullFromSAX):
  """Most of the PyLTXML functions are dispatched to method calls on
  instances of this, which are returned by Open and friends"""
  seenValidityError = False
  def __init__(self,source,features):
    #print ('S',source,features)
    ASyncPullFromSAX.__init__(self,source,BitMaker,features,Parsers)

  def __getattr__(self,name):
    if name=='doctype':
      self.doctype=Doctype()
      return self.doctype
    elif name=='where':
      #      print ('w',self,self.worker,dir(self.worker))
      ln = None
      while ln is None:
        try:
          ln=self.worker.locator.getLineNumber()
        except AttributeError:
          # print ('ww',self.worker,dir(self.worker))
          self.worker.ready.wait(0.1)
      col = self.worker.locator.getColumnNumber()
      if col is not None:
        col = col+1 # why different from PyLTXML???
      return ("unnamed entity",
              ln,
              col,
              self.worker.source.getSystemId()) # XYZZY -- broken for gen ent
    elif name=='XMLVersion':
      raise SXLError("no such property: %s"%name)
    else:
      raise AttributeError("PullFromSAX instance has no attribute '%s'"%name)

  def getNextBit(self):
    return self.getEvent()

def Open(uri,flags,dtdHack=None):
  # Ignore flags for now
  s = SAXLTXML(prepare_input_source(uri),
               {feature_namespaces:True,
                #feature_validation:True,
                feature_namespace_prefixes:True})
  return s

def OpenStream(file,flags,baseURI):
  # Ignore flags for now
  s = SAXLTXML(prepare_input_source(file,baseURI),
               {feature_namespaces:True,
                #feature_validation:True,
                feature_namespace_prefixes:True})
  return s

def GetNextBit(s):
  return s.getNextBit()

def Close(s):
  pass

def ItemActualAttributesNS(item):
  return item.aAttrs

def GetAttrVal(item,name):
  return item.getAttrVal(name)

NSL_bad=0
NSL_start_bit=1
NSL_end_bit=2
NSL_empty_bit=3
NSL_eof_bit=4
NSL_text_bit=5
NSL_pi_bit=6
NSL_doctype_bit=7
NSL_comment_bit=8
# the rest of these are Item types
NSL_inchoate=9
NSL_non_empty=10
NSL_empty=11
NSL_free=12

class BitMaker(ContentHandler):

  def startElementNS(self,name,qname,attrs):
    self.deliver(StartBit(name,qname,attrs,self))

  def endElementNS(self, name, qname):
    self.deliver(EndBit(name,qname))

  def setDocumentLocator(self,locator):
    # print ('sl',locator,self)
    self.locator=locator

  def startDocument(self):
    self.nsdict = {"xml":"http://www.w3.org/XML/1998/namespace"}
    self.nsbStack = {}

  def startPrefixMapping(self, prefix, uri):
    # print ('spm',prefix,uri)
    try:
      self.nspush(prefix)
    except KeyError:
      pass
    if uri is None:
      # print ('ubp',prefix,self.nsdict[prefix])
      del self.nsdict[prefix]
    else:
      self.nsdict[prefix]=uri

  def endPrefixMapping(self, prefix):
    # print ('epm',prefix)
    try:
      self.nsdict[prefix] = self.nspop(prefix)
    except KeyError:
      del self.nsdict[prefix]

  def characters(self, content):
    self.deliver(TextBit(content))

  def nspush(self,prefix):
    # save current binding, if there is one
    # sys.stderr.write("nspush: %s\n"%prefix)
    pre = self.nsdict[prefix]
    try:
      self.nsbStack[prefix].append(pre)
    except KeyError:
      self.nsbStack[prefix]=[pre]
    # sys.stderr.write(" pushed: %s\n"%self.nsbStack[prefix])
    # sys.stderr.flush()

  def nspop(self,prefix):
    # sys.stderr.write("nspop: %s\n"%prefix)
    # sys.stderr.flush()
    # sys.stderr.write(" popping: %s %s\n"%(prefix,self.nsbStack[prefix]))
    # sys.stderr.flush()
    stk = self.nsbStack[prefix]
    res = stk.pop()
    if stk==[]:
      del self.nsbStack[prefix]
    return res
  
class Doctype:
  entities={}
  elementTypes={}
  doctypeStatement=None

class Bit:
  pass

class StartBit(Bit):
  type=NSL_start_bit

  def __init__(self,name,qname,attrs,worker):
    # print ('sb',name,qname)
    self.nsuri=name[0]
    self.llabel=name[1]
    self.label=qname
    if qname is not self.llabel:
      self.prefix = qname[0:qname.find(':')]
    else:
      self.prefix = None
    self.name=name
    self.qname=qname
    self.attrs=attrs
    self.item=self
    self.worker=worker

  def __getattr__(self,name):
    if name=="nsdict":
      self.nsdict=self.worker.nsdict.copy()
      return self.nsdict
    if name=="aAttrs":
      self.aAttrs=[]
      for aname in self.attrs.getQNames():
        (ns,ln)=self.attrs.getNameByQName(aname)
        self.aAttrs.append((aname,self.attrs.getValueByQName(aname),ns,ln))
      return self.aAttrs
    raise AttributeError("Item has no attribute '%s'"%name)

  def getAttrVal(self,name):
    try:
      return self.attrs.getValueByQName(name)
    except KeyError:
      return

class EndBit(Bit):
  type=NSL_end_bit

  def __init__(self,name,qname):
    # print ('eb',name,qname)
    self.llabel=name[1]

class TextBit(Bit):
  type=NSL_text_bit

  def __init__(self,body):
    # print ('tb',body[0:min(10,len(body))])
    self.body=body

class SXLError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def prepare_input_source(url,base=""):
  # work around egregious bug in nturl2path
  hack=False
  if os.name == 'nt':
    if url[0:5]=='file:' and url[9]==':':
      url="file:///"+url[8]+"|"+url[10:]
      hack=True
    elif base[0:5]=='file:' and base[9]==':':
      base="file:///"+base[8]+"|"+base[10:]
      hack=True
    res=p_i_s(url,base)
    u=res.getSystemId()
    if hack and u[0:5]=='file:' and u[9]=='|':
      res.setSystemId("file:///"+u[8]+":"+u[10:])
    return res
  else:
    return p_i_s(url,base)
