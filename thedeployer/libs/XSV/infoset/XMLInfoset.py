"""Infosets: Vanilla infoset classes and instance vars"""

__version__="$Revision: 1.11 $"
# $Id: XMLInfoset.py,v 1.11 2006-08-15 16:17:02 ht Exp $

import types
import re

infosetSchemaNamespace = "http://www.w3.org/2001/05/XMLInfoset"
xsiNamespace = "http://www.w3.org/2001/XMLSchema-instance"

class InformationItem:
  alwaysNamed=0
  def printme(self, file, namespaces={}):
    file.write("<!-- XXX %s XXX -->" % self)

class Document(InformationItem):
  
  def __init__(self, baseURI, encoding=None, standalone=None, version=None):
    self.children = []
    self.documentElement = None
    self.notations = []
    self.unparsedEntities = []        
    self.baseURI = baseURI
    self.characterEncodingScheme = encoding
    self.standalone = standalone
    self.version = version
    self.allDeclarationsProcessed = 1
    
  def addChild(self, child):
    if isinstance(child, Element):
      if self.documentElement:
        raise Exception, "attempt to add second Element child to Document"
      else:
        self.documentElement = child
    self.children.append(child)

  def addNotation(self, notation):
    self.notations.append(notation)

  def addUnparsedEntity(self, entity):
    self.unparsedEntities.append(entity)

  def printme(self, file,useSNV=0,firstAttrs=['name','ref','type','minOccurs'],
              lastAttrs=['id']):
    if self.version:
      file.write("<?xml version='%s'?>\n" % self.version)
    self.documentElement.printme(file,firstAttrs,lastAttrs,{},0,useSNV)
    file.write("\n")

  def indent(self, indent="",indentMixed=0):
    self.documentElement.indent(indent,indentMixed)
    
