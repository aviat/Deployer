"""Schema compilation: ListFacet component"""

__version__="$Revision: 1.12 $"
# $Id: ListFacet.py,v 1.12 2005-08-10 20:30:54 ht Exp $

import re
import types

from Facet import Facet

class ListFacet(Facet):
  def register(self,table):
    if table.has_key(self.name):
      table[self.name].stringValue.append(self.stringValue)
    else:
      table[self.name]=self
      self.stringValue=[self.stringValue]

class Pattern(ListFacet):
  name='pattern'
  def __getattr__(self,name):
    if name=='regexps':
      if self.value is None:
        self.regexps=None
      else:
        self.regexps=map(lambda pat:_tryCompile(pat),
                         self.value)
      return self.regexps
    elif name=='value':
      return self.stringValue           # don't cache
    else:
      raise AttributeError,name

class Enumeration(ListFacet):
  name='enumeration'
  def __getattr__(self,name):
    if name=="value":
      self.value=map(lambda sv,s=self:s.getValue(sv),
                     self.stringValue)
      self.value=filter(lambda x:x is not None,
                        self.value)
      return self.value
    else:
      raise AttributeError,name

  def getValue(self,string):
    ff={}
    ff.update(self.type.facets)
    if ff.has_key('enumeration'):
      del ff['enumeration']
    res=self.type.validateText(string,self,self,ff,1)
    if res:
      self.error("facet enumeration value %s not a valid literal: %s"%(string,
                                                                       res))
    else:
      return self.actualValue

def init():
  global _badPat,_trivPat,_fixAnchors
  # note we allow the classes d, D, s, S, w and W because the Python
  # semantics are very nearly correct
  # Note in reading this that \\ puts a \ in the string, thereby escaping
  # the following char for the regexp, i.e \\\\ puts a \ in the regexp
  _badPat=re.compile("(^|[^\\\\])\\\\[^nrt\\|.?*\\\\+()\\[\\]\\-\\^dDsSwW]|(\\[[^\[\]]*-\\[)|,\\}|\\{[^0-9]",re.UNICODE)
  _trivPat=re.compile('.*',re.DOTALL)              # match anything, sigh
  _fixAnchors=re.compile('(^|[^\\\\\\[])([$^])')

def _tryCompile(pat):
  version=None
  if type(pat) is types.TupleType:
    version=pat[0]
    pat=pat[1]
  if _badPat.search(pat) is not None:
    #print ('losing pat',pat,_badPat.search(pat).groups())
    res=_trivPat
  else:
    try:
      # turn ^ and $ into ordinary chars, force match of whole input
      res=re.compile("(%s)$"%_fixAnchors.sub('\\1\\\\\\2',pat)) 
    except re.error:
      res=_trivPat
  if version is None:
    return res
  else:
    return (version,res)

# $Log: ListFacet.py,v $
# Revision 1.12  2005-08-10 20:30:54  ht
# allow numeric ranges,
# correct subtractive group exclusion
#
# Revision 1.11  2005/04/14 11:44:39  ht
# fix enumeration value checking
#
# Revision 1.10  2005/03/14 09:28:16  ht
# escape some $ and ^
#
# Revision 1.9  2004/08/18 08:33:15  ht
# fix _tryCompile bug
#
# Revision 1.8  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.7  2003/06/13 10:50:12  ht
# make patterns match whole input
#
# Revision 1.6  2003/03/03 20:55:39  ht
# allow \\\\ in pattern string we can compile
#
# Revision 1.5  2002/11/25 14:56:34  ht
# fix rebuilding of Enumerations to compute value
#
# Revision 1.4  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.3  2002/09/24 14:10:27  ht
# try allowing some charclasses (dsw) which Python supports well enough
#
# Revision 1.2  2002/09/23 21:33:19  ht
# compile patterns as Python regexps on demand,
# falling back to no check (via .*) if non-Python re features used
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
