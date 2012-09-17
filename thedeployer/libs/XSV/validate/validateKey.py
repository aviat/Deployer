"""W3C XML Schema validity assessment: Keys and friends"""

__version__="$Revision: 1.9 $"
# $Id: validateKey.py,v 1.9 2005-10-21 09:00:45 ht Exp $

from types import DictType, ListType, InstanceType

from XSV.infoset.XMLInfoset import Attribute, Element, Characters
from XSV.compile.SchemaError import whereString
from XSV.util.xstime import xstime
from XSV.compile import XMLSchemaInstanceNS as xsi

from verror import verror, vwarn

Element.keyTabs={}

def validateKeys(decl,elt):
  elt.keyTabs={}
  validateKeys1(elt,decl.keys,1)
  validateKeys1(elt,decl.uniques,0)
  subtabs={}
  # first merge all the children's keyTabs
  # TODO: think about impact of recursive validity of children on what's next
  for c in elt.children:
    if isinstance(c,Element):
      for (sk,st) in c.keyTabs.items():
        if subtabs.has_key(sk):
          subtab=subtabs[sk]
        else:
          subtab={}
          subtabs[sk]=subtab
        if type(st)==DictType:
          for (n,v) in st.items():
            if subtab.has_key(n):
              subtab[n]="losing"
            else:
              subtab[n]=v
  # now propagate upwards where there's no conflict          
  for (sk,st) in subtabs.items():
    if elt.keyTabs.has_key(sk):
      tab=elt.keyTabs[sk]
    else:
      tab={}
      elt.keyTabs[sk]=tab
    for (n,v) in st.items():
      if v!="losing":
        if not tab.has_key(n):
          tab[n]=v
  validateKeyRefs(elt,decl.keyrefs)

def validateKeys1(elt,kds,reqd):
  for key in kds:
    tab={}
    candidates=key.selector.find(elt)
    if candidates:
      for s in candidates:
        keyKey=_buildKey(s,key.fields,key.schema)
        if keyKey is not None:
          if len(keyKey)>1:
            keyKey=tuple(keyKey)
          else:
            keyKey=keyKey[0]
        else:
          if reqd:
            verror(s,
                   "missing one or more fields %s from key {%s}%s"%(key.fields,
                                                                    key.targetNamespace,
                                                                unicode(str(key.name),'utf-8')),
                   key.schema,"cvc-identity-constraint.2.2.2")
          continue
	if tab.has_key(keyKey):
          if reqd:
            code="cvc-identity-constraint.2.2.3"
          else:
            code="cvc-identity-constraint.2.1.2"
	  verror(s,"duplicate key %s for {%s}%s, first appearance was %s"%
                 (unicode(keyKey),
                  key.targetNamespace,unicode(str(key.name),'utf-8'),
                  whereString(tab[keyKey].where)),
                 key.schema,code)
	else:
	  tab[keyKey]=s
          s.hasKey=1
    elt.keyTabs[key]=tab

def _buildKey(s,fps,schema):
  keyKey=[]
  for fp in fps:
    kv=fp.find(s)
    if kv:
      # print ('f', kv,kv[0].localName)
      if len(kv)>1:
        verror(s,"Field XPath %s produced multiple hits"%fp.str,
               schema,
               "cvc-identity-constraint.3")
      if kv[0].assessedType is None:
        # has to have been validated OK to be used
        return 
      if isinstance(kv[0],Element):
        try:
          nulla=kv[0].attributes[(xsi,"nil")]
          if (nulla.validity=='valid' and
              nulla.schemaNormalizedValue == "true"):
            # pretend not here -- key will error, others OK -- NOT IN REC!!!
            return
        except KeyError:
          pass
        try:
          keyKey.append(_hashable(kv[0].actualValue))
        except AttributeError:
          # TODO: is this really OK, i.e. mixed content?
          if (len(kv[0].children)>0 and
              isinstance(kv[0].children[0],Characters)):
            keyKey.append(kv[0].children[0].characters)
          else:
            # XPath says in this case value is the empty string
            keyKey.append("")
      elif isinstance(kv[0],Attribute):
        keyKey.append(_hashable(kv[0].actualValue))
      else:
        # TODO error or shouldnt?
        vwarn(s,"oops, key value %s:%s"%(type(kv[0]),kv[0]),schema)
    else:
      return
  return keyKey

def _hashable(obj):
  if type(obj)==ListType:
    return tuple(obj)
  elif type(obj)==InstanceType and isinstance(obj,xstime):
    return str(obj)
  else:
    return obj

def validateKeyRefs(elt,krds):
  res=1
  for ref in krds:
    if ref.refer is None:
      break
    candidates=ref.selector.find(elt)
    if candidates:
      # print ('c', candidates,candidates[0].localName)
      if elt.keyTabs.has_key(ref.refer):
        keyTab=elt.keyTabs[ref.refer]
        if keyTab=='bogus':
          break
      else:
        elt.keyTabs[ref.refer]='bogus'
        verror(elt,
               "No key or unique constraint named %s applies below here, refed by keyref {%s}%s"%(unicode(str(ref.refer.qname),'utf-8'),ref.targetNamespace,
                                                                                                  unicode(str(ref.name),'utf-8')),
               ref.schema,"cvc-identity-constraint.2.3.2")
        break
      for s in candidates:
        keyKey=_buildKey(s,ref.fields,ref.schema)
        # print ('k',keyKey)
        if not keyKey:
          continue
	if len(keyKey)>1:
	  keyKey=tuple(keyKey)
	else:
	  keyKey=keyKey[0]
	if not keyTab.has_key(keyKey):
	  verror(s,"no key in %s for %s"%(unicode(str(ref.refer.qname),'utf-8'),
                                          unicode(keyKey)),
                 ref.schema,
                 "cvc-identity-constraint.2.3.2")


# $Log: validateKey.py,v $
# Revision 1.9  2005-10-21 09:00:45  ht
# more debugging
#
# Revision 1.8  2005/08/22 12:31:22  ht
# better, i hope, handling of displaying non-ascii qnames
#
# Revision 1.7  2004/05/29 09:59:36  ht
# fix no-keyrefs bug
#
# Revision 1.6  2003/03/30 18:17:07  ht
# add support for (alternating) reflection of key tables
#
# Revision 1.5  2003/02/24 18:34:32  ht
# ignore nil fields -- goes beyond REC
#
# Revision 1.4  2003/01/20 12:28:21  ht
# make sure key vals can be hashed
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:47:42  ht
# validation sub-package version
#
