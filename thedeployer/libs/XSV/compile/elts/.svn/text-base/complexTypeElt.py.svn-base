"""Schema compilation first phase for complexType elements"""

__version__="$Revision: 1.7 $"
# $Id: complexTypeElt.py,v 1.7 2006-04-21 11:03:23 ht Exp $

from typeElt import typeElt

from XSV.compile.SchemaError import shouldnt
from XSV.compile.QName import QName
from XSV.compile.Type import Type
from XSV.compile.ComplexType import ComplexType

class complexTypeElt(typeElt):
  sub=None
  derivedBy=None
  final=""
  block=""
  abstract="false"
  complexContent=None
  simpleContent=None
  mixed=None
  def __init__(self,sschema,elt):
    typeElt.__init__(self,sschema,elt)
    sschema.eltStack[0:0]=[self]

  def __getattr__(self,name):
    if self.sub is not None:
      if name in ('facets','sequence','choice','all','group','attrs','model'):
        return getattr(self.sub,name)
    else:
      if name in ('facets','attrs','model'):
        return []
    raise AttributeError,name

  def init(self,elt):
    basetypeName=None
    if self.complexContent is not None:
      self.sub=self.complexContent
      if self.complexContent.restriction is not None:
        self.derivedBy='restriction'
        if self.complexContent.restriction.__dict__.has_key('base'):
          # must be a complex type
          basetypeName=QName(self.complexContent.restriction.base,
                             self.complexContent.restriction.elt,
                             self.schema.sschema)
      elif self.complexContent.extension is not None:
        self.derivedBy='extension'
        if self.complexContent.extension.__dict__.has_key('base'):
          # must be a simple type
          basetypeName=QName(self.complexContent.extension.base,
                             self.complexContent.extension.elt,
                             self.schema.sschema)
    elif self.simpleContent is not None:
      self.sub=self.simpleContent
      if self.simpleContent.restriction is not None:
        self.derivedBy='restriction'
        if self.simpleContent.restriction.__dict__.has_key('base'):
          basetypeName=QName(self.simpleContent.restriction.base,
                             self.simpleContent.restriction.elt,
                             self.schema.sschema)
      elif self.simpleContent.extension is not None:
        self.derivedBy='extension'
        if self.simpleContent.extension.__dict__.has_key('base'):
          basetypeName=QName(self.simpleContent.extension.base,
                             self.simpleContent.extension.elt,
                                       self.schema.sschema)
      else:
        shouldnt('stcm')
    else:
      # handle shorthand case with no complex/simpleContent
      self.derivedBy='restriction'
      if self.__dict__.has_key('sequence'):
        self.model=self.sequence
      elif self.__dict__.has_key('choice'):
        self.model=self.choice
      elif self.__dict__.has_key('group'):
        self.model=self.group
      elif self.__dict__.has_key('all'):
        self.model=self.all
      elif self.__dict__.has_key('attrs'):
        self.model=None                 # TODO: check this actually works!
      # attrs case works as is
      else:
        # renaming the urType
        # TODO: check this actually works!
        self.model=None
        self.attrs=[]
    self.schema.sschema.eltStack=self.schema.sschema.eltStack[1:]
    if not self.__dict__.has_key('final'):
      self.final=self.schema.finalDefault
    if not self.__dict__.has_key('block'):
      self.block=self.schema.blockDefault
    self.component=ComplexType(self.schema.sschema,self)
    if basetypeName:
      self.component.basetypeName=basetypeName
    else:
      self.component.basetype=Type.urType

# $Log: complexTypeElt.py,v $
# Revision 1.7  2006-04-21 11:03:23  ht
# typo
#
# Revision 1.6  2006/04/21 10:36:18  ht
# improve final and block support
#
# Revision 1.5  2004/09/08 17:10:36  ht
# typo
#
# Revision 1.4  2004/09/08 17:08:18  ht
# use correct nsdict for basetype
#
# Revision 1.3  2002/11/29 21:11:48  ht
# rework contentType computation to make it lazy,
# fixing bogus extentsion of simpleContent case,
# check for mix/nomix extension cases
#
# Revision 1.2  2002/09/02 16:06:47  ht
# error note to myself
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
