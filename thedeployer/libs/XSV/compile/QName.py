"""Schema compilation: QName component"""

__version__="$Revision: 1.6 $"
# $Id: QName.py,v 1.6 2005-10-21 08:59:49 ht Exp $

import types

from XSV.infoset.relNorm.rebuild import Mapper

class QName:
  # either QName(qname, item, sschema) or QName(prefix, local, uri) or
  #        QName(qname, nsdict, sschema) (doesn't happen????)
  def __init__(self, arg1, arg2, arg3):
    #print "QName(%s,%s,%s),%s" % (arg1, arg2, arg3,isinstance(arg2,Mapper) and arg3.processingInclude)
    if isinstance(arg2,Mapper):
      (self.prefix,self.local) = splitQName(arg1)
      if self.prefix or not arg3.processingInclude==2:
        self.uri=arg2.lookupPrefix(self.prefix)
      else:
        # chameleon include fix
        self.uri=arg3.targetNS
      if self.prefix and not self.uri:
        self.uri="error: prefixWasNotDeclared"
    elif type(arg2)  is  types.DictType:
      (self.prefix,self.local) = splitQName(arg1)
      if arg2.has_key(self.prefix):
        self.uri=arg2[self.prefix]
      elif self.prefix:
        self.uri="error: prefixWasNotDeclared"
      else:
        self.uri=None
    else:
      self.prefix = arg1
      self.local = arg2
      self.uri = arg3
    self.pair = (self.uri, self.local)

  def __cmp__(self, other):
    # print "comparing %s and %s" % (self,other)
    if not isinstance(other, QName):
      # ??? XXX
      return -1
    return cmp(self.pair, other.pair)

  def __hash__(self):
    return hash(self.pair)

  def __unicode__(self):
    # may be Unicode
    return "%s{%s}:%s" % (self.prefix or "",self.uri,self.local)

  def __str__(self):
    u=self.__unicode__()
    return u.encode('utf-8','replace')

def splitQName(qname):
  n=qname.find(':')
  if n>-1:
    prefix=qname[0:n]
    local=qname[n+1:]
  else:
    prefix=None
    local=qname
  return (prefix, local)
    

# $Log: QName.py,v $
# Revision 1.6  2005-10-21 08:59:49  ht
# more debugging
#
# Revision 1.5  2005/08/22 12:31:22  ht
# better, i hope, handling of displaying non-ascii qnames
#
# Revision 1.4  2005/03/14 09:27:49  ht
# fix encoding name
#
# Revision 1.3  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.2  2002/09/23 21:25:16  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
