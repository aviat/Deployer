"""Schema compilation: AttributeUse component"""

__version__="$Revision: 1.3 $"
# $Id: AttributeUse.py,v 1.3 2002-11-25 14:53:08 ht Exp $

from Component import Component
from QName import QName

from SchemaError import shouldnt

_attrOccurs={'prohibited':(0,0),
            'optional':(0,1),
            'default':(0,1),
            'fixed':(0,1),
            'required':(1,1)}


class AttributeUse(Component):
  nameType=None
  attributeDeclarationName=None
  valueConstraint=None
  minOccurs=1
  maxOccurs=1
  def __init__(self,sschema,xrpr,attributeDeclaration=None,use=None,vct=None,
               value=None):
    Component.__init__(self,sschema,xrpr,None)
    if use is not None:
      (self.minOccurs,self.maxOccurs)=_attrOccurs[use]
    if vct is not None:
      self.valueConstraint=(vct,value)
    if attributeDeclaration is not None:
      self.attributeDeclaration=attributeDeclaration

  def __getattr__(self,name):
    if name=='attributeDeclaration':
      if self.attributeDeclarationName and self.nameType=='attribute':
        if self.schema.vAttributeTable.has_key(self.attributeDeclarationName):
          self.attributeDeclaration=self.schema.vAttributeTable[self.attributeDeclarationName]
        else:
          self.error("Undeclared attribute %s referenced"%(self.attributeDeclarationName))
          self.attributeDeclaration=None
        return self.attributeDeclaration
      else:
        shouldnt('attrUse1')
    elif name=='attributeGroup':
      if self.attributeDeclarationName and self.nameType=='attributeGroup':
        if self.schema.vAttributeGroupTable.has_key(self.attributeDeclarationName):
          self.attributeGroup=self.schema.vAttributeGroupTable[self.attributeDeclarationName]
        else:
          self.error("Undeclared attribute group %s referenced"%(self.attributeDeclarationName))
          self.attributeGroup=None
        return self.attributeGroup
      else:
        shouldnt('attrUse2')
    elif name=='vcv':
      if self.valueConstraint is not None:
        return self.doVcv(self.attributeDeclaration.typeDefinition)
      else:
        self.vcv=self.attributeDeclaration.vcv
        return self.vcv
    elif name=='qname':
      # allow type derivation without chasing refs
      if self.attributeDeclarationName:
        self.qname=self.attributeDeclarationName
      else:
        self.qname=QName(None,self.attributeDeclaration.name,
                         self.attributeDeclaration.targetNamespace)
      return self.qname
    else:
      raise AttributeError,name

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=(self.valueConstraint is not None) and (self.vcv is not None)
    p2=self.attributeDeclaration.prepare()
    return p1 and p2

  def expand(self,table):
    # ref might be broken, so check before forwarding
    if self.nameType=='attributeGroup':
      if self.attributeGroup is not None:
        self.attributeGroup.expand(table)
    elif self.attributeDeclaration is not None:
      # might lose, so check first
      self.attributeDeclaration.expand(table,self)


# $Log: AttributeUse.py,v $
# Revision 1.3  2002-11-25 14:53:08  ht
# involve vcv in preparation
#
# Revision 1.2  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
