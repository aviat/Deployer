"""W3C XML Schema validity assessment: add validation methods to components"""

__version__="$Revision: 1.16 $"
# $Id: component.py,v 1.16 2005-04-14 11:47:28 ht Exp $

import re
import types
from math import ceil, log10

from XSV.compile.AbInitio import AbInitio, NumericST, QNameST
from XSV.compile.AbInitio import StringST, URIReferenceST
from XSV.compile.SimpleType import SimpleType
from XSV.compile.Type import Type
from XSV.compile.SimType import SimType
from XSV.compile.List import List
from XSV.compile.Union import Union
from XSV.compile.QName import QName

from XSV.compile.SchemaError import shouldnt
from XSV.compile import XMLSchemaInstanceNS as xsi

from verror import verror, vwarn

_wsoChar=_wsChars=_fSpace=_iSpace=None  # initialised in init()

# validation methods for schema components

_abort='abort'

def validateText(typeDef, text, item, context, facets=None):
  res=typeDef.validateText(text, item, context, facets)
  # will go to either validateTextSimple or validateTextAbInitio
  if res is None:
    return    # win
  # lose
  if item is not None:
    if 'schemaNormalizedValue' in item.__dict__:
      del item.schemaNormalizedValue
    if 'actualValue' in item.__dict__:
      del item.actualValue
  if res is not _abort:
    return res

def validateTextSimple(self, text, item, context,
                       facets, doNorm=1):
  if facets is None:
    facets=self.facets
  return self.validateTextSub(text,item,context,facets,doNorm)

def validateTextAbInitio(self, text, item, context, facets=None, doNorm=1):
  # may be called directly from validateText, or via validateTextSimple
  # and validateTextAtomic
  if self is Type.urSimpleType:
    item.schemaNormalizedValue=item.actualValue=text
    return
  if facets is None:
    facets=self.facets
  if doNorm:
    snv=self.normalize(text,item,facets['whiteSpace'].value)
  else:
    snv=text
  res=checkString(snv,context,facets)
  if res is not None:
    return res
  res=self.convertToActualValue(snv,item)
  if res is not None:
    return res
  return self.checkValue(item.actualValue,context,facets)

def validateTextAtomic(self,text,item,context,facets,doNorm):
  if self.primitiveType is not None:
    return self.primitiveType.validateText(text,item,context,facets,doNorm)
  else:
    return _abort

def validateTextList(self,text,item,context,facets,doNorm):
  if doNorm:
    snv=self.normalize(text,item,facets['whiteSpace'].value)
  else:
    snv=text
  res=checkString(snv,context,facets)
  if res is not None:
    return res
  if snv=='':
    # cope with python feature
    lv=[]
  else:
    lv=snv.split(' ')
  ll=facetValue(facets,'length')
  al=len(lv)
  if ll is not None and al!=ll:
    return ' length of list is not %d'%ll
  lmin=facetValue(facets,'minLength')
  if lmin is not None and al<lmin:
    return ' length of list is < %d'%lmin
  lmax=facetValue(facets,'maxLength')
  if lmax is not None and al>lmax:
    return ' length of list is > %d'%lmax
  it=self.itemType
  if it is None:
    return _abort
  pos=1
  av=[]
  tres=[]
  for substr in lv:
    res=it.validateText(substr,item,context,it.facets,0) # cheat!!!!!!!!!!
    if res:
      tres.append(' item number %d in list%s'%(pos,res))
    else:
      av.append(item.actualValue)
    pos=pos+1
  if tres:
    return ';'.join(tres)
  else:
    item.actualValue=av
  return self.checkValue(av,context,facets)

def validateTextUnion(self,text,item,context,facets,doNorm=1):
  subres=[]
  try:
    pf=facets['pattern']
  except KeyError:
    pf=None
  for mt in self.memberTypes:
    if mt is not None:
      if pf is None:
        res=mt.validateText(text,item,context,mt.facets,doNorm)
      else:
        ff=mt.facets.copy()
        try:
          opf=ff['pattern']
          npf=Pattern(opf.schema.sschema,opf.elt)
          npf.schema=opf.schema
          npf.value=pf.value+opf.value  # conjoin two patterns
        except KeyError:
          npf=pf
        ff['pattern']=npf
        # could/should? cache this in a union-keyed dict on mt
        res=mt.validateText(text,item,context,ff,doNorm)
      if res is not None:
        subres.append(res)
      else:
        return self.checkValue(item.actualValue,context,facets)
  # no subtypes won, we lose
  return " no members of union succeeded: %s"%';'.join(subres)

