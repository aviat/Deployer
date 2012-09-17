"""Schema compilation: Group component"""

__version__="$Revision: 1.9 $"
# $Id: Group.py,v 1.9 2005-04-22 13:54:20 ht Exp $

from Component import Component
from QName import QName

from SchemaError import shouldnt

groupElt=None                           # imported by init()
explicitGroupElt=None                           # imported by init()

class Group(Component):
  compositor=None
  base=None
  particles=[]
  foundWhere='groupTable'
  def __init__(self,sschema,xrpr=None,surrogate=None):
    Component.__init__(self,sschema,xrpr)
    if xrpr is not None and self.compositor:
      self.particles=map(lambda p:p.component,
                         filter(lambda p:p.component is not None,xrpr.model))
    elif surrogate is not None:
      # really for errors only
      self.xrpr=surrogate

  def __unicode__(self):
    name = self.name or "[anon]"
    model = map(str, self.particles)
    return "{Group %s comp %s:%s}" % (name, self.compositor, ''.join(model))

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def rebuild(self):
    Component.rebuild(self)
    if self.name:
      # really a model group def, merge modelGroup
      self.compositor=self.modelGroup.compositor
      self.particles=self.modelGroup.particles
      self.modelGroup=None
    if self.compositor:
      # cheat like hell
      self.__class__={'sequence':Sequence,
                      'choice':Choice,
                      'all':All}[self.compositor]

  def modelGroupRebuild(self,val):
    self.modelGroup=val

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    r=1
    for p in self.particles:
      r=p.prepare() and r
    return r

  def redefine(self):
    # we have a component which should be based on itself
    # note this forces some reference resolution normally left until later
    if not self.schema.groupTable.has_key(self.name):
      self.error("attempt to redefine in terms of non-existent group: %s"%self.name)
      return
    else:
      redefed=self.schema.groupTable[self.name]
    qn=QName(None,self.name,self.schema.targetNS)
    selfRefs=self.findSelfRefs(qn,list())
    if len(selfRefs)>1:
      self.error("more than one self-reference not allowed in group redefinition")
    else:
      redefed.name="%d %s"%(redefed.id,self.name)
      self.schema.groupTable[redefed.name]=redefed
      self.schema.groupTable[self.name]=self
      self.qname=qn
      if len(selfRefs)==0:
        # must be a restriction -- postpone the real work
        self.base=redefed
      elif len(selfRefs)==1:
        # an extension, just use it
        srp=selfRefs[0].component
        if srp.occurs!=(1,1):
          self.error("self-reference when redefining a group must have maxOccurs=minOccurs=1")
        srp.termName=QName(None,redefed.name,self.schema.targetNS)

  def findSelfRefs(self,qn,res):
    for elt in self.xrpr.model:
      if isinstance(elt,groupElt):
        if elt.component.termName==qn:
          res.append(elt)
      elif isinstance(elt,explicitGroupElt):
        res=elt.component.term.findSelfRefs(qn,res)
    return res

class Sequence(Group):
  compositor='sequence'

class Choice(Group):
  compositor='choice'

class All(Group):
  compositor='all'

class ModelGroup:
  # dummy, just to hold reflection vars
  pass

def init():
  # cut import loops
  global groupElt, explicitGroupElt
  from elts.groupElt import groupElt
  from elts.explicitGroupElt import explicitGroupElt

# $Log: Group.py,v $
# Revision 1.9  2005-04-22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.8  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.7  2005/04/14 13:16:34  ht
# fix redefine infinite loop in obscure case
#
# Revision 1.6  2004/01/28 11:11:58  ht
# fix order bug in prepare
#
# Revision 1.5  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.4  2002/11/05 14:20:16  ht
# implement group redef
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
