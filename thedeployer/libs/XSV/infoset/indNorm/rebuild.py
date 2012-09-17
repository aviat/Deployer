"""Build class instances from an individual normal form XML document"""

__version__="$Revision: 1.7 $"
# $Id: rebuild.py,v 1.7 2007-02-16 14:13:32 ht Exp $

import XSV

usePyLTXML = XSV.useLTXML()

if usePyLTXML:
  from PyLTXML import Open, Close, NSL_read, NSL_read_namespaces
  from PyLTXML import GetNextBit, GetAttrVal
  # use map source='PyLTXML'
  NSL_bad="bad"
  NSL_start_bit="start"
  NSL_empty_bit="empty"
  NSL_end_bit="end"
else:
  from XSV.infoset.SAXLTXML import Open, Close, NSL_read, NSL_read_namespaces
  from XSV.infoset.SAXLTXML import GetNextBit, GetAttrVal
  from XSV.infoset.SAXLTXML import NSL_bad, NSL_start_bit, NSL_empty_bit
  from XSV.infoset.SAXLTXML import NSL_end_bit


import types

NilVal=(None,)

def fromIndFile(filename,constructInd):
  flags=(NSL_read|NSL_read_namespaces)
  try:
    if type(filename)==types.UnicodeType:
      filename=filename.encode('utf_8')
    #print ('fIF',filename)
    file=Open(filename,flags)
  except:
   return
  root=buildInd(file,constructInd)      # e.g. SSchema.psviConstruct
  if root and file.seenValidityError:
    root=None
  Close(file)
  return root

eaTab={}

def eltAttrs(lab,file):
  # we don't actually use this for the time being
  try:
    attrs=eaTab[lab]
  except:
    ets=file.elementTypes[lab]
    if ets is None:
      eaTab[lab]=None
      return
    attrs=ets.attrDefns.keys()
    eaTab[lab]=attrs
  return attrs

def buildInd(file,constructInd,b=None):
  if not b:
    b = GetNextBit(file)
  while b:
    if b.type == NSL_start_bit or b.type == NSL_empty_bit:
      inst=constructInd(b.llabel,b.item)
      # is this too XMLSchema-specific?  Note we can't handle this in
      # Component.rebuild itself, as there are circular references
      #print ('ni',inst,inst.reffed,b.type)
      if inst is not None and inst.reffed:
        inst.reffed=0
        rebuild=0
      else:
        rebuild=1
      if GetAttrVal(b.item,'i:nil')=='true': #  b.type==NSL_empty_bit and [only works with PyLTxML]
        if b.type!=NSL_empty_bit:
          b = GetNextBit(file)
        pass
      elif inst is not None:
        buildRels(file,inst,constructInd,b.item,b.type==NSL_empty_bit)
        # buildRels consumes our end tag if non-empty
      else:
        if b.type==NSL_start_bit:
          # skip this, assume non-recursive
          lab=b.label
          b=GetNextBit(file)
          while b is not None and (b.type!=NSL_end_bit or b.label!=lab):
            b=GetNextBit(file)
      if rebuild and (inst is not None) and inst.rebuild:
        inst.rebuild()
      return inst
    elif  b.type == NSL_bad:
      raise Exception, "parse error"
    elif b.type==NSL_end_bit:
      shouldnt('bend')
    b = GetNextBit(file)
  # shouldn't be possible to fall out without errror
  raise Exception, "oops, ran off end of XML file"

def buildRels(file,ind,constructInd,item,noContent=0):
  b=None
  readEnd=noContent
  # skip=1 means we've found a daughter ahead of time, spin through reflMap
  #  until we hit it
  # skip=2 means we've hit our parent's end, spin through reflMap until the end
  if noContent:
    skip=2
  else:
    skip=0
  # print ('br',ind,item.llabel,ind.reflectionInMap)
  for (xName,tt,opt,pAttr) in ind.reflectionInMap:
    if tt in ('string','boolean','list','aspecial'):
#      print ('which',pAttr,(tt=='aspecial' and xName) or pAttr)
      setattr(ind,(tt=='aspecial' and xName) or pAttr,
              GetAttrVal(item,xName))
      if skip:
        continue
    else:
      if tt=='components' or tt=='esspecial':
        lv=[]
      else:
        lv=None
      if tt=='esspecial' or tt=='especial':
        rAttr=xName[0]
      else:
        rAttr=pAttr
      if not skip:
        b = GetNextBit(file)
        if b is None:
          shouldnt('nobit')
      while b:
        if skip==2 or (skip==0 and b.type == NSL_end_bit):
          readEnd=1
          # this is just this overhead ind's end
          if lv is None and not opt:
            shouldnt ('fell off: %s, %s, %s'%(b.llabel,xName,pAttr))
          else:
            setattr(ind,rAttr,lv)
            skip=2
            break
        elif skip==1 or b.type == NSL_start_bit or b.type == NSL_empty_bit:
          if not skip:
            rval=buildInd(file,constructInd,b)
          if b.llabel not in xName:
            if lv is None and not opt:
              shouldnt('missing: %s, %s, %s'%(b.llabel,xName,pAttr))
            setattr(ind,rAttr,lv)
            skip=1
            break
          elif lv is not None:
            lv.append(rval)
            skip=0
          else:
            setattr(ind,rAttr,rval)
            skip=0
            break
        elif  b.type == NSL_bad:
          raise Exception, "parse error"
        # note we ignore pis, comments, text -- text is whitespace or broken
        b=GetNextBit(file)
      if not skip:
        b=GetNextBit(file)
  if not readEnd:
    # do we ever need to look at the existing b here?
    b=GetNextBit(file)
    while b:
      if b.type==NSL_end_bit:
        if b.llabel!=item.llabel:
          shouldnt('unsync: %s,%s'%(item.llabel,b.llabel))
        return
      elif b.type==NSL_start_bit or b.type==NSL_empty_bit:
        shouldnt('unsync2: %s,%s'%(item.llabel,b.llabel))
      elif b.type==NSL_bad:
        raise Exception, "parse error"
      b=GetNextBit(file)
    shouldnt('eof???')

def av(item,name):
  return GetAttrVal(item,name)

def shouldnt(msg):
  error("Shouldn't happen "+msg)

def error(msg):
  raise UnmarshallError,msg

class UnmarshallError(Exception):
  pass

# $Log: rebuild.py,v $
# Revision 1.7  2007-02-16 14:13:32  ht
# debugging
#
# Revision 1.6  2006/08/15 16:17:02  ht
# fall back to pull-SAX if PyLTXML not available
#
# Revision 1.5  2005/08/10 20:31:22  ht
# comment
#
# Revision 1.4  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.3  2002/11/04 13:36:01  ht
# protect against unicode filenames
#
# Revision 1.2  2002/10/08 20:31:23  ht
# remove unused import
#
# Revision 1.1  2002/06/28 09:46:07  ht
# part of package now
#
