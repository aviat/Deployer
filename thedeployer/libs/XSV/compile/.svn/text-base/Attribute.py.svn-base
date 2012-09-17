"""Schema compilation: Attribute component"""

__version__="$Revision: 1.7 $"
# $Id: Attribute.py,v 1.7 2005-04-22 13:54:20 ht Exp $

import types

from Component import Component
from ComplexType import ComplexType
from QName import QName
from Type import Type

from elts.attributeGroupElt import attributeGroupElt

class Attribute(Component):
  attrName=None
  attrDef=None
  typeDefinitionName=None
  valueConstraint=None
  foundWhere='attributeTable'
  def __init__(self,sschema,xrpr,scope=None):
    if (type(scope) is types.StringType or (xrpr and xrpr.form)=='qualified'):
      ns='ns'
    else:
      ns=None
    Component.__init__(self,sschema,xrpr,ns)
    if xrpr is not None:
      if type(scope) is types.StringType:
        self.scope=scope
        if xrpr.default!=None:
          self.valueConstraint=('default',xrpr.default)
        elif xrpr.fixed!=None:
          self.valueConstraint=('fixed',xrpr.fixed)
      else:
        self.scopeRepr=scope
      if xrpr.type is not None:
        self.typeDefinitionName=QName(xrpr.type,xrpr.elt,
                                      sschema)
        if xrpr.simpleType is not None:
          self.error("declaration with 'type' attribute must not have nested type declaration")
      elif xrpr.simpleType is not None:
        self.typeDefinition=xrpr.simpleType.component
      else:
        self.typeDefinition=Type.urSimpleType

  def __unicode__(self):
    if (self.typeDefinition is not None and
        self.typeDefinition.name and
        self.typeDefinition.name[0]!='['):
      return "{Attribute {%s}%s:%s}"%(self.targetNamespace,self.name,self.typeDefinition.name)
    else:
      return "{Attribute {%s}%s:%s}"%(self.targetNamespace,self.name,unicode(self.typeDefinition))

  def __str__(self):
    u=self.__unicode__()
    return u.encode('iso8859_1','replace')

  def __getattr__(self,name):
    if name=='typeDefinition':
      self.typeDefinition=None
      if self.typeDefinitionName:
        if self.schema.vTypeTable.has_key(self.typeDefinitionName):
          self.typeDefinition=self.schema.vTypeTable[self.typeDefinitionName]
          if isinstance(self.typeDefinition,ComplexType):
            self.error("type definition for an attribute ({%s}%s) must not be complex: %s"%(self.targetNamespace,self.name,self.typeDefinitionName))
            self.typeDefinition=None
        else:
          self.error("Undefined type %s referenced as type definition of {%s}%s"%(self.typeDefinitionName, self.targetNamespace, self.name))
      return self.typeDefinition
    elif name=='scope':
      if isinstance(self.scopeRepr,attributeGroupElt):
        self.scope=None
      else:
        self.scope=self.scopeRepr.component
      return self.scope
    elif name=='vcv':
      # value constraint value
      return self.doVcv(self.typeDefinition)
    else:
      raise AttributeError,name

  def prepare(self):
    if self.prepared:
      return 1
    self.prepared=1
    p1=(self.typeDefinition is not None) and self.typeDefinition.prepare()
    p2=(self.scope is not None)
    p3=(self.valueConstraint is not None) and (self.vcv is not None)
    return p1 and p2 and p3

  def expand(self,tab,use):
    qn=use.qname
    if tab.has_key(qn):
      self.error("attempt to redeclare attribute %s, ignored" % qn)
    else:
      tab[qn]=use

  def checkSubtype(self,other):
    mytype=self.typeDefinition
    if (mytype is not None and
        other.typeDefinition is not None and
        not mytype.isSubtype(other.typeDefinition,other.typeDefinition.final)):
      self.error("restricting attribute with type {%s}%s not derived from declared base's attribute's type %s{%s}"%(mytype.targetNamespace,mytype.name,other.typeDefinition.targetNamespace,other.typeDefinition.name))


# $Log: Attribute.py,v $
# Revision 1.7  2005-04-22 13:54:20  ht
# clean up all encoding names
#
# Revision 1.6  2005/04/22 11:03:34  ht
# shift to iso8859_1 from iso8859_1
#
# Revision 1.5  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.4  2002/11/25 14:53:08  ht
# involve vcv in preparation
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
