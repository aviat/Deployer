"""Build class instances from an alternating normal form XML document"""

__version__="$Revision: 1.4 $"
# $Id: rebuild.py,v 1.4 2005-04-22 13:54:20 ht Exp $

# Note that we get lists in TWO cases:
# 1) multiple rel elements with same name
# 2) multiple daughters of single rel element

import PyLTXML
import types

NilVal=(None,)

def fromAltFile(filename,relMap,constructInd,root=None):
  flags=(PyLTXML.NSL_read|PyLTXML.NSL_read_namespaces)
  try:
    if type(filename)==types.UnicodeType:
      filename=filename.encode('utf_8')
    file=PyLTXML.Open(filename,None,flags)
  except:
    return
#  try:
  if root:
    buildRels(file,root,relMap,constructInd)
  else:
    root=buildInd(file,relMap,constructInd)
 # except:
   # root=None
#  try:
  if root and file.seenValidityError:
    root=None
 # except:
  #  pass
#  try:
  PyLTXML.Close(file)
 # except:
  #  pass
  return root

def buildRels(file,ind,relMap,constructInd):
  b = PyLTXML.GetNextBit(file)
  down=0
  while b:
    if b.type == "start" or b.type == "empty":
      if down:
        # multiple values
        rval=buildInd(file,relMap,constructInd,b)
      else:
#        print ('br',b.llabel)
        lab=b.llabel
        if relMap.has_key(lab):
          lab=relMap[lab]
        if b.type=="start":
          rval=buildInd(file,relMap,constructInd)
        elif PyLTXML.GetAttrVal(b.item,'xsi:nil')=='true':
          rval=NilVal
        else:
          rval=""
        # three cases -- a) this rel was empty; b) this rel had text content;
        #                c) this rel had an ind elt content
        # In case (a) and (b) the end tag is not there/consumed, case (c) it's
        # still to come
        if b.type=="start" and (type(rval)==types.InstanceType or not rval):
          down=1
#      print ('bir',rval,lab,ind.__dict__.has_key(lab))
      if ind.__dict__.has_key(lab) and (getattr(ind,lab) is not None):
        # Can't use hasattr because that finds the class defaults
        # But what about non-null defaults at the __init__ level?
        ov=getattr(ind,lab)
        if type(ov)==types.ListType:
          ov.append(rval)
        else:
          setattr(ind,lab,[ov,rval])
      else:
        setattr(ind,lab,rval)
    elif b.type == "end":
      # if we have one or more inds as value, this is just this rel's end 
      if down:
        down=0
      else:
        # we're done
        return
    elif  b.type == "bad":
      raise Exception, "parse error"
    # note we ignore pis, comments, text -- text is whitespace or broken
    b = PyLTXML.GetNextBit(file)
  # better be the top rel finishing . . .

def buildInd(file,relMap,constructInd,b=None):
  if not b:
    b = PyLTXML.GetNextBit(file)
  text=""
  while b:
    if b.type == "start" or b.type == "empty":
#      print ('bi',b.llabel)
      inst=constructInd(b.llabel,b.item)
      # is this too XMLSchema-specific?  Note we can't handle this in
      # Component.rebuild itself, as there are circular references
      if inst is not None and inst.reffed:
        inst.reffed=0
        rebuild=0
      else:
        rebuild=1
      if b.type=="start":
        if inst is not None:
          buildRels(file,inst,relMap,constructInd)
          # buildRels consumes our end tag
        else:
          # skip this, assume non-recursive
          lab=b.label
          b=PyLTXML.GetNextBit(file)
          while b is not None and (b.type!="end" or b.label!=lab):
            b=PyLTXML.GetNextBit(file)
      if rebuild and (inst is not None) and inst.rebuild:
        inst.rebuild()
      return inst
    elif b.type=="text":
      text=b.body
    elif b.type=="end":
      # we were text only, return it
#      print ('bt',text)
      return text
    elif  b.type == "bad":
      raise Exception, "parse error"
    b = PyLTXML.GetNextBit(file)
  # shouldn't be possible to fall out without errror
  raise Exception, "oops, ran off end of XML file"

def av(item,name):
  return PyLTXML.GetAttrVal(item,name)

# $Log: rebuild.py,v $
# Revision 1.4  2005-04-22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.3  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.2  2002/11/04 13:36:01  ht
# protect against unicode filenames
#
# Revision 1.1  2002/06/28 09:46:26  ht
# part of package now
#
