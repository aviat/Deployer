"""Schema compilation: Restriction component"""

__version__="$Revision: 1.15 $"
# $Id: Restriction.py,v 1.15 2006-12-22 15:51:19 ht Exp $

from Component import Component
from AbInitio import AbInitio
from List import List
from Union import Union

from SchemaError import shouldnt

_checkFacetTable={"minInclusive":'checkMin',
		 "minExclusive":'checkMin',
		 "maxInclusive":'checkMax',
		 "maxExclusive":'checkMax',
		 "totalDigits":'checkPS',
		 "fractionDigits":'checkPS',
		 "minFractionDigits":'checkPS',
		 "precision":'checkPS',
		 "lexicalMappings":'checkPS',
		 "enumeration":'checkEnum',
		 "length":'vacuousCheck',
		 "minLength":'vacuousCheck',
		 "maxLength":'vacuousCheck',
		 "pattern":'checkPattern',
                 "whiteSpace":'vacuousCheck'}

class Restriction(Component):
  builtin=0
  def __getattr__(self,name):
    if name=='facets':
      newTable=self.xrpr.facets
      if newTable.has_key('pattern'):
        # special treatment -- multiple patterns are branches
        pf=newTable['pattern']
        if (not self.builtin) and len(pf.stringValue)>1:
          pf.stringValue=['|'.join(map(lambda p:'('+p+')',pf.stringValue))]
      if (self.base is None or
          self.variety=='unknown' or
          (self.variety=='atomic' and
           self.primitiveType is None)):
        # unknown means earlier error, bail out
        self.facets={}
        return {}
      oldTable=self.base.facets
      ft=self.base
      if ft.variety!=self.variety:
        self.error("type with variety %s must not have base type defn with variety %s"%(self.variety,ft.variety))
      if self.variety=='atomic':
        auth=self.primitiveType
        tname=self.base.name
      elif self.variety=='list':
        tname='List'
        auth=List
        ft=self.base
        if 'whiteSpace' not in oldTable:
          nwsf=Whitespace(self.sschema,self.base.elt)
          nwsf.value='collapse'
          nwsf.fixed=1
          oldTable['whiteSpace']=nwsf
      elif self.variety=='union':
        tname='Union'
        auth=Union
        ft=self.base
      else:
        shouldnt('bogusv: %s'%self.variety)
      self.facets=oldTable.copy()
      allowed=auth.allowedFacets
      #print ('r',newTable.keys(),oldTable.keys())
      for facetName in newTable.keys():
        if facetName in allowed:
          newF=newTable[facetName]
          newF.type=ft
          newF.auth=auth
      for facetName in newTable.keys():
        newF=newTable[facetName]
        if facetName in allowed:
          if oldTable.has_key(facetName):
            oldF=oldTable[facetName]
          else:
            oldF=None
          if oldF is not None and oldF.fixed and newF.value!=oldF.value:
            self.error("facet %s is fixed in basetype %s, cannot be changed"%(facetName,tname))
          newNew=getattr(ft,_checkFacetTable[facetName])(facetName,
                                                           oldF,
                                                           newF,
                                                           newTable,
                                                           self,
                                                         oldTable)
          if newNew is not None:
            self.facets[facetName]=newNew
        else:
          self.error("facet %s not allowed on type %s"%(facetName,tname))
      return self.facets
    elif name not in ('variety','rootName','primitiveType','memberTypes',
                      'itemType','base','validateText'):
      raise AttributeError,name
    if not self.__dict__.has_key('base'):
      if self.super.basetype is not None:
        self.base=self.super.basetype
        if isinstance(self.base,AbInitio):
          self.primitiveType=self.base
          if name=='primitiveType':
            return self.base
      else:
        # error already signalled . . .
        self.base=None
        return None
    if name=='base':
      return self.base
    elif self.base is not None:
      return getattr(self.base,name)
    else:
      return None
    
  def prepare(self):
    return len(self.facets)==0 or 1

# $Log: Restriction.py,v $
# Revision 1.15  2006-12-22 15:51:19  ht
# improve checking of min/max
#
# Revision 1.14  2006/08/15 16:12:18  ht
# enforce simple type restriction same-variety constraint
#
# Revision 1.13  2005/04/14 11:45:56  ht
# check facets when preparing,
# make sure facets all have types before checking
#
# Revision 1.12  2005/03/14 21:34:41  ht
# further simple type fix -- separate type from auth
#
# Revision 1.11  2005/03/14 21:19:58  ht
# fix hierarchy bug -- caused whiteSpace not to propogate to built-in derived
#
# Revision 1.10  2004/10/04 11:36:47  ht
# token support for pDecimal
#
# Revision 1.9  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.8  2003/07/09 10:31:39  ht
# vacuous prepare
#
# Revision 1.7  2003/06/30 18:58:58  ht
# no facets if no base
#
# Revision 1.6  2003/03/30 16:23:37  ht
# use different basis for facet inheritance checking,
# so we always have an instance, otherwise check... will not fly
#
# Revision 1.5  2003/01/20 12:25:06  ht
# improved robustness wrt earlier errors
#
# Revision 1.4  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.3  2002/11/01 17:07:49  ht
# fail more gracefully in absence of base type
#
# Revision 1.2  2002/09/23 21:37:12  ht
# get new facet back from restriction check,
# add pattern check,
# construct multi-branch pattern in case of multiple patterns
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
