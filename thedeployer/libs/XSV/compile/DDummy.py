"""Schema compilation: DDummy component"""

__version__="$Revision: 1.1 $"
# $Id: DDummy.py,v 1.1 2002-06-28 09:40:22 ht Exp $

class dumpDummy:
  reffed=0
  rebuild=None
  foundWhere=None
  def __init__(self,sschema,xrpr):
    pass

class DumpedSchema(dumpDummy):
  pass

class namespaceSchemaInformation(dumpDummy):
  schemaNamespace=None

class contentType(dumpDummy):
  model=None

class namespaceConstraint(dumpDummy):
  pass

class valueConstraint(dumpDummy):
  pass

class xpathTemp(dumpDummy):
  pass

class schemaDocument(dumpDummy):
  pass


# $Log: DDummy.py,v $
# Revision 1.1  2002-06-28 09:40:22  ht
# XSV as package: components
#
