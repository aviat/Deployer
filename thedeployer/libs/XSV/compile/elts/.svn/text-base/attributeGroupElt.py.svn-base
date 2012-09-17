"""Schema compilation first phase for attributeGroup elements"""

__version__="$Revision: 1.1 $"
# $Id: attributeGroupElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from XSV.compile.AttributeUse import AttributeUse
from XSV.compile.QName import QName
from XSV.compile.AttributeGroup import AttributeGroup

from defRefElt import defRefElt
from commonElt import commonElt

class attributeGroupElt(defRefElt):
  def __init__(self,sschema,elt):
    defRefElt.__init__(self,sschema,elt)
    sschema.eltStack[0:0]=[self]
    self.attrs=[]

  def init(self,elt):
    self.schema.sschema.eltStack=self.schema.sschema.eltStack[1:]
    defRefElt.init(self,'attributeGroup',attributeGroupElt,('ref',))

  def checkRefed(self):
    if self.attrs:
      self.error("can't have ref %s and attrs in attributeGroup"%self.ref)
    if self.name:
      self.error("internal attributeGroup with name %s"%self.name)
      self.name=''
    self.component=AttributeUse(self.schema.sschema,self,None)
    self.component.attributeDeclarationName=QName(self.ref,self.elt,
                                                            self.schema.sschema)
    self.component.nameType='attributeGroup'

  def checkInternal(self):
    self.error("internal attributeGroup must have ref")

  def checkTop(self):
    # only called if we are a top-level attributeGroup
    self.component=AttributeGroup(self.schema.sschema,self)

  def newComponent(self,schema):
    commonElt.newComponent(self,'attributeGroup',schema.attributeGroupTable)

# $Log: attributeGroupElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
