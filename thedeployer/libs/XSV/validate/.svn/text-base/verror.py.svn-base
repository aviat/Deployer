"""W3C XML Schema validity assessment: Error reporting"""

__version__="$Revision: 1.1 $"
# $Id: verror.py,v 1.1 2002-06-28 09:47:42 ht Exp $

from XSV.compile.SchemaError import where as addWhere

def verror(elt,message,schema,code=None,two=0,daughter=None,iitem=None):
  # code argument identifies CVC
  ve=schema.sschema.resElt.newDaughter("invalid")
  ve.newText(message)
  if code:
    ve.newAttr("code",code)
  if two:
    addWhere(ve,elt.where2)
  else:
    addWhere(ve,elt.where)
  if daughter is not None:
    ve.addChild(daughter)
  schema.sschema.errors=schema.sschema.errors+1
  if iitem is None:
    iitem=elt
  if iitem.errorCode:
    iitem.errorCode.append(" "+code)
  else:
    iitem.errorCode=[code]

def vwarn(elt,message,schema):
  if schema.sschema.dontWarn:
    return
  ve=schema.sschema.resElt.newDaughter("warning")
  ve.newText(message)
  if elt is not None:
    addWhere(ve,elt.where)


# $Log: verror.py,v $
# Revision 1.1  2002-06-28 09:47:42  ht
# validation sub-package version
#
