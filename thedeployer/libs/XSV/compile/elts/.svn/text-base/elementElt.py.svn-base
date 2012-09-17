"""Schema compilation first phase for element elements"""

__version__="$Revision: 1.1 $"
# $Id: elementElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from defRefElt import defRefElt
from particleElt import particleElt
from groupElt import groupElt
from commonElt import commonElt

from XSV.compile.Particle import Particle
from XSV.compile.Element import Element
from XSV.compile.QName import QName

from XSV.compile.SchemaError import shouldnt

class elementElt(defRefElt,particleElt):
  type=None
  complexType=None
  simpleType=None
  form=None
  default=None
  fixed=None
  substitutionGroup=None
  nullable=None
  parent=None
  abstract=None
  final=None
  block=None
  def __init__(self,sschema,elt):
    defRefElt.__init__(self,sschema,elt)
    self.keys=[]
    self.keyrefs=[]
    self.uniques=[]

  def init(self,elt):
    # does some simple checks and calls back on of three following methods
    defRefElt.init(self,'element',groupElt)
    particleElt.init(self)

  def checkRefed(self):
    # called if nested 'ref' form
    for ba in ('type','block','default','nullable','fixed','complexType','simpleType','key','keyref','unique'):
      if self.__dict__.has_key(ba) and getattr(self,ba):
        self.error("element with ref can't have %s"%ba)
        setattr(self,ba,None)
    if self.maxOccurs=="0":
      self.component=None
    else:
      self.component=Particle(self.schema.sschema,self,None)
      self.component.termName=QName(self.ref,self.elt,
                                              self.schema.sschema)
      self.component.termType='element'

  def checkInternal(self):
    # local def
    if self.form is None:
      self.form=self.schema.elementFormDefault
    self.final=''
    self.block=''
    nElt=Element(self.schema.sschema,self,self.parent)
    if self.maxOccurs=="0":
      self.component=None
    else:
      self.component=Particle(self.schema.sschema,self,nElt)

  def checkTop(self):
    # top-level def
    if self.final==None:
      self.final=self.schema.finalDefault
    if self.final=='#all':
      self.final='restriction extension'
    if self.block==None:
      self.block=self.schema.blockDefault
    if self.block=='#all':
      self.block='restriction extension substitution'
    self.component=Element(self.schema.sschema,self,'global')

  def merge(self,other):
    # called in content model restricting
    shouldnt('merge3')
    myName=self.name or self.ref
    if other.__class__==Element:
      otherName=other.name or other.ref
      if myName==otherName:
	# should do subsumption check, construct merged type, of course
	return self
      else:
	self.error("can't restrict %s with %s"%(otherName,myName))

  def newComponent(self,schema):
    commonElt.newComponent(self,'element',schema.elementTable)

# $Log: elementElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