def convertToActualValueAtomic(self,str,item):
  shouldnt('atomic')

def convertToActualValueUnion(self,str,item):
  shouldnt('union')

def checkValueSimple(self,value,context,facets):
  shouldnt('checkValue')

def checkString(str,context,facets):
  if facets.has_key('pattern'):
    pf=facets['pattern']
    for pat in pf.regexps:
      if type(pat) is types.TupleType:
        # XML version sensitive -- check before using
        if pf.schema.sschema.XMLVersion==pat[0]:
          xpat=pat[1]
        else:
          continue
      else:
        xpat=pat
      mr=xpat.match(str)
      if mr is None:
        pv=pf.value[pf.regexps.index(pat)]
        if type(pv) is types.TupleType:
          pv = pv[1]
        if len(pv)>20:
          pv=pv[0:20]+u'...'
        return " does not match pattern %s"%pv

def checkValue(self,value,context,facets):
  evs=facetValue(facets,'enumeration')
  if evs is not None:
    for val in evs:
      if val==value:
        return
    return " not in enumeration [%s]"%', '.join(map(lambda v:unicode(v),evs))

def normalize(self,str,item,ws):
  if item is None:
    shouldnt('noitem')
  if ws=='replace':
    str=_wsoChar.sub(' ',str)
  elif ws=='collapse':
    str=_wsChars.sub(' ',str)
    str=_iSpace.sub('',str)
    str=_fSpace.sub('',str)
  # else  ((not ws) or ws=='preserve'): pass
  item.schemaNormalizedValue=str
  return str

AbInitio.normalize=normalize
SimpleType.normalize=normalize

def checkValueS(self,val,context,facets):
  vl = len(val)
  el=facetValue(facets,'length')
  if el is not None and vl!=el:
    return " length!=%s"%el
  ml=facetValue(facets,'maxLength')
  if ml is not None and vl>ml:
    return " length>%s"%ml
  ml=facetValue(facets,'minLength')
  if ml is not None and vl<ml:
    return " length<%s"%ml
  return AbInitio.checkValue(self,val,context,facets)

def checkValueD(self,val,context,facets):
  fd = facetValue(facets,'fractionDigits')
  if fd is not None:
    # try to win quickly. . .
    if int(val) is not val:
      if fd is 0:
        shifted = val
      else:
        shifted = val*pow(10,fd)
      if int(shifted)!=shifted:
        return " has more than %s fraction digits"%fd
  td = facetValue(facets,'totalDigits')
  if td is not None and val!=0.0:
    ldig = ceil(log10(abs(val)))
    if ldig>td or val!=round(val,int(td-ldig)):
      return " has more that %s total digits"%td
  minI=facetValue(facets,'minInclusive')
  if type(minI) is types.UnicodeType:
    if minI=="NaN":
      if val!="NaN":
        return "<>%s"%minI
    elif minI=="INF":
      return "<%s"%minI
  elif minI is not None:
    if type(val) is types.UnicodeType:
      if val=="NaN":
        return "<>%s"%minI
      elif val=="-INF":
        return "<%s"%minI
    elif val<minI:
      return "<%s"%minI
  minE=facetValue(facets,'minExclusive')
  if type(minE) is types.UnicodeType:
    if minE=="NaN":
      return "<>%s"%minE
    elif minE=="INF" and val!="INF":
      return "<=%s"%minE
    elif val=="-INF":
      return "<=%s"%minE
  elif minE is not None:
    if type(val) is types.UnicodeType:
      if val=="NaN":
        return "<>%s"%minE
      elif val=="-INF":
        return "<=%s"%minE
    elif val<=minE:
      return "<=%s"%minE
  maxI=facetValue(facets,'maxInclusive')
  if type(maxI) is types.UnicodeType:
    if maxI=="NaN":
      if val!="NaN":
        return "<>%s"%maxI
    elif maxI=="-INF":
      return ">%s"%maxI
  elif maxI is not None:
    if type(val) is types.UnicodeType:
      if val=="NaN":
        return "<>%s"%maxI
      elif val=="INF":
        return ">%s"%maxI
    elif val>maxI:
      return ">%s"%maxI
  maxE=facetValue(facets,'maxExclusive')
  if type(maxE) is types.UnicodeType:
    if maxE=="NaN":
      return "<>%s"%maxE
    elif maxE=="-INF" and val!="-INF":
      return ">=%s"%maxE
    elif val=="INF":
      return ">=%s"%maxE
  elif maxE is not None:
    if type(val) is types.UnicodeType:
      if val=="NaN":
        return "<>%s"%maxE
      elif val=="INF":
        return ">=%s"%maxE
    elif val>=maxE:
      return ">=%s"%maxE
  return AbInitio.checkValue(self,val,context,facets)

