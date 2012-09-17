"""Schema compilation first phase for group elements"""

__version__="$Revision: 1.1 $"
# $Id: groupElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from defRefElt import defRefElt
from particleElt import particleElt
from commonElt import commonElt

from XSV.compile.Particle import Particle
from XSV.compile.QName import QName
from XSV.compile.Group import ModelGroup

class groupElt(defRefElt,particleElt):
  # Note this is _not_ parallel to group -- it is not a common superclass of
  # choiceElt, etc.
  # It actually always disappears -- if nested with a ref, into a particle
  # with a termRef; if top-level, into a named sequence, choice or all
  def __init__(self,sschema,elt):
    defRefElt.__init__(self,sschema,elt)
    sschema.eltStack[0:0]=[self]
    self.model=[]

  def init(self,elt):
    self.schema.sschema.eltStack=self.schema.sschema.eltStack[1:]
    defRefElt.init(self,'group',groupElt)
    particleElt.init(self)

  def checkRefed(self):
    if self.model:
      self.error("can't have ref %s and model in group"%self.ref)
    if self.name:
      self.error("internal group with name %s"%self.name)
      self.name=''
    if self.maxOccurs=="0":
      self.component=None
    else:
      self.component=Particle(self.schema.sschema,self,None)
      self.component.termName=QName(self.ref,self.elt,
                                              self.schema.sschema)
      self.component.termType='group'

  def checkInternal(self):
    self.error("internal group must have ref")
    self.component=None

  def checkTop(self):
    # only called if we are a top-level group
    # have to transform into our model
    # our xrpr is lost!
    # note that top-level groups must contain exactly one choice/sequence/all
    if not len(self.model)==1:
      self.error("Top-level model group definitions must contain exactly one choice/sequence/all")
      if len(self.model)==0:
        # arghh
        self.component=None
        return
    mod=self.model[0].component.term
    if mod is not None:
      mod.name=self.name
      # we're a mgd, hack to get two levels of reflection
      mod.reflectedName=ModelGroup.reflectedName
      mod.reflectionOutMap=ModelGroup.reflectionOutMap
    self.component=mod

  def newComponent(self,schema):
    commonElt.newComponent(self,'group',schema.groupTable)

# $Log: groupElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
