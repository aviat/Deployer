"""Schema compilation first phase for schema elements"""

__version__="$Revision: 1.2 $"
# $Id: schemaElt.py,v 1.2 2002-09-02 16:10:28 ht Exp $

from commonElt import commonElt

from XSV.compile.Schema import Schema
from XSV.compile.Annotation import Annotation

class schemaElt:
  version=None
  id=None
  def __init__(self,sschema,elt):
    self.elt=elt
    sschema.eltStack[0:0]=[self]
    if elt.hasAttrVal('targetNamespace'):
      myns=elt.attrVal('targetNamespace')
    else:
      myns=None
    if sschema.current is not None:
      if (myns!=sschema.targetNS and
          (not myns) and
          sschema.processingInclude):
        # chameleon include, OK
        myns=sschema.targetNS
        sschema.processingInclude=2
      sschema.targetNS=myns
    if sschema.schemas.has_key(myns):
      oldSchema=sschema.schemas[myns]
      oldSchema.xrpr=self
      sschema.targetNS=myns
      oldSchema.maybeSetVar('elementFormDefault',
                            'elementFormDefault','unqualified')
      oldSchema.maybeSetVar('attributeFormDefault','attributeFormDefault',
                            'unqualified')
      oldSchema.maybeSetVar('finalDefault','finalDefault','')
      oldSchema.maybeSetVar('blockDefault','blockDefault','')
      self.component=oldSchema
    else:
      self.component=Schema(sschema,self)
    sschema.current=self.component
    self.dds=[]

  def init(self,elt):
    sch=self.component
    # todo:oldSchema.annotations=oldSchema.annotations.append(self.annotations)
    if self.__dict__.has_key('annot') and self.annot:
      sch.annotations=map(lambda a:a.component,self.annot)
    if elt is not None:
      ooba=filter(lambda a:a.nsuri,
                  elt.actualAttrs)
      if ooba:
        ooba=map(lambda a:a.elt,ooba)
        if not sch.annotations:
          sch.annotations=[Annotation(sch.sschema,None)]
        if sch.annotations[0].attrs:
          sch.annotations[0].attrs=sch.annotations[0].attrs.append(ooba)
        else:
          sch.annotations[0].attrs=ooba
    sch.sschema.eltStack=sch.sschema.eltStack[1:]
    for dd in self.dds:
      if dd.name is None:
        continue
      dd.newComponent(sch)

# $Log: schemaElt.py,v $
# Revision 1.2  2002-09-02 16:10:28  ht
# minor fixups of udf/uba variety, identified by pychecker
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
