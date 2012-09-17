"""Schema compilation: Facet component"""

__version__="$Revision: 1.7 $"
# $Id: Facet.py,v 1.7 2005-03-14 21:34:41 ht Exp $

from Component import Component
from elts.commonElt import commonElt

class Facet(Component,commonElt):
  # note this is schizo -- both elt and component
  annotation=None
  fixed=0
  def __init__(self,sschema,elt):
    commonElt.__init__(self,sschema,elt)
    self.fid=self.idCounter
    Component.idCounter=self.fid+1

  def __getattr__(self,name):
    if name=='value':
      self.value=self.val(self.auth)    # TODO: handle undef
      return self.value
    elif name=='auth':
      self.auth=self.type
      return self.auth
    else:
      raise AttributeError,name

  def init(self,elt):
    self.xrpr=self
    self.stringValue=self.value
    del self.value

  def register(self,table):
    if table.has_key(self.name):
      self.error("Not allowed multiple values for %s"%self.name)
    else:
      self.fixed=self.fixed=="1" or self.fixed=="true"
      table[self.name]=self

  def val(self,type):
    return self.stringValue

  def prepare(self):
    return self.value is not None

class Whitespace(Facet):
  name='whiteSpace'

class Precision(Facet):
  name='fractionDigits'

  def val(self,type):
    return self.stringValue in ('1','true')

class LexicalMappings(Facet):
  name='fractionDigits'

  def val(self,type):
    return self.stringValue.split()


# $Log: Facet.py,v $
# Revision 1.7  2005-03-14 21:34:41  ht
# further simple type fix -- separate type from auth
#
# Revision 1.6  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.5  2003/03/30 16:24:18  ht
# interpret fixed as boolean
#
# Revision 1.4  2003/03/29 11:19:35  ht
# todo comment
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/09/23 13:53:37  ht
# give facets their own id
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
