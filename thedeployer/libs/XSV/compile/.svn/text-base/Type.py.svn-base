"""Schema compilation: Type component"""

__version__="$Revision: 1.6 $"
# $Id: Type.py,v 1.6 2007-02-16 14:20:24 ht Exp $

from Component import Component
from QName import QName

class Type(Component):
  annotations=[]                        # TODO: implement this
  foundWhere='typeTable'
  qname=None

  def __init__(self,sschema,xrpr):
    Component.__init__(self,sschema,xrpr,'ns')
    # todo: assemble annotation from ([sc]Content),restriction/(extension|list/union)
    if self.annotation is not None:
      self.annotations=[self.annotation]

  def __getattr__(self,name):
    if name=='basetype':
      st=None
      if self.basetypeName:
        if self.schema.vTypeTable.has_key(self.basetypeName):
          st=self.schema.vTypeTable[self.basetypeName].checkBase(self)
          if st is None:
            self.basetype=None
            return
        else:
          self.error("Undefined type %s referenced as basetype of %s"%(self.basetypeName, self.name or '[anonymous]'))
          self.basetype=None
          return
        bt = st
        while (bt is not None and
               bt is not Type.urType):
          if bt is self:
            self.error("Basing a type on itself is forbidden")
            self.basetype=None
            return
          if (bt.__dict__.has_key('variety') and # can't do isinstance(bt,SimpleType
              bt.variety=='union' and
              self in bt.memberTypes):
            # should really check all the way _down_ from all the members!
            self.error("Basing a type on a union including itself is forbidden")
            self.basetype=None
            return
          if bt.__dict__.has_key('basetype'):
            bt = bt.basetype
          else:
            break
      else:
        # default case (always complex?)
        st=self.guessBase()
      if st is not None:
        self.basetype=st
      return self.basetype
    else:
      raise AttributeError,name

  def redefine(self):
    # we have a component which should be based on itself
    # note this forces some reference resolution normally left until later
    base=self.basetype
    if base is None:
      self.error("attempt to redefine in terms of non-existent type: %s"%self.name)
      return
    if base.name!=self.name:
      # note namespace identity already enforced by including
      self.error("attempt to redefine in terms of type other than self: %s vs. %s"%
                 (self.name,base.name))
      return
    if 0: # isinstance(self,SimpleType) and isinstance(base,ComplexType):
      self.error("attempt to redefine complex as simple: %s vs. %s"%
                 (self.name,base.name))
    else:
      base.name="%d %s"%(base.id,base.name)
      self.basetypeName=QName(base.qname.prefix,base.name,base.qname.uri)
      self.schema.typeTable[self.name]=self
      self.schema.typeTable[base.name]=base # for simpleContent
      self.qname=QName(None,self.name,self.schema.targetNS)


# $Log: Type.py,v $
# Revision 1.6  2007-02-16 14:20:24  ht
# implement self-derivation bar checking
#
# Revision 1.5  2005/04/14 13:23:39  ht
# fix redef name bug
#
# Revision 1.4  2003/12/04 10:49:02  ht
# fix rebuilding of scope pblm
#
# Revision 1.3  2002/11/29 21:11:48  ht
# rework contentType computation to make it lazy,
# fixing bogus extentsion of simpleContent case,
# check for mix/nomix extension cases
#
# Revision 1.2  2002/11/05 14:17:33  ht
# fix dbl redefine name bug
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
