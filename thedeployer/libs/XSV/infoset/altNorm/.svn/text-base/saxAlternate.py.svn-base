"""Build class instances from an alternating normal form XML document,
using sax"""

__version__="$Revision: 1.1 $"
# $Id: saxAlternate.py,v 1.1 2002-06-28 09:46:26 ht Exp $

# Note that we get lists in TWO cases:
# 1) multiple rel elements with same name
# 2) multiple daughters of single rel element

from xml import sax
import types

NilVal=(None,)
XSINil=("http://www.w3.org/2001/XMLSchema-instance","nil")

# Create a class to handle content events
class cHandler(sax.ContentHandler):
 
  def __init__(self,relMap,constructInd,root):
    self.relMap=relMap
    self.constructInd=constructInd
    self.current=self.inst=root
    self.buildingI=self.current is None
    self.stack=[]
    self.null=0
    self.skipTo=0
    
  def setDocumentLocator(self,loc):
    self.loc=loc

  def startElementNS(self,name,qname,attrs):
    if self.skipTo is not 0:
      return
    if self.buildingI:
      ind=self.inst=self.buildInd(name,attrs)
      if ind is not None:
        ind.open=1
        if self.current:
          if type(self.current)==types.ListType:
            self.current.append(ind)
          else:
            self.current=[self.current,ind]
        else:
          self.current=ind
    else:
      if attrs.has_key(XSINil) and attrs[XSINil]=='true':
        self.null=1
      else:
        self.stack[0:0]=[(self.current,self.inst)]
        self.current=self.text=None
    self.buildingI=not self.buildingI

  def endElementNS(self,name,qname):
    if self.buildingI:
      # sense is inverted here, we just finished a rel'n
      if self.null:
        self.null=0
        ind=NilVal
      else:
        if self.current is not None:
          ind=self.current
        else:
          ind=self.text                 # may well be None
        (self.current,self.inst)=self.stack[0]
        self.text=None
        self.stack=self.stack[1:]
      self.buildRel(name,ind)
    else:
      if self.skipTo is not 0:
        if self.skipTo==name:
          self.skipTo=0
        else:
          return
      elif (self.current is not None and
            not name[1]=='pointer' and
            self.inst.rebuild):
        self.inst.rebuild()
    self.buildingI=not self.buildingI
  
  def characters(self,content):
    if self.skipTo is not 0:
      return
    if self.buildingI:
      if self.text is None:
        self.text=content
      elif self.current is None:
#        print ('glomming',self.text,content)
        self.text=self.text+content
      else:
        # better be whitespace
        pass
    else:
      # better be whitespace
      pass

  def buildRel(self,name,ind):
    if ind is None:
      ind=""
    lab=str(name[1])
    if self.relMap.has_key(lab):
      lab=self.relMap[lab]
    # three cases -- a) this rel was empty; b) this rel had text content;
    #                c) this rel had an ind elt content
    if (self.inst.__dict__.has_key(lab) and
        (getattr(self.inst,lab) is not None)):
      # Can't use hasattr because that finds the class defaults
      # But what about non-null defaults at the __init__ level?
      ov=getattr(self.inst,lab)
      if type(ov)==types.ListType:
        ov.append(ind)
      else:
        setattr(self.inst,lab,[ov,ind])
    else:
      setattr(self.inst,lab,ind)

  def buildInd(self,name,attrs):
    inst=self.constructInd(name[1],attrs)
    # is this too XMLSchema-specific?  Note we can't handle this in
    # Component.rebuild itself, as there are circular references
    if inst is None:
      # skip all children, assume non-recursive
      self.skipTo=name
    return inst


class eHandler(sax.ErrorHandler):
  def error(self,exception):
    print 'error: %s'%exception

  def fatalError(self,exception):
    print 'fatal error: %s'%exception

  def warning(self,exception):
    print 'warn: %s'%exception

def fromAltFile(filename,relMap,constructInd,root=None):
  # Create a parser
  parser = sax.make_parser()
  # enable namespaces
  parser.setFeature(sax.handler.feature_namespaces,1)
  # Provide the parser with a document handler
  ch=cHandler(relMap,constructInd,root)
  parser.setContentHandler(ch)
  #parser.setErrorHandler(eHandler())

  parser.parse(filename)

  return ch.current

def av(attrs,name,ns=None):
  return attrs.has_key((ns,name)) and attrs[(ns,name)]

# $Log: saxAlternate.py,v $
# Revision 1.1  2002-06-28 09:46:26  ht
# part of package now
#
