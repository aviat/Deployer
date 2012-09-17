"""Schema compilation: Particle component"""

__version__="$Revision: 1.8 $"
# $Id: Particle.py,v 1.8 2006-08-15 16:11:22 ht Exp $

from Component import Component
from QName import QName
from Element import Element
from Group import Choice
from FSM import UniqueFSM

from XSV import xsvNS

from SchemaError import shouldnt

UndefQName=None

class Particle(Component):
  termName=None
  def __init__(self,sschema,xrpr=None,term=None,surrogate=None):
    Component.__init__(self,sschema,xrpr,None)
    if xrpr is not None:
      self.occurs=_computeMinMax(xrpr.minOccurs or "1",xrpr.maxOccurs,self)
    elif surrogate is not None:
      # for errors only
      self.xrpr=surrogate
    if term is not None:
      self.term=term

  def __getattr__(self,name):
    if name=='term':
      self.term=None
      if self.termName:
        if self.termType=='element':
          if self.schema.vElementTable.has_key(self.termName):
            self.term=self.schema.vElementTable[self.termName]
          else:
            self.error("Undefined element %s referenced from content model"%self.termName)
        elif self.termType=='group':
          if self.schema.vGroupTable.has_key(self.termName):
            self.term=self.schema.vGroupTable[self.termName]
            if self.term.base is not None:
              # term is an as-yet-unchecked restrictive redefinition
              # build and check the fsms -- not reused yet, sigh
              (baseFSM,nd)=UniqueFSM(self.term.base)
              if not nd:
                # if nd, then it breaks UPA and we can't check subsumption
                # the UPA violation will get caught elsewhere
                (termFSM,nd)=UniqueFSM(self.term)
                if not nd:
                  # as above
                  res=termFSM.subsumed(baseFSM)
                  if res is not None:
                    termFSM.subsumptionError(self,baseFSM,res,"group",
                                             self.termName,
                                             "[original %s]"%self.termName,xsvNS)
                    self.term.error("redefined group not a restriction of its original definition")
          else:
            self.error("Undefined group %s referenced from content model"%self.termName)
        else:
          shouldnt('tnt')
      else:
        shouldnt('tn')
      return self.term
    elif name=='minOccurs':
      return str(self.occurs[0])
    elif name=='maxOccurs':
      return str(self.occurs[1] or 'unbounded')
    else:
      raise AttributeError,name

  def merge(self,other):
    return self
    # short circuited for now
    if self.occurs==(0,0):
      return None
    if (self.__dict__.has_key('termName') and self.termName and
        other.__dict__.has_key('termName') and self.termName==other.termName):
      return self
    if self.term.__class__ is other.term.__class__:
      if (self.occurs[0]>=other.occurs[0] and
          ((not other.occurs[1]) or
           (self.occurs[1] and
            self.occurs[1]<=other.occurs[1]))):
        self.term=self.term.merge(other.term)
      else:
        self.schema.error('restriction range %s not a sub-range of base %s'%
                          (self.occurs,other.occurs),self.xrpr.elt)
      return self
    if other.term.__class__ is Choice and self.term.__class__ is Element:
      # special case this because it occurs in SforS
      for om in other.term.particles:
        if (om.term.__class__ is Element and
            om.term.name==self.term.name and
            om.term.targetNamespace==self.term.targetNamespace):
          return self.merge(om)
    self.xrpr.error('non-like-for-like restriction not checked yet: %s vs. %s'%(self.term.__class__,other.term.__class__),1)
    return self

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    return (self.term is not None) and self.term.prepare()

  def exponent(self):
    if self.occurs[0]==0:
      if self.occurs[1]==1:
        return '?'
      else:
        return '*'
    if (self.occurs[0]==1 and
	(self.occurs[1]==1)):
      return ''
    else:
      return '+'

  def occursReflect(self,parent):
    # ignore, see below
    pass

  def minOccursRebuild(self,val):
    # hack to get in and rebuild occurs
    self.occurs=_computeMinMax(self.minOccurs,self.maxOccurs,self)

def _computeMinMax(minStr,maxStr,comp):
  try:
    min = long(minStr)
  except ValueError:
    min=1
    comp.error("%s not a valid minOccurs value"%minStr)
  if maxStr == "unbounded":
    max = None
  elif maxStr:
    try:
      max = long(maxStr)
    except ValueError:
      max=1
      comp.error("%s not a valid maxOccurs value"%maxStr)
  else:
    max = 1
  return (min,max)


def init():
  global UndefQName
  UndefQName=QName(None,'#undef#',None)


# $Log: Particle.py,v $
# Revision 1.8  2006-08-15 16:11:22  ht
# use xsvNS for dumping FSMs
#
# Revision 1.7  2004/05/12 15:13:57  ht
# remove bogus leftover
#
# Revision 1.6  2003/12/04 10:53:01  ht
# use shared subsumption error messaging
#
# Revision 1.5  2003/11/27 12:20:08  ht
# Check restriction OK on group redefinition
#
# Revision 1.4  2002/11/05 14:20:39  ht
# check restriction in case of group redef
#
# Revision 1.3  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:09:25  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
