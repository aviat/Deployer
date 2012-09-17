"""Schema compilation: SimType component"""

__version__="$Revision: 1.5 $"
# $Id: SimType.py,v 1.5 2006-12-22 15:51:42 ht Exp $

# shared by SimpleType and AbInitio

from SchemaError import shouldnt

class SimType:
  prohibitedSubstitutions=()            # checked wrt xsi:type
  def checkBase(self,derived):
    return derived.checkSimpleBase(self)

  def checkSimpleBase(self,st):
    if self.derivedBy in st.final:
      self.error("Error, %s declares %s as base, which is final"%(self.name,
                                                             st.name))
      return
    else:
      return st

  def checkComplexBase(self,st):
    # this only happens if we're the
    # {content type} of a text-only ComplexType, so need to go inside
    # its basetype
    if st.contentType!="textOnly":
      self.error("textOnly type %s may not have non-textOnly basetype %s, content type %s"%(self.name,st.name,st.contentType))
      self.basetype=None
    else:
      return st.model

  def checkMax(self,facetName,old,newF,newTable,td,oldTable):
    return newF

  def checkMin(self,facetName,old,newF,newTable,td,oldTable):
    if facetName=='minInclusive':
      b='['
      o='('
      otherName='minExclusive'
    else:
      b='('
      o='['
      otherName='minInclusive'
    if newTable.has_key(otherName):
      td.error("can't use minInclusive and minExclusive in same simple type")
      return
    if self.checkMinVals(facetName,newF.value,otherName,old,b,o,td,newTable,
                         oldTable):
      return newF
    else:
      return None

  def checkEnum(self,facetName,old,newF,newTable,td,oldTable):
    return newF

  def checkPS(self,facetName,old,newF,newTable,td,oldTable):
    return newF

  def vacuousCheck(self,facetName,old,newF,newTable,td,oldTable):
    return newF

  def checkPattern(self,facetName,old,newF,newTable,td,oldTable):
    if old is not None:
      # is this ever wrong?
      newF.value=old.value+newF.value
    return newF

  def checkMinVals(self,facetName,newVal,otherName,old,b,o,td,
                   newTable,oldTable):
    #print ('cmv',facetName,newVal,old,b,o,td,newTable,oldTable)
    # implement lots of fiddley constraints on min facets
    # some or all of this could be shared with other types . . .
    # 2005-04-14: Various bugs here -- increasing minEx does not give correct error
    if newVal is None:
      return 0
    ok=1
    if (old is not None and newVal<old.value):
      old = old.value
      ok=0
    elif self.__dict__.has_key(otherName):
      old=getattr(self,otherName)
      if (old is not None and
	  ((facetName=='minInclusive' and newVal<=old) or
	   (facetName=='minExclusive' and newVal<old))):
	ok=0
    if not ok:
      td.error("attempt to reduce range lower bound from %s%d to %s%d"%(o,old,b,newVal))
      return 0
    # check against max -- ?? -- doesn't actually say anywhere . . .
    # For now I declare that an empty range, e.g. (3,4) is OK but an
    # incoherent one, e.g. (3,3) or [3,2] is not
    # Note that what consititutes an empty range depends on fractionDigits
    # I'm not sure what follows is correct, done when tired
    # [1.1,1.1] - OK  [1.1,1.1) - no (1.1,1.1] - no (1.1,1.1) no
    if newTable.has_key('maxExclusive'):
      max=newTable['maxExclusive']
    elif oldTable.has_key('maxExclusive'):
      max=oldTable['maxExclusive']
    else:
      max=None
    if max is not None:
      max=max.value
    if max is not None and newVal>=max:
      ok=0
      o=')'
    else:
      if newTable.has_key('maxInclusive'):
        max=newTable['maxInclusive']
      elif oldTable.has_key('maxInclusive'):
        max=oldTable['maxInclusive']
      else:
        max=None
      if max is not None:
        max=max.value
      if (max is not None and ((facetName=='minExclusive' and newVal>=max) or
			 # minInclusive
			 newVal>max)):
	ok=0
	o=']'
    if not ok:
      td.error("attempt to raise range lower bound above upper bound: %s%d,%d%s"%(b,newVal,max,o))
      return 0
    return 1

# $Log: SimType.py,v $
# Revision 1.5  2006-12-22 15:51:42  ht
# improve checking of min/max
#
# Revision 1.4  2006/04/21 10:36:18  ht
# improve final and block support
#
# Revision 1.3  2005/04/14 11:46:39  ht
# add note about gaps/bugs
#
# Revision 1.2  2003/03/30 16:22:38  ht
# move facet restriction checking to SimType
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
