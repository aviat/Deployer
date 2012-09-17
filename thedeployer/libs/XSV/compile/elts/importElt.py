"""Schema compilation first phase for import elements"""

__version__="$Revision: 1.4 $"
# $Id: importElt.py,v 1.4 2004-01-31 15:42:32 ht Exp $

from urlparse import urljoin

from commonElt import commonElt

class importElt(commonElt):
  schemaLocation=None
  namespace=None

  def init(self,elt):
    # check now to avoid going to net if poss.
    ss=self.schema.sschema
    sct=ss.schemas
    if sct.has_key(self.namespace):
      other=sct[self.namespace]
      ne=ss.resElt.newDaughter("schemaDocAttempt")
      ne.newAttr('source','import')
      if self.namespace is not None:
        ne.newAttr('namespace',self.namespace)
      fullLoc=urljoin(ss.fileNames[0],
                      self.schemaLocation or self.namespace)
      ne.newAttr('URI',fullLoc)
      if other==self.schema:
        ne.newAttr('outcome',"Failure: attempt to import containing schema's target namespace")
      elif fullLoc in other.locations:
        ne.newAttr('outcome','redundant') # i.e. we've seen this before
      else:
        ne.newAttr('outcome','skipped')   # i.e. we chose to only pursue
                                          # one file per import
        ne.newAttr('otherLocs',' '.join(other.locations))
    else:
      ss.checkinSchema(self.namespace,
                       self.schemaLocation or self.namespace,
                       ss.fileNames[0],
                       "import",0,0,elt)


# $Log: importElt.py,v $
# Revision 1.4  2004-01-31 15:42:32  ht
# *** empty log message ***
#
# Revision 1.3  2004/01/31 15:40:39  ht
# enforce ban on containing namespace import
#
# Revision 1.2  2002/09/23 21:20:18  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:43:22  ht
# XSV as package: schema doc element classes
#
