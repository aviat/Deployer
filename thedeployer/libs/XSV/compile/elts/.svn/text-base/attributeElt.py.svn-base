"""Schema compilation first phase for attribute elements"""

__version__="$Revision: 1.1 $"
# $Id: attributeElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from XSV.compile.QName import QName
from XSV.compile.Attribute import Attribute
from XSV.compile.AttributeUse import AttributeUse

from defRefElt import defRefElt
from attributeGroupElt import attributeGroupElt
from commonElt import commonElt

class attributeElt(defRefElt):
  type=None
  simpleType=None
  form=None
  use=None
  default=None
  fixed=None

  def init(self,elt):
    defRefElt.init(self,'attribute',attributeGroupElt,('ref',))

  def checkRefed(self):
    if self.type is not None:
      self.error("attribute with ref %s can't have type %s"%(self.ref,self.type))
      self.type=None
    elif self.simpleType is not None:
      self.error("attribute with ref %s can't have simpleType"%self.ref)
      self.simpleType=None
    if self.default!=None:
      vct='default'
      value=self.default
    elif self.fixed!=None:
      vct='fixed'
      value=self.fixed
    else:
      vct=value=None
    self.component=AttributeUse(self.schema.sschema,self,None,
                                          self.use or 'optional',vct,value)
    self.component.attributeDeclarationName=QName(self.ref,self.elt,
                                                            self.schema.sschema)
    self.component.nameType='attribute'

  def checkInternal(self):
    # local def
    if self.default!=None:
      vct='default'
      value=self.default
    elif self.fixed!=None:
      vct='fixed'
      value=self.fixed
    else:
      vct=value=None
    if self.form is None:
      self.form=self.schema.attributeFormDefault
    nAttr=Attribute(self.schema.sschema,self,self.parent)
    self.component=AttributeUse(self.schema.sschema,self,nAttr,
                                          self.use or 'optional',vct,value)

  def checkTop(self):
    # top-level def
    self.component=Attribute(self.schema.sschema,self,'global')

  def newComponent(self,schema):
    commonElt.newComponent(self,'attribute',schema.attributeTable)

# $Log: attributeElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
