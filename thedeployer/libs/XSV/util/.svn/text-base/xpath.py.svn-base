"""Simple XPath subset implementation"""

__version__="$Revision: 1.7 $"
# $Id: xpath.py,v 1.7 2005-10-21 09:23:48 ht Exp $

# TODO: raise some errors on bogus patterns!
import types
from XSV.infoset.XMLInfoset import Element

def _slashSplit(s):
  return s.split('/')

class XPath:
  def __init__(self,str,nsdict):
    self.str=str.replace(' ','').replace('\t','').replace('\n','').replace('\r','')
    self.nsdict=nsdict
    self.pats=self.parse(self.str)

  def parse(self,str):
    disjuncts=map(lambda s:_slashSplit(s),str.split('|'))
    # weird result for //
    return map(lambda d,ss=self:map(lambda p,s=ss:s.patBit(p),
                                    d),
               disjuncts)

  def patBit(self,part):
    if part=='':
      # // in string
      return None
    elif part=='.':
      return idWrap
    if '::' in part:
      ap = part.find('::')
      axis=part[0:ap]
      part = part[ap+2:]
      if axis=='attribute':
        part='@'+part
      elif axis!='child':
        return None
    if part[0]=='@':
      if ':' in part:
        cp=part.find(':')
        ns=self.nsdict[part[1:cp]]
        part=part[cp+1:]
      else:
        part=part[1:]
        ns=None
      return lambda e,y=None,s=self,a=part,ns=ns:s.attrs(e,a,ns,y)
    else:
      if ':' in part:
        cp=part.find(':')
        ns=self.nsdict[part[0:cp]]
        part=part[cp+1:]
      else:
        ns=None
      b=part.find('[')
      if b>-1:
        f=part.find(']')
        return lambda e,y=None,s=self,n=part[0:b],ns=ns,m=self.patBit(part[b+1:f]):s.children(e,n,ns,y,m)
      else:
        return lambda e,y=None,s=self,n=part,ns=ns:s.children(e,n,ns,y)

  def find(self,element):
    res=[]
    for pat in self.pats:
      sub=self.process(element,pat)
      if sub:
        res=res+sub
    if res:
      return res
    else:
      return None

  def find1(self,nodelist,pat):
    res=[]
    for e in nodelist:
      sub=self.process(e,pat)
      if sub:
	res=res+sub
    if res:
      return res
    else:
      return None

  def process(self,element,pat):
    pe=pat[0]
    if pe:
      res=pe(element)
    elif len(pat)>1:
      # None means descendant, side effect of split is two Nones in first place
      if pat[1]:
        pat=pat[1:]
      elif len(pat)>2:
        pat=pat[2:]
      else:
        # bogus pattern ending in //
        return None
      if pat[0]:
        res=pat[0](element,1)
      else:
        # bogus pattern -- ///?
        return None
    else:
      # bogus pattern ending in /
      return None
    if not res:
      return None
    if len(pat)>1:
      return self.find1(res,pat[1:])
    else:
      return res

  def attrs(self,element,aname,ns,anywhere):
    # assume this is the end of the line
    for a in element.attributes.values():
      if (a.localName == aname and a.namespaceName==ns) or aname == "*":
        res=[a]
        break
    else:
      res=None
    if anywhere:
      for c in element.children:
        if isinstance(c,Element):
          sr=self.attrs(c,aname,ns,1)
          if sr:
            if res:
              res=res+sr
            else:
              res=sr
    return res

  def children(self,element,cname,ns,anywhere,subPat=None):
    # trickier, we need to stay in control
    res=[]
    for c in element.children:
      if isinstance(c,Element):
        if (c.localName==cname and c.namespaceName==ns) or cname == "*":
          if (not subPat) or subPat(c):
            res.append(c)
        if anywhere:
          sr=self.children(c,cname,ns,1,subPat)
          if sr:
            if res:
              res=res+sr
            else:
              res=sr
    if res:
      return res
    else:
      return None

def idWrap(e):
  return [e]

# $Log: xpath.py,v $
# Revision 1.7  2005-10-21 09:23:48  ht
# kill all whitespace, not just space
#
# Revision 1.6  2005/10/21 09:11:19  ht
# axis check in wrong place
#
# Revision 1.5  2005/10/21 09:06:48  ht
# off by one
#
# Revision 1.4  2005/10/21 09:00:07  ht
# support ::
#
# Revision 1.3  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.2  2002/09/23 21:46:53  ht
# move to string methods from string library
#
# Revision 1.1  2002/06/28 09:47:06  ht
# XSV as package: utils
#
