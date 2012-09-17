"""W3C XML Schema validity assessment: methods for compoents to record
results in PSVI
"""

__version__="$Revision: 1.3 $"
# $Id: assess.py,v 1.3 2004-01-31 11:42:51 ht Exp $

import XSV.infoset.XMLInfoset as XMLInfoset

from XSV.compile.Type import Type

# assess methods

def assess(self,sschema,decl):
  allfull = 1
  allnone = 1
  nochildren = 1
  for c in self.children:
    if isinstance(c, XMLInfoset.Element):
      nochildren = 0
      validationAttempted = c.__dict__.has_key("validationAttempted") and c.validationAttempted
      if validationAttempted != 'full':
        allfull = 0
      if validationAttempted and c.validationAttempted != 'none':
        allnone = 0
  attrs=self.attributes.values()
  for c in attrs:
    if isinstance(c, XMLInfoset.Attribute):
      nochildren = 0
      validationAttempted = c.__dict__.has_key("validationAttempted") and c.validationAttempted
      if validationAttempted != 'full':
        allfull = 0
      if validationAttempted and c.validationAttempted != 'none':
        allnone = 0

  if nochildren:
    if self.assessedType is not None:
      self.validationAttempted = 'full'
    else:
      self.validationAttempted = 'none'
  else:
    if allfull and self.assessedType is not None:
      self.validationAttempted = 'full'
    elif allnone and self.assessedType is None:
      self.validationAttempted = 'none'
    else:
      self.validationAttempted = 'partial'
  # print ('a',self.localName,self.assessedType!=None,allnone,self.lax)

  if self.errorCode is not None:
    self.validity = 'invalid'
  elif self.assessedType is None:
    self.validity = 'notKnown'
  else:
    has_losing_child = 0
    has_untyped_strict_child = 0
    has_non_winning_typed_child = 0
    for c in self.children:
      if not isinstance(c, XMLInfoset.Element):
        continue
      strict = c.__dict__.has_key("strict") and c.strict
      validatedType = c.__dict__.has_key("assessedType") and c.assessedType
      validity = c.__dict__.has_key("validity") and c.validity
      if validity == 'invalid':
        has_losing_child = 1
      if strict and validatedType is None:
        has_untyped_strict_child = 1
      if validatedType is not None and validity != 'valid':
        has_non_winning_typed_child = 1
    for c in attrs:
      if not isinstance(c, XMLInfoset.Attribute):
        continue
      strict = c.__dict__.has_key("strict") and c.strict
      validatedType = c.__dict__.has_key("assessedType") and c.assessedType
      validity = c.__dict__.has_key("validity") and c.validity
      if validity == 'invalid':
        has_losing_child = 1
      if strict and validatedType is None:
        has_untyped_strict_child = 1
      if validatedType is not None and validity != 'valid':
        has_non_winning_typed_child = 1
    if has_losing_child or has_untyped_strict_child:
      self.validity = 'invalid'
    # elif (has_non_winning_typed_child or
      #    (nochildren and self.validationAttempted!='full')):
      # self.validity = 'notKnown'
    else:
      self.validity = 'valid'

  if self.validity!='invalid':
    if self.assessedType is not None:
      self.typeDefinition=self.assessedType
      self.elementDeclaration=decl
    elif self.lax:
      self.typeDefinition=Type.urType
  self.validationContext=sschema.docElt
  
XMLInfoset.Element.assess=assess
XMLInfoset.Element.assessedType=None
XMLInfoset.Element.lax=0

def assess(self,sschema,decl):
  if self.errorCode:
    self.validity = 'invalid'
  else:
    self.validity = 'valid'
  if self.assessedType is not None:
    self.validationAttempted = 'full'
    if self.validity=='valid':
      self.typeDefinition=self.assessedType
      self.attributeDeclaration=decl
  else:
    self.validationAttempted = 'none'
    self.validity = 'notKnown'
  self.validationContext=sschema.docElt
  
XMLInfoset.Attribute.assess=assess
XMLInfoset.Attribute.assessedType=None


# $Log: assess.py,v $
# Revision 1.3  2004-01-31 11:42:51  ht
# improve PSVI in lax+no decl case
#
# Revision 1.2  2003/03/30 16:21:06  ht
# try to get closer to conformance wrt outcome
#
# Revision 1.1  2002/06/28 09:47:42  ht
# validation sub-package version
#
