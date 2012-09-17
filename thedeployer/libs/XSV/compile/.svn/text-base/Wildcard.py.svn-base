"""Schema compilation: Wildcard component"""

__version__="$Revision: 1.9 $"
# $Id: Wildcard.py,v 1.9 2007-02-16 14:08:07 ht Exp $

from Component import Component
from AttributeUse import AttributeUse

class Wildcard(Component):
  negated=0
  def __init__(self,sschema,xrpr=None,extra=0):
    Component.__init__(self,sschema,xrpr)
    if xrpr is not None:
      self.processContents=xrpr.processContents
    
  def __unicode__(self):
    return "{Wildcard: %s, %s}"%(self.allowed,self.processContents)

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def prepare(self):
    return 1

  def allows(self,namespace):
    if self.negated:
      return namespace not in self.namespaces
    else:
      return namespace in self.namespaces

  def expand(self,tab,use):
    # Called when this wildcard is in a complexType or attributeGroup
    # have to copy when expanded, as could happen several times if
    # we're in a group
    mine=self
    if tab.has_key("#any"):
      mine=self.intersect(tab["#any"].attributeDeclaration)
    newUse=AttributeUse(use.sschema,use.xrpr,mine)
    newUse.minOccurs=use.minOccurs
    newUse.maxOccurs=use.maxOccurs
    tab["#any"] = newUse

  def intersect(self,other):
    if self.negated==other.negated:
      if (self.namespaces==other.namespaces and
          self.processContents==other.processContents):
        # no copy in this case?
        return self
      nw=Wildcard(self.sschema,self.xrpr)
      nw.negated=self.negated
      nw.namespaces=[]
      if nw.negated:
        # neg/neg
        for n in self.namespaces+other.namespaces:
          if n not in nw.namespaces:
            nw.namespaces.append(n)
      else:
        # pos/pos
        for n in self.namespaces:
          if n in other.namespaces:
            nw.namespaces.append(n)
    else:
      nw=Wildcard(self.sschema,self.xrpr)
      nw.negated=0
      if self.negated:
        # neg/pos
        inN=other.namespaces
        outN=self.namespaces
      else:
        # pos/neg
        inN=self.namespaces
        outN=other.namespaces
      if not outN:
        nw.namespaces=inN
      else:
        nw.namespaces=[]
        for n in inN:
          if (n and (n not in outN)):
            nw.namespaces.append(n)
    if nw.negated:
      nw.allowed='not %s'%nw.namespaces
    else:
      nw.allowed='%s'%nw.namespaces
    if self.processContents==other.processContents:
      nw.processContents=self.processContents
    else:
      if self.processContents=='strict' or other.processContents=='strict':
        nw.processContents='strict'
      elif self.processContents=='lax' or other.processContents=='lax':
        nw.processContents='lax'
      else:
        nw.processContents='skip'
    return nw

  def checkSubtype(self,other):
    # TODO: something
    pass

  def subsumed(self,other):
    # check if all of me is in him
    if (not (self.processContents==other.processContents or
             other.processContents=='skip' or
             self.processContents=='strict')):
      return 0
    if self.negated==other.negated:
      if self.negated:
        for ns in other.namespaces:
          if ns not in self.namespaces:
            return 0
      else:
        for ns in self.namespaces:
          if ns not in other.namespaces:
            return 0
      return 1
    elif self.negated:
      # I think this always loses -- we're infinite, other is finite
      return 0
    elif not other.namespaces:
      return 1
    else:
      for n in self.namespaces:
        if n in other.namespaces:
          return 0
    return 1
  
  def isEmpty(self):
    return (not self.negated) and self.namespaces == []
  
  def note(self,table):
    pass

  def namespaceConstraintRebuild(self,val):
    # note we _can't_ reconstruct the right subclass :-(
    if val.variety=='any':
      self.allowed='##any'
      self.namespaces=[]
      self.negated=1
    else:
      self.negated=(val.variety=='negative')
      self.namespaces=map(lambda nn:((nn!='##none' and nn) or None),
                          val.namespaces.split())
      if self.negated:
        self.allowed='##other'
      else:
        self.allowed=self.namespaces

class AnyAny(Wildcard):
  allowed='##any'  # for trace info
  namespaces=[]
  negated=1

class AnyOther(Wildcard):
  allowed='##other'  # for trace info
  negated=1
  def __init__(self,sschema,xrpr):
    Wildcard.__init__(self,sschema,xrpr)
    self.namespaces=[self.targetNamespace,None]

class AnyInList(Wildcard):
  def __init__(self,sschema,xrpr,extra=None):
    Wildcard.__init__(self,sschema,xrpr)
    self.namespaces=map(self.namespaceCode,xrpr.namespace.split())
    self.allowed=self.namespaces

  def namespaceCode(self,arg):
    if arg=='##local':
      return None
    elif arg=='##targetNamespace':
      return self.targetNamespace
    else:
      return arg


# $Log: Wildcard.py,v $
# Revision 1.9  2007-02-16 14:08:07  ht
# more info in printed repr
#
# Revision 1.8  2006/04/04 12:34:34  ht
# check processContents wrt wildcard subsumption
#
# Revision 1.7  2005/04/22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.6  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.5  2003/06/13 09:05:46  ht
# bug in intersection
#
# Revision 1.4  2002/11/11 18:17:46  ht
# __unicode__, handle negation/##other correctly
#
# Revision 1.3  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:13:36  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
