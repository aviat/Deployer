"""Schema compilation first phase for rul elements"""

__version__="$Revision: 1.2 $"
# $Id: rulElt.py,v 1.2 2002-11-25 10:39:01 ht Exp $

from commonElt import commonElt

from XSV.compile.Restriction import Restriction
from XSV.compile.List import List
from XSV.compile.Union import Union

class rulElt(commonElt):
  facets=[]
  def init(self,elt):
    self.component=self.comp(self.schema.sschema,self)

class restrictionElt(rulElt):
  # TODO: check base vs content???
  group=None
  all=None
  choice=None
  sequence=None
  simpleType=None
  attrs=[]
  comp=Restriction
  def init(self,elt):
    if (elt is not None and
        'complexContent'==(elt.parent.llabel or elt.parent.label)):
      # don't init yet, complexContent itself will handle this
      pass
    else:
      rulElt.init(self,elt)
      if self.simpleType is not None:
        self.component.basetype=self.simpleType.component
      tab={}
      if self.facets:
        for facet in self.facets:
          facet.register(tab)
      self.facets=tab

class listElt(rulElt):
  # TODO: check base vs content
  simpleType=None
  itemType=None
  comp=List

class unionElt(rulElt):
  # TODO: check base vs content
  subTypes=[]
  memberTypes=None
  comp=Union

class extensionElt(commonElt):
  group=None
  all=None
  choice=None
  sequence=None
  facets=[]
  attrs=[]
  init=None

# $Log: rulElt.py,v $
# Revision 1.2  2002-11-25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
