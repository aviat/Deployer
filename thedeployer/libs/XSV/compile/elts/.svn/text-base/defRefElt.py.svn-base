"""Schema compilation first phase for defRef elements"""

__version__="$Revision: 1.1 $"
# $Id: defRefElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt
from complexTypeElt import complexTypeElt

class defRefElt(commonElt):
  # shared by groupElt,attributeElt and elementElt
  name=None
  ref=None
  parent=None
  def init(self,eltName,nestingElt,badAttrs=('minOccurs','maxOccurs','ref')):
    if not (self.name or self.ref):
      self.error("%s with no name or ref"%eltName) # die?
    parent=self.schema.sschema.eltStack[0]
    if isinstance(parent,complexTypeElt) or isinstance(parent,nestingElt):
      self.parent=parent
      if self.ref is not None:
        # TODO: check ref syntax
        self.checkRefed()
      else:
        # TODO: check name syntax
        self.checkInternal()
    else:
      for an in badAttrs:
        if getattr(self,an)!=None:
          self.error("top-level %s may not have %s"%(eltName,an))
          setattr(self,an,None)
      # top-level def
      # TODO: check name syntax more thoroughly
      if (self.name and (':' in self.name)):
        self.error("'name' must be an NCName") # die?
      self.checkTop()


# $Log: defRefElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