class Element(InformationItem):
  indented=None
  attrStart=None

  def __init__(self, parent, namespaceName, localName, prefix=None, baseURI=0, inScopeNamespaces=0):
    self.parent = parent
    self.namespaceName = namespaceName
    self.localName = localName
    self.prefix = prefix
    self.children = []
    self.attributes = {}
    if baseURI == 0:
      if isinstance(parent, InformationItem):
        self.baseURI = parent.baseURI
      else:
        self.baseURI = None
    else:
      self.baseURI = baseURI
    self.baseURI = baseURI
    self.namespaceAttributes = {}
    if inScopeNamespaces == 0:
      if isinstance(parent, Element):
        self.inScopeNamespaces = parent.inScopeNamespaces
      else:
        self.inScopeNamespaces = {"xml":
                                  Namespace("xml",
                                       "http://www.w3.org/XML/1998/namespace")}
        if namespaceName is not None:
          if prefix!="xml":
            self.inScopeNamespaces[prefix]=Namespace(prefix,namespaceName)
    else:
      self.inScopeNamespaces = inScopeNamespaces
      
  def addChild(self, child):
    self.children.append(child)

  def addAttribute(self, attr):
    self.attributes[(attr.namespaceName, attr.localName)] = attr

  def addNamespaceAttribute(self, attr):
    self.namespaceAttributes[(attr.namespaceName, attr.localName)] = attr

  def newDaughter(self,name):
    elt=Element(self,self.namespaceName,name)
    self.addChild(elt)
    return elt

  def newAttr(self,name,val):
    self.addAttribute(Attribute(self,None,name,None,val))

  def newText(self,chars):
    self.addChild(Characters(self,chars))

  def printme(self, file, firstAttrs, lastAttrs, namespaces={},
              printXMLNS=0, useSNV=0):
    nsname = self.namespaceName
    
    ans = self.attributes.keys()
    ans.sort(lambda n1,n2,f=firstAttrs,l=lastAttrs:orderAttrs(n1[1],n2[1],f,l))

    # do we need any namespace attributes ...
    ns = {}
    count = len(namespaces)
    # ... for in-scope namespaces?
    # sys.stderr.write("<%s\n"%self.localName)
    for inns in self.inScopeNamespaces.values():
      # sys.stderr.write(" %s : %s\n"%(inns.prefix,inns.namespaceName))
      if namespaces.has_key(inns.prefix):
        if namespaces[inns.prefix].namespaceName == inns.namespaceName:
          pass                          # already got it
        else:
          ns[inns.prefix] = inns
          count = count+1
      else:
        ns[inns.prefix] = inns
        count = count+1
    # ... to unbind?
    for prefix in namespaces.keys():
      if not self.inScopeNamespaces.has_key(prefix):
        ns[prefix]=Namespace(prefix,"")
    # ... for the element name?
    if nsname:
      eltBinding=getBinding(namespaces,nsname,1)
      if eltBinding is not None:
        eltPrefix = eltBinding.prefix
      else:
        eltBinding=getBinding(ns,nsname,1)
        if eltBinding is not None:
          eltPrefix = eltBinding.prefix
        else:
          eltPrefix = "ns%d" % count
          ns[eltPrefix] = Namespace(eltPrefix, nsname)
          count = count+1
    # ... for the attributes?
    for a in self.attributes.values():
      ansname = a.namespaceName
      if ansname is not None:
        attrBinding=getBinding(namespaces,ansname)
        if attrBinding is not None:
          attrPrefix = attrBinding.prefix
        else:
          attrBinding=getBinding(ns,ansname)
          if attrBinding is not None:
            attrPrefix = attrBinding.prefix
          else:
            attrPrefix = "ns%d" % count
            ns[attrPrefix] = Namespace(attrPrefix, ansname)
            count = count+1
        
    if ns:
      namespaces = namespaces.copy()
      for n in ns.values():
        if n.namespaceName=="":
          del namespaces[n.prefix]
        else:
          # sys.stderr.write("%s -> %s\n"%(n.prefix,n.namespaceName))
          namespaces[n.prefix] = n

    if nsname:
      if eltPrefix is None:
        nms="<%s" % self.localName
      else:
        nms="<%s:%s" % (eltPrefix, self.localName)
    else:
      nms="<%s" % self.localName
    file.write(nms)
    if self.indented is not None:
      self.indented=self.indented+(" "*(len(nms)))
      self.attrStart=len(self.indented)

    for n in ns.values():
      n.printme(file,self,printXMLNS)
      
    for an in ans:
      self.attributes[an].printme(file, namespaces, useSNV)

    if ((not self.children) and
        ((not useSNV) or self.schemaNormalizedValue is None)):
      file.write("/>")
      return
    file.write(">")

    if useSNV and self.schemaNormalizedValue is not None:
      text = escape(self.schemaNormalizedValue, 0)
      file.write(text)
    else:
      for child in self.children:
        child.printme(file, firstAttrs, lastAttrs, namespaces, printXMLNS, useSNV)

    if nsname:
      if eltPrefix == None:
        file.write("</%s>" % self.localName)
      else:
        file.write("</%s:%s>" % (eltPrefix, self.localName))
    else:
      file.write("</%s>" % self.localName)

  # A hack to indent nested elements by inserting whitespace
  def indent(self, indent="",indentMixed=0):
    self.indented=indent
    if not self.children:
      return
    elementOnly=1
    textOnly=1
    for c in self.children:
      if (isinstance(c, Character) and (not c.elementContentWhitespace) and
          c.characterCode in (9,10,32)):
        c.elementContentWhitespace=1
      elif (isinstance(c, Characters) and (not c.elementContentWhitespace) and
            c.allWhite()):
        c.elementContentWhitespace=1
    for c in self.children:
      if isinstance(c, Element):
        textOnly=0
        if not elementOnly:
          break
      elif isinstance(c, Character) or isinstance(c, Characters):
        if not c.elementContentWhitespace:
          elementOnly=0
          if not textOnly:
            break
    if textOnly or ((not elementOnly) and (not indentMixed)):
      return
    old = self.children
    self.children = []
    for c in old:
      if not ((isinstance(c, Character) or isinstance(c, Characters)) and
              c.elementContentWhitespace):
        self.addChild(Characters(self, "\n"+indent+"  ", 1))
      if isinstance(c, Element):
        c.indent(indent+"  ",indentMixed)
      if (isinstance(c,Element) or
          (not c.elementContentWhitespace)):
        self.addChild(c)
      elif (isinstance(c,Characters) and c.characters.find("\n\n")>-1):
        self.addChild(Characters(self,"\n",1))
    self.addChild(Characters(self, "\n"+indent, 1))      
    
class Character(InformationItem):

  def __init__(self, parent, characterCode, elementContentWhitespace=0):
    self.parent = parent
    self.characterCode = characterCode
    self.elementContentWhitespace = elementContentWhitespace

# sequence of characters represented as string
class Characters(InformationItem):

  def __init__(self, parent, characters, elementContentWhitespace=0):
    self.parent = parent
    self.characters = characters
    self.elementContentWhitespace = elementContentWhitespace

  def printme(self, file, firstAttrs, lastAttrs, namespaces={}, printXMLNS=0, useSNV=0):
    text = escape(self.characters, 0)
    file.write(text)

  def allWhite(self):
    for c in self.characters:
      if c not in ' \t\n':
        return 0
    return 1
    
class Attribute(InformationItem):

  def __init__(self, ownerElement, namespaceName, localName, prefix, normalizedValue, specified=1, attributeType=None):
    self.ownerElement = ownerElement
    self.namespaceName = namespaceName
    self.localName = localName
    self.prefix = prefix
    self.normalizedValue = normalizedValue
    self.specified = specified
    self.attributeType = attributeType
    
  def printme(self, file, namespaces={}, useSNV=0):
    nsname = self.namespaceName
    if useSNV:
      val = self.schemaNormalizedValue
    else:
      val = self.normalizedValue
    text = escape(val, 1)
    if nsname is None:
      ans=" %s" % self.localName
    else:
      ans=" %s:%s" % (getBinding(namespaces,nsname).prefix, self.localName)
    avs='="%s"' % text
    oe=self.ownerElement
    if oe.indented is not None:
      tl=len(avs)+len(ans)
