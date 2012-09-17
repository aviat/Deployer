"""Schema compilation: VMapping component"""

__version__="$Revision: 1.2 $"
# $Id: VMapping.py,v 1.2 2002-11-11 18:18:40 ht Exp $

from QName import QName

from SchemaError import shouldnt

class VMapping:
  def __init__(self, schema, tablename):
    self.schema = schema
    self.tablename = tablename

  def findSchema(self, uri, local):
    if uri == self.schema.targetNS:
      return self.schema
    # look it up
    if self.schema.sschema.schemas.has_key(uri):
      return self.schema.sschema.schemas[uri]
    else:
      return None
  
  def has_key(self, key):
    if key is None:
      return 0
    if not isinstance(key, QName):
      shouldnt('nk: %s'%key)
      return 0
    s = self.findSchema(key.uri, key.local)
    if s is None:
      # not an error to check, we'll record one error when we really go for it
      return 0
    return s.__dict__[self.tablename].has_key(key.local)
                        
  def __getitem__(self, key):
    s = self.findSchema(key.uri, key.local)
    if s is None:
      self.schema.error("unknown namespace for %s for %s" % (key.uri,
                                                               key.local))
      return None
    return s.__dict__[self.tablename][key.local]


# $Log: VMapping.py,v $
# Revision 1.2  2002-11-11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
