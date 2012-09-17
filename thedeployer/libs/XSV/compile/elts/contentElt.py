"""Schema compilation first phase for content elements"""

__version__="$Revision: 1.1 $"
# $Id: contentElt.py,v 1.1 2002-06-28 09:43:22 ht Exp $

from commonElt import commonElt

from XSV.compile.SchemaError import shouldnt

class contentElt(commonElt):
  sub=None
  restriction=None
  extension=None
  def init(self,elt):
    if self.restriction is not None:
      self.sub=self.restriction
    elif self.extension is not None:
      self.sub=self.extension
    else:
      shouldnt('cecm')

  def __getattr__(self,name):
    if (self.sub and
        name in ('facets','sequence','choice','all','group','attrs')):
      return getattr(self.sub,name)
    else:
      raise AttributeError,name
  
class complexContentElt(contentElt):
  mixed='unspecified'
  def init(self,elt):
    contentElt.init(self,elt)
    self.model=self.sequence or self.choice or self.group or self.all

class simpleContentElt(contentElt):
  def init(self,elt):
    contentElt.init(self,elt)

# $Log: contentElt.py,v $
# Revision 1.1  2002-06-28 09:43:22  ht
# XSV as package: schema doc element classes
#
