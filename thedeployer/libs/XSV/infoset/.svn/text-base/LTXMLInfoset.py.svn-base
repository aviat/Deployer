"""Infosets: Expose (Py)LTXML as vanilla infoset"""

__version__="$Revision: 1.10 $"
# $Id: LTXMLInfoset.py,v 1.10 2006-08-15 16:17:02 ht Exp $

from XMLInfoset import *
import XSV

usePyLTXML = XSV.useLTXML()

if usePyLTXML:
  from PyLTXML import Open, Close, NSL_read, NSL_read_all_bits
  from PyLTXML import NSL_read_namespaces, NSL_read_no_consume_prolog
  from PyLTXML import GetNextBit, ItemActualAttributesNS, GetAttrVal, error
  NSL_bad="bad"
  NSL_start_bit="start"
  NSL_empty_bit="empty"
  NSL_end_bit="end"
  NSL_pi_bit="pi"
  NSL_comment_bit="comment"
  NSL_text_bit="text"
else:
  from SAXLTXML import Open, Close, NSL_read, NSL_read_all_bits
  from SAXLTXML import NSL_read_namespaces, NSL_read_no_consume_prolog
  from SAXLTXML import GetNextBit, ItemActualAttributesNS, GetAttrVal
  from SAXLTXML import SXLError as error
  from SAXLTXML import NSL_bad, NSL_start_bit, NSL_empty_bit, NSL_pi_bit
  from SAXLTXML import NSL_comment_bit, NSL_end_bit, NSL_text_bit

import types

def documentFromURI(uri,fragID=None,targetLocalName=None,idAttr=None):
  if type(uri)==types.UnicodeType:
    uri=uri.encode('utf_8')
  file = Open(uri, NSL_read+NSL_read_all_bits+NSL_read_namespaces+NSL_read_no_consume_prolog)
  doc = documentFromFile(file,fragID,targetLocalName,idAttr)
  Close(file)
  return doc

def documentFromFile(file,fragID=None,targetLocalName=None,idAttr=None,
                     includedDefaultedAttrs=1):
  d = Document(None)
  # d.baseURI = file.baseURI  XXX
  try:
    d.version = file.XMLVersion
  except error, e:
    d.version = "1.0"
  ents = file.doctype.entities
  for ename in ents.keys():
    pass                                # for now
#  docent = EntityDeclaration("DocumentEntity", None, None, None, None, None, None, file.doctype.xencoding)
#  d.addEntityDeclaration(docent)
  w = file.where
  b = GetNextBit(file)
  # print ('b',b.type,targetLocalName,fragID)
  while b:
    if  b.type == NSL_bad:
      raise Exception, "parse error"
    elif b.type == NSL_pi_bit:
      pass                            # XXX
    elif b.type == NSL_comment_bit:
      pass                            # XXX
    elif b.type == NSL_start_bit or b.type == NSL_empty_bit:
      if fragID is None:
        d.addChild(elementFromBit(d, b, file, w, includedDefaultedAttrs))
        return d
      elif (b.llabel==targetLocalName and
            GetAttrVal(b.item,idAttr)==fragID):
        d.addChild(elementFromBit(d, b, file, w, includedDefaultedAttrs))
        b = GetNextBit(file)
        while b:
          # print ('b2',b.type)
          if  b.type == NSL_bad:
            raise Exception, "parse error"
          b = GetNextBit(file)
        return d
    w = file.where
    b = GetNextBit(file)
    # print ('b3',b.type)
  # shouldn't be possible to fall out without errror
  raise Exception, "oops, ran off end of XML file"

def elementFromBit(parent, bit, file, w, includedDefaultedAttrs):
  # print 'efb'
  nsname = bit.nsuri
  localname = bit.llabel
  prefix = bit.prefix
  baseuri = w[3]                        # XXX change when xml:base implemented
  inscopens = None
  if isinstance(parent,Element) and parent.inScopeNamespaces is not None:
    pis=parent.inScopeNamespaces
    for n in bit.item.nsdict.keys():
      if not pis.has_key(n):
        break
    else:
      # can share with parent
      inscopens=0
  if inscopens is None:
    inscopens = {}
    for n in bit.item.nsdict.keys():
      inscopens[n] = Namespace(n, bit.item.nsdict[n]) # XXX
  if file.doctype.elementTypes.has_key(bit.label):
    spec = file.doctype.elementTypes[bit.label]
  else:
    spec = None
  e = Element(parent, nsname, localname, prefix, baseuri, inscopens)
  e.originalName = bit.label
  e.where = w                           # position of start tag
  
  atts = ItemActualAttributesNS(bit.item)
  for (aname,avalue,ansname,alocalname) in atts:
    if aname is not alocalname:
      prefix = aname[0:aname.find(':')]
    else:
      prefix = None
    a = Attribute(e, ansname, alocalname, prefix, avalue)
    e.addAttribute(a)
    a.originalName = aname
  if spec and includedDefaultedAttrs:
    defaulted_attrs = []
    for aspec in spec.attrDefns.values(): # find types and default values
      for a in e.attributes.values():
        if a.originalName == aspec.name:
          a.attributeType = aspec.type
          if aspec.defType == "NONE" or aspec.defType == "#FIXED":
            a.default = aspec.defValue
          break
      else:
        # attribute not present, see if there is a default
        # (but not for namespace attrs, they have already been handled)
        if aspec.name == "xmlns" or aspec.name[0:6] == "xmlns:":
          pass
        elif aspec.defType == "NONE" or aspec.defType == "#FIXED":
          a = makeDefaultAttribute(e, aspec, inscopens or e.inScopeNamespaces)
          if a:
            defaulted_attrs.append(a)
    for a in defaulted_attrs:
      e.addAttribute(a)

  if bit.type == NSL_empty_bit:
    e.where2 = e.where
    return e

  w = file.where
  b = GetNextBit(file)
  while b.type != NSL_end_bit:
    if  b.type == NSL_bad:
      raise Exception, "parse error"
    elif b.type == NSL_pi_bit:
      pass                            # XXX
    elif b.type == NSL_comment_bit:
      pass                            # XXX
    elif b.type == NSL_start_bit or b.type == NSL_empty_bit:
      e.addChild(elementFromBit(e, b, file, w, includedDefaultedAttrs))
    elif b.type == NSL_text_bit:
      t = Characters(e, b.body, (spec or 0) and spec.type == "ELEMENT")
      t.where = w
      e.addChild(t)
    w =  file.where
    b = GetNextBit(file)

  e.where2 = w                          # position of end tag
  
  return e

def makeDefaultAttribute(element, spec, inscopens):
  parts = spec.name.split(":")
  nparts = len(parts)
  if nparts > 2 or parts[0] == "" or (nparts == 2 and parts[1] == ""):
    return None                         # ignore namespace-bad attrs
  if nparts == 2:
    prefix = parts[0]
    local = parts[1]
    if not inscopens.has_key(prefix):
      return None                       # ditto (parser will have reported it)
    ns = inscopens[prefix].namespaceName
  else:
    local = parts[0]
    ns = None
    prefix = None
  a = Attribute(element, ns, local, prefix, spec.defValue, 0, spec.type)
  a.originalName = spec.name
  return a

# $Log: LTXMLInfoset.py,v $
# Revision 1.10  2006-08-15 16:17:02  ht
# fall back to pull-SAX if PyLTXML not available
#
# Revision 1.9  2006/05/10 14:00:05  ht
# only import needful bits from PyLTXML, prelude to replacing
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