def convertToValueQ(self,str,item):
  # not complete by any means
  parts=str.split(':')
  if len(parts) not in (1,2):
    raise ValueError( ", it has more than one colon or is empty")
  b=0
  if self.sschema.XMLVersion=="1.1":
    namepat=_NCNamePat11
  else:
    namepat=_NCNamePat
  if len(parts)==2:
    b=b+1
    if namepat.match(parts[0]) is None:
      raise ValueError(" -- its prefix is not a Name")
  if namepat.match(parts[b]) is None:
    raise ValueError(" -- its localName is not a Name")

  try:
    nst=item.inScopeNamespaces
  except AttributeError:
    try:
      nst=item.ownerElement.inScopeNamespaces
    except AttributeError:
      nst=item.elt.elt.inScopeNamespaces
  if len(parts) is 2:
    pref=parts[0]
    try:
      return (nst[pref].namespaceName,parts[1])
    except KeyError:
      raise ValueError( ", it has undeclared prefix: %s"%pref)
  else:
    try:
      return (nst[None].namespaceName,parts[0])
    except KeyError:
      return (None,parts[0])

def checkValueQ(self,parts,context,facets):
  if self.sschema.checkingSchema:
    if parts[0] not in self.sschema.allowedNamespaces:
      return " is qualified by an unimported non-local namespace: %s"%parts[0]
  return AbInitio.checkValue(self,parts,context,facets)

def facetValue(facets,fn):
  if facets.has_key(fn):
    return facets[fn].value
  else:
    return None

def init():
  global _wsoChar, _wsChars, _fSpace, _iSpace, _NCNamePat, _NCNamePat11
  SimpleType.validateTextAtomic=validateTextAtomic
  SimpleType.validateTextList=validateTextList
  SimpleType.validateTextUnion=validateTextUnion
  SimpleType.validateText=validateTextSimple
  SimType.checkValue=checkValue
  AbInitio.validateText=validateTextAbInitio
  NumericST.checkValue = checkValueD
  StringST.checkValue = URIReferenceST.checkValue = checkValueS
  QNameST.convertToValue = convertToValueQ
  QNameST.checkValue = checkValueQ
  _wsoChar=re.compile("[\t\r\n]")
  _wsChars=re.compile("[ \t\r\n]+")
  _iSpace=re.compile("^ ")
  _fSpace=re.compile(" $")
  from XSV import NCNamePat as _NCNamePat
  from XSV import NCNamePat11 as _NCNamePat11


# $Log: component.py,v $
# Revision 1.16  2005-04-14 11:47:28  ht
# coerce round arg to int
#
# Revision 1.15  2004/10/21 12:57:45  ht
# allow 0 wrt totalDigits
#
# Revision 1.14  2004/07/01 13:24:43  ht
# Mark some pattern values with XML-version-sensitivity,
# note the XML version of the doc being validated on the root SSchema,
# pushing and popping it appropriately,
# make pattern matching and QName checking only use the right patterns for
# the XML version of the document they are working on
#
# Revision 1.13  2004/06/30 10:43:36  ht
# fix bug in list separator
# implement fractionDigits and totalDigits
#
# Revision 1.12  2004/02/10 13:25:12  ht
# implement string length checking
#
# Revision 1.11  2004/02/06 18:46:16  ht
# support NaN, INF, -INF
#
# Revision 1.10  2004/01/31 11:47:56  ht
# improve qname validation
#
# Revision 1.9  2003/06/13 10:50:12  ht
# make patterns match whole input
#
# Revision 1.8  2003/01/20 12:26:22  ht
# avoid actualValue if not there
#
# Revision 1.7  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.6  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.5  2002/09/23 21:39:04  ht
# move to string methods from string library,
# use match-result.end to confirm pattern matches whole string
#
# Revision 1.4  2002/09/23 14:05:21  ht
# add support for compiled patterns
#
# Revision 1.3  2002/09/02 16:12:48  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.2  2002/09/01 21:22:15  ht
# note posible staleness
#
# Revision 1.1  2002/06/28 09:47:42  ht
# validation sub-package version
#
