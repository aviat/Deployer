"""Schema compilation: SchemaError component"""

__version__="$Revision: 1.1 $"
# $Id: SchemaError.py,v 1.1 2002-06-28 09:40:22 ht Exp $

class SchemaError(Exception):
  pass

def shouldnt(msg):
  error("Shouldn't happen "+msg)

def error(msg):
  raise SchemaError,msg

def where(elt,w):
  if w and w[3]!=0:
    if w[0]!='unnamed entity':
      elt.newAttr('entity',w[0])
    elt.newAttr('line',str(w[1]))
    elt.newAttr('char',str(w[2]))
    elt.newAttr('resource',w[3])

def whereString(w):
  if w and w[3]!=0:
    return ("in %s at line %d char %d of %s" % w)
  else:
    return "location unknown"

# $Log: SchemaError.py,v $
# Revision 1.1  2002-06-28 09:40:22  ht
# XSV as package: components
#
