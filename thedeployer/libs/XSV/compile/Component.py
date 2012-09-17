"""Schema compilation: base class for all components"""

__version__="$Revision: 1.11 $"
# $Id: Component.py,v 1.11 2004-10-21 14:21:30 ht Exp $

from SchemaError import shouldnt
from QName import QName

class Component:
  isSimple=0
  prepared=0
  reffed=0
  name=None
  targetNamespace=None
  idCounter=1
  annotation=None

  def __init__(self,sschema,xrpr,ns='ns'):
    self.sschema=sschema
    if sschema is not None:
      self.schema=sschema.current
      if ns=='ns' and (self.schema is not None) and not sschema.rebuilding:
        self.targetNamespace=self.schema.targetNS
    self.xrpr=xrpr
    if xrpr is not None:
      if xrpr.__dict__.has_key('name'):
        self.name=xrpr.name
      if xrpr.__dict__.has_key('annot') and xrpr.annot:
        if len(xrpr.annot)!=1:
          shouldnt("multi-annot: %d"%len(xrpr.annot))
        self.annotation=xrpr.annot[0].component
      if xrpr.elt is not None:
        ooba=filter(lambda a:a.nsuri,
                    xrpr.elt.actualAttrs)
        if ooba:
          ooba=map(lambda a:a.elt,ooba)
          if self.annotation is None:
            self.annotation=Annotation(self.sschema,None)
          if not self.annotation.attrs:
            self.annotation.attrs=ooba
          else:
            self.annotation.attrs=self.annotation.attrs.append(ooba)
    self.id=self.idCounter
    Component.idCounter=self.id+1

  def __copy__(self):
    # cribbed from copy.py:_copy_inst_ 
    y = _EmptyClass()
    y.__class__ = self.__class__
    state = self.__dict__
    y.__dict__.update(state)
    return y

  def doVcv(self,td):
    # only relevant for Attribute and Element
    # print ('dv',self,td,self.qname.local,td.name)
    if self.valueConstraint is None:
      shouldnt('vcv')
    elif td is None:
      self.vcv=self.valueConstraint[1]
      return self.vcv
    else:
      vct=td.simple()
      if not vct.isSimple:
        # the model type of a mixed complex type
        if not (td.contentType=="mixed" and td.emptiable()):
          self.error("value constraint not allowed for element with complex type unless its emptiable and mixed: %s"%td.contentType)
        self.vcv=self.valueConstraint[1]
      else:
        if self.xrpr is None:
          item=self                     # HACK, to provide a place for actual
                                        # value to be stored for cached sForS
        else:
          item=self.xrpr.elt.elt        # all the way to XMLInfoset
        res=validateText(vct,self.valueConstraint[1],
                         item,self,vct.facets)
        if res:
          self.error("value constraint value %s not of declared type: %s"%(self.valueConstraint[1],
                                                                           res))
          self.vcv=self.valueConstraint[1]
        else:
          try:
            self.vcv=item.actualValue   # cheat
          except AttributeError:
            self.vcv=self.valueConstraint[1]
      return self.vcv

  def error(self,message,warning=0,extras=None):
    try:
      elt=self.xrpr.elt
    except AttributeError:
      elt=None
    self.schema.error(message,elt,warning,extras)

  def rebuild(self):
    # called after reln's plugged in during initFromDump
    map=self.reflectionInMap
    if map:
      for (reflName,vtype,nillable,attr) in map:
        if vtype=='boolean':
          setattr(self,attr,getattr(self,attr)=='true')
        elif vtype=='integer':
          setattr(self,attr,long(getattr(self,attr)))
        elif vtype=='list':
          # always list of atoms encoded as string
          val=getattr(self,attr)
          if val is None:
            nval=[]
          else:
            nval=val.split()
          setattr(self,attr,nval)
        elif vtype=='aspecial':
          getattr(self,reflName+"Rebuild")(getattr(self,reflName))
          # must work by side-effect, must precede pointer check
        elif vtype=='especial' or vtype=='esspecial':
          getattr(self,reflName[0]+"Rebuild")(getattr(self,reflName[0]))

  def scopeRebuild(self,val):
    # shared by Element and Attribute -- will always be a pointer
    if val is None:
      self.scope=None
    elif val=='global':
      self.scope='global'           # avoid unicode since we test for string
    else:
      # warning -- global variable hack!!!
      self.scope=self.sschema.currentCTC

  def valueConstraintRebuild(self,val):
    # shared by Element, Attribute and AttributeUse
    if val is not None:
      self.valueConstraint=(val.variety,val.value)

  def register(self,kind,table):
    if self.name:
      if table.has_key(self.name):
        self.schema.error("attempt to overwrite %s {%s}%s, ignored"%(kind,
                                                       self.schema.targetNS,
                                                                 self.name),
                          self.xrpr.elt,
                          1)
      else:
        table[self.name]=self
        self.qname=QName(None,self.name,self.schema.targetNS)
    else:
      shouldnt('nc: %s'%self)

class _EmptyClass:
    pass

from Annotation import Annotation

def init():
  # cut import loop
  global validateText
  from XSV.validate.component import validateText

# $Log: Component.py,v $
# Revision 1.11  2004-10-21 14:21:30  ht
# handle case where validateText aborts w/o an error message
#
# Revision 1.10  2004/09/09 16:42:20  ht
# more info in error msg
#
# Revision 1.9  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.8  2003/12/04 10:49:02  ht
# fix rebuilding of scope pblm
#
# Revision 1.7  2003/06/06 17:02:23  ht
# fix element default vs mixed bug
#
# Revision 1.6  2003/01/21 23:20:40  ht
# provide right item for validateText when checking a valueConstraint from a schema doc
#
# Revision 1.5  2003/01/20 12:25:06  ht
# improved robustness wrt earlier errors
#
# Revision 1.4  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.3  2002/09/23 21:25:55  ht
# move to string methods from string library
#
# Revision 1.2  2002/09/02 16:09:25  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
# Revision 1.9  2002/06/15 18:57:49  ht
# switch to reflectionInMap for rebuilding
#
# Revision 1.8  2002/06/13 21:03:08  ht
# get current complex type stack working properly
#
# Revision 1.7  2002/06/12 18:46:20  ht
# restructure in preparation for allowing either normal form to be reflected
#
# Revision 1.6  2002/06/11 13:15:28  ht
# dump non-global, non-None scope as local, rebuild properly
#
# Revision 1.5  2002/05/28 16:47:48  ht
# fix aspecial rebuilding,
# change especial rebuilding to avoid trashing reflection method,
# rebuild scope
#
# Revision 1.4  2002/05/27 22:30:25  ht
# remove debuggin print,
# actually _use_ reloaded ind dump,
# handle esspecial properly
#
# Revision 1.3  2002/05/27 20:17:54  ht
# individual normal form reload barely working, debugging prints still in
#
# Revision 1.2  2002/05/27 16:11:44  ht
# working on new restore
#
# Revision 1.1  2002/05/25 21:55:45  ht
# split more off from XMLSchema.py
#