#      print (tl,len(oe.indented),oe.attrStart)
      if oe.attrStart+tl>80:
        il=len(oe.indented)
        if il+tl>80:
          # really long
          oe.attrStart=il-len(oe.localName)
          file.write("\n")
          file.write(" "*oe.attrStart)
        else:
          oe.attrStart=len(oe.indented)
          file.write("\n")
          file.write(oe.indented)
      oe.attrStart=oe.attrStart+tl
    file.write(ans)
    file.write(avs)

class Namespace(InformationItem):

  def __init__(self, prefix, namespaceName):
    self.prefix = prefix
    self.namespaceName = namespaceName;

  def printme(self, file, oe, printXMLNS=0):
    if ((not printXMLNS) and self.prefix=="xml"):
      return
    text = escape(self.namespaceName, 1)
    if self.prefix == None:
      nns=' xmlns="%s"' % text
    else:
      nns=' xmlns:%s="%s"' % (self.prefix, text)
    if oe.indented is not None:
      tl=len(nns)
      if oe.attrStart+tl>80:
        oe.attrStart=len(oe.indented)
        file.write("\n")
        file.write(oe.indented)
      oe.attrStart=oe.attrStart+tl
    file.write(nns)

#  class EntityDeclaration(InformationItem):

#    def __init__(self, entityType, name, systemIdentifier, publicIdentifier, baseURI, notation, content, charset):
#      self.entityType = entityType
#      self.name = name
#      self.systemIdentifier = systemIdentifier
#      self.publicIdentifier = publicIdentifier
#      self.baseURI = baseURI
#      self.notation = notation
#      self.content = content
#      self.charset = charset

#    def reflect(self, parent=None):
#      pass                                # not yet
  
# reverse namespace lookup
def getBinding(nsTable,name,allowDNS=0):
  for namespace in nsTable.values():
    if namespace.namespaceName == name:
      if allowDNS or namespace.prefix is not None:
        return namespace

def escape(text, isattr=0):
  if text is None:
    return 'NNNNNNNNN'
  if "&" in text:
    text=text.replace("&","&amp;")
  if "<" in text:
    text=text.replace("<","&lt;")
  if isattr and '"' in text:
    text=text.replace('"',"&quot;")
  if uPat.search(text):
    text=uPat.sub(entRef,text)
  return text

uPat=re.compile(u"[\x01-\x08\x0b\x0c\x0e-\x1f\x80-\uffff]",re.UNICODE)

def entRef(match):
  return "&#%d;"%ord(match.group(0))

def orderAttrs(n1,n2,firstAttrs,lastAttrs):
  if n1 in firstAttrs:
    if n2 in firstAttrs:
      return cmp(firstAttrs.index(n1),firstAttrs.index(n2))
    else:
      return -1
  elif n2 in firstAttrs:
    return 1
  if n1 in lastAttrs:
    if n2 in lastAttrs:
      return cmp(lastAttrs.index(n1),lastAttrs.index(n2))
    else:
      return 1
  elif n2 in lastAttrs:
    return -1
  return cmp(n1,n2)

import sys

if 0:
  d = Document("http://base")
  e = Element(d, "http://some/namespace", "foo", None, d.baseURI)
  d.addChild(e)
  a = Attribute(e, "http://some/namespace", "attr", None, "value")
  e.addAttribute(a)
  e2 = Element(d, "http://some/namespace", "bar", None, d.baseURI)
  e.addChild(e2)
  c = Characters(e, "\nhello world\n")
  e.addChild(c)
  d.printme(sys.stderr)

# $Log: XMLInfoset.py,v $
# Revision 1.11  2006-08-15 16:17:02  ht
# fall back to pull-SAX if PyLTXML not available
#
# Revision 1.10  2004/08/31 15:11:18  ht
# add serialisation support,
# including use of SNV
#
# Revision 1.9  2004/06/30 11:09:43  ht
# be a bit more careful serializing: always use numcharrefs
# for non ASCII chars
#
# Revision 1.8  2003/02/26 11:56:51  ht
# allow attribute order to be controlled when dumping
# fix xmlns indentation
#
# Revision 1.7  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.6  2002/10/23 08:48:13  ht
# improve indenting of from-indented-file material,
# wrap attrs if indenting
#
# Revision 1.5  2002/10/08 20:50:07  ht
# minor pychecker-discoverd fixes
#
# Revision 1.4  2002/10/02 13:49:34  ht
# normally dont print xmlns:xml binding
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
