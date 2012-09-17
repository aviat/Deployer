"""Relation normal form: Example of use"""

__version__="$Revision: 1.2 $"
# $Id: layerExample.py,v 1.2 2002-09-23 21:45:03 ht Exp $

import layer

# minimal illustration of layer functionality
# assumes <sample><bit name='a'/><bit name='..'/>...</sample>

def doit(filename=None):
  f=layer.factory()
  top=f.fromFile({"bit":("group","bitList")},
                 {},
                 lookup,"instance","variable",None,filename)
  return top

def lookup(eltName):
  return eval(eltName)

class sample:
  def __init__(self,factory,elt):
    self.elt=elt
    self.factory=factory

  def init(self,elt):
    print ' '.join(map(lambda b:b.name,self.bitList))

class bit:
  def __init__(self,factory,elt):
    self.elt=elt
    self.factory=factory

# $Log: layerExample.py,v $
# Revision 1.2  2002-09-23 21:45:03  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:46:17  ht
# part of package now
#
