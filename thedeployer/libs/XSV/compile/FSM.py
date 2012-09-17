"""Schema compilation: Finite State Machine implementation
for content models

See ~/work/schema/FSA_counters.txt for fuller discussion.

Briefly:

Construction and determinisation of FSAs with counters

Assume these constraints:
 
 Particles within *strong repeated particles* must either have
 {minOccurs}=={maxOccurs} or {minOccurs}=0.

 Particles within *weak repeated particles* must either have
 {minOccurs}=={maxOccurs} or {minOccurs}=0 or {maxOccurs}=unbounded.

 A *repeated particle* is one whose {minOccurs,maxOccurs} is
 other than {0,1}, {1,1}

 A *repeated particle* is *weak* if {minOccurs} <= 1, otherwise it's
 *strong*

[[This only matters if interior particle may be both initial and final in
the enclosing group]]

This is designed (:-( to rule out (a{1,2},b?){2,2}, which is known to
defeat both greedy and anti-greedy 'deterministic' algorithms.  It's
too strong -- e.g. (a{1,2},b?)* is OK, but (a{5,7})* is not, so we
play it more carefully.

[This discussion is somewhat stale and contradictory]
"""

__version__="$Revision: 1.22 $"
# $Id: FSM.py,v 1.22 2007-10-12 18:47:49 ht Exp $

# FSM for schema
import copy
import types
import sys

from Group import All, Sequence, Choice
from Element import Element
from Wildcard import Wildcard
from QName import QName
from XSV.infoset.XMLInfoset import Element as ISElement
from XSV.infoset.XMLInfoset import Characters
#from XSV.validate.verror import verror

import Particle

class FSM:
  def __init__(self):
    self.nodes = []
    self.eltTab = {}
    self.startNode = None
    self.counters = []
    self.npTab = {}
    self.nextID = 1

  def counterState(self):
    # for re-entrancy detection during subsumption
    return map(lambda c:c.count,self.counters)

  def setCounters(self,counts):
    n = len(self.counters)
    i = 0
    while i < n:
      self.counters[i].init(counts[i])
      i=i+1

  def initCounters(self):
#    print 'ic'
    for c in self.counters:
      c.init()

  def addCounter(self,cnt):
    self.counters.append(cnt)
    
  def assignIDs(self,reverse=1):
    if not self.nodes:
      return
    if reverse:
      self.nodes.reverse()
    for n in self.nodes:
      if n.id:
        continue
      #    print "assigning id %d to %s" % (self.fsm.nextID,self)
      n.id = self.nextID
      self.nextID = self.nextID + 1

  def printme(self,file):
    self.assignIDs()
    self.nodes.sort(FSMNode.compareIDs)
    for n in self.nodes:
#      try:
      file.write("%2d" % n.id)
#      except:
 #       print ('fw',n,n.id)
  #      xyzzy()
      if n.label is not None:
        file.write(" ");
        if not n.label[0].node.__dict__.has_key('id'):
          n.label[0].node.fsm.assignIDs()
        sep="("
        for m in n.label:
          file.write(sep);
          file.write("%s"%unicode(m));
          sep=", "
        file.write(")")
      file.write(":\n")
#      if n.label:
#  	sys.stdout.write("[")
#  	for nn in n.label:
#  	  sys.stdout.write("%d " % nn.id)
#  	sys.stdout.write("]")
      for e in n.edges:
        e.printme(file)
        file.write("\n");
        
  def asXML(self):
    res=ISElement(None,None,"fsm")
    self.assignIDs(0)
    self.nodes.sort(FSMNode.compareIDs)
    for n in self.nodes:
      ne=res.newDaughter("node")
      ne.newAttr('id',("%s" % n.id))
      nen=0
      if n.isEndNode():
	ne.newAttr('final','true')
      else:  
        n.edges.sort(FSMEdge.compare)
      if len(n.counters)>0:
        ne.newAttr('cnt',str(map(lambda c:unicode(c),n.counters)))
      for e in n.edges:
        if e.__class__ is ExitEdge:
          fd=e.descC()
          if fd!="":
            ne.newAttr('actions',fd)
          continue
        ee=ne.newDaughter("edge")
        lab=unicode(str(e),'utf-8')
        ed=e.descC()
        if ed!="":
          ee.newAttr('actions',ed)
        ee.newAttr('label',lab)
        ee.newAttr('dest',("%s" % e.dest.id))
    return res

  # cf Aho & Ullman p93
  # but note we never have two identical labels, so we only
  # have to worry about lambda arcs
  def determinise(self):
    D = FSM()
    D.counters = self.counters
    D.startNode = FSMNode(D)
    D.startNode.label = _eclosure(self.startNode)
    D.unmarkedNodes = [D.startNode]
    while D.unmarkedNodes:
      x = D.unmarkedNodes.pop()
      destnodes = {}
      for n in x.label:
        checkers = n.checkers
        maxers = n.maxers
        n = n.node
	for e in n.edges:
          if e.__class__ is not EmptyEdge:
            if e.__class__ is ExitEdge:
              ee=e.clone(x)
            else:
              y = _eclosure(e.dest)
              for n in D.nodes:
                if y == n.label:
                  break
              else:
                n = FSMNode(D)
                D.unmarkedNodes.append(n)
                n.label = y
              ee=e.clone(x, n)
            ee.checkers=ee.checkers+checkers
            ee.maxers=ee.maxers+maxers
    return D

  def subsumed(self, fsm):
    # Check whether self (d) is subsumed by fsm (b), by parsing all paths thru self
    # Modelled on validateElement.validateElementModel
    procStates = []
    fsm.initCounters()
    self.initCounters()
    unprocStates = [(fsm.startNode,self.startNode,
                     fsm.counterState(),self.counterState())]
    while unprocStates:
      p=unprocStates[0]
      b=p[0]
      d=p[1]
      #print ('sub',b.id,d.id,p[2],p[3])
      sys.stdout.flush()
      self.setCounters(p[3])
      dl=d.edges
      i=len(dl)-1
      realProgress = False
      while i>=0:
        fsm.setCounters(p[2])   # in case we did an incr in b
        de=dl[i]
        win=0
        if de.__class__ is IncrEdge:
          # only if no other way forward
          if realProgress:
            break
          elif de.guardsOK():
            de.cnt.incr()
            de.initMins()
            dl=de.dest.edges
            i=len(dl)-1
          continue
        elif not de.guardsOK():
          i = i - 1
          continue
        bl=b.edges
        j=len(bl)-1
        while j>=0:
          be=bl[j]
          sr=be.subsumes(de)
          if type(sr)==types.StringType:
            return ('notSubType',de,d,b,sr)
          elif type(sr)==types.TupleType:
            return sr
          if sr:
            if be.__class__ is IncrEdge:
              ns=(be.dest,p[1],fsm.counterState(),p[3])
              if ns not in procStates:
                if ns not in unprocStates:
                  unprocStates.append(ns)
              win=1
              break
            if sr==2:
              # two element edges
              # what about nillable/identity constraints?
              myDec=de.decl
              otherDec=be.decl
              if (myDec is not None and
                  otherDec is not None):
                if (myDec.typeDefinition is not None and
                  otherDec.typeDefinition is not None and
                  (type(myDec.scope) is not types.StringType or
                   type(otherDec.scope) is not types.StringType)):
                  ofinal=otherDec.typeDefinition.final
                  if 'extension' in ofinal:
                    finals=ofinal
                  elif ofinal is ():
                    finals=('extension',)
                  else:
                    finals=['extension']+list(ofinal)
                  if (not myDec.typeDefinition.isSubtype(otherDec.typeDefinition,finals)):
                    return ('notSubType',de,d,b,be)
                if (otherDec.valueConstraint is not None and
                    otherDec.valueConstraint[0]=='fixed' and
                    (myDec.valueConstraint is None or
                     myDec.valueConstraint[0]!='fixed' or
                     myDec.valueConstraint[1]!=otherDec.valueConstraint[1])):
                  return ('badFixed',de,d,b,be)
            win=1
            realProgress = 1
            # check end status
            if sr!=3:
              ns=(be.dest,de.dest,fsm.counterState(),self.counterState())
              if ns not in procStates:
                if ns not in unprocStates:
                  unprocStates.append(ns)
            break
          j = j-1
        if not win:
          return ('noparse',de,d,b)
        i = i-1
      procStates.append(p)
      unprocStates=unprocStates[1:]
    # success

  def subsumptionError(self,badGuy,other,checkResult,variety,rName,bName):
    if len(checkResult)==3:
      (rType,nodeR,nodeB) = checkResult
    elif len(checkResult)==4:
      (rType,edgeR,nodeR,nodeB) = checkResult
    else:
      (rType,edgeR,nodeR,nodeB,extra) = checkResult
      
    pics=[Characters(None,"\nBase model:\n"),
          other.asXML(),
          Characters(None,"\nThis model:\n"),
          self.asXML()]
    if rType=='noparse':
      lab=unicode(str(edgeR),'utf-8')
      badGuy.error("Content model of %s not actually a restriction of base %s %s: a %s element at node %s of this model can't be matched by any edge leaving node %s of the base"%(rName,variety,bName,lab,nodeR.id,nodeB.id),0,pics)
    elif rType=='notSubType':
      lab=unicode(str(edgeR),'utf-8')
      dtd=edgeR.decl.typeDefinition.name
      if type(extra)==types.StringType:
        badGuy.error("Content model of %s not actually a restriction of base %s %s: the %s element at node %s of this model has a type (%s) not derived from the type (%s) of the global element accepted by the matching wildcard edge leaving node %s of the base"%(rName,variety,bName,lab,nodeR.id,dtd,extra,nodeB.id),0,pics)
      else:
        btd=extra.decl.typeDefinition.name
        badGuy.error("Content model of %s not actually a restriction of base %s %s: the %s element at node %s of this model has a type (%s) not derived from the type (%s) of the matching %s edge leaving node %s of the base"%(rName,variety,bName,lab,nodeR.id,dtd,btd,lab,nodeB.id),0,pics)
    elif rType=='uwNotSubType':
      (rType,edgeB,edgeR,uDecl) = checkResult
      lab=unicode(str(edgeB),'utf-8')
      dtd=uDecl.typeDefinition.name
      badGuy.error("Content model of %s not actually a restriction of base %s %s: the wildcard at node %s of this model allows only one element type, but it has a type (%s) not derived from the type (%s) of the element %s leaving node %s of the base"%(rName,variety,bName,edgeR.source.id,dtd,edgeB.decl.typeDefinition.name,lab,edgeB.source.id),0,pics)
    elif rType=='uwNoType':
      (rType,edgeB,edgeR) = checkResult
      lab=unicode(str(edgeB),'utf-8')
      badGuy.error("Content model of %s not actually a restriction of base %s %s: the wildcard at node %s of this model allows elements labelled %s leaving node %s (also allowed by the element edge of that name from node %s of the base) but assigns them no type"%(rName,variety,bName,edgeR.source.id,lab,edgeB.source.id),0,pics)
    elif rType=='notEnd':
      badGuy.error("Content model of %s not actually a restriction of base %s %s: no way forward from this models' end state %s from the base's node %s which gets to an end state"%(rName,variety,bName,nodeR.id,nodeB.id),0,pics)
    elif rType=='badFixed':
      lab=unicode(str(edgeR),'utf-8')
      bvc=extra.decl.valueConstraint[1]
      badGuy.error("Content model of %s not actually a restriction of base %s %s: the %s element at node %s of this model does not have a 'fixed' value the same as that (%s) of the matching %s edge leaving node %s of the base"%(rName,variety,bName,lab,nodeR.id,bvc,lab,nodeB.id),0,pics)
    else:
      shouldnt('notSubsumed')

  def newNodePlus(self,node,edgelistC,edgelistM):
    if len(edgelistC)>0 or len(edgelistM)>0:
      # should this be sorted?
      kk = tuple(edgelistC+[0]+edgelistM+[node])
      #print ('nnpc',node.id,len(edgelistC),len(edgelistM),self.npTab.has_key(kk))
    else:
      kk=node
      #print ('nnp',kk.id,self.npTab.has_key(kk))
    sys.stdout.flush()
    try:
      return self.npTab[kk]
    except:
      nn=NodePlus(node,edgelistC,edgelistM)
      self.npTab[kk]=nn
      return nn

class NodePlus:
  def __init__(self,node,edgelistC,edgelistM):
    self.node = node
    self.checkers = []
    self.maxers = []
    for edge in edgelistC:
      self.checkers.extend(edge.checkers)
    for edge in edgelistM:
      self.maxers.extend(edge.maxers)

  def __str__(self):
    sim="%d"%self.node.id
    sep="("
    if len(self.checkers)!=0:
      for c in self.checkers:
        sim=sim+sep
        sim=sim+c.toString(0)
        sep=", "
    if len(self.maxers)!=0:
      for c in self.maxers:
        sim=sim+sep
        sim=sim+c.toString(-1)
        sep=", "
    if sep=="(":
      return sim
    else:
      return sim+")"

class Counter:
  idBase='a'
  def __init__(self,particle,fsm,min,max):
    fsm.addCounter(self)
    self.min=min
    self.max=max
    self.particle=particle
    self.id=self.idBase
    Counter.idBase=incrString(Counter.idBase)

  def __str__(self):
    return self.toString(0)

  def init(self,value=0):
    self.count = value

  def incr(self):
    self.count = self.count+1
    
  def checkMin(self):
    return self.count>=self.min

  def maxedOut(self):
    return self.max==self.count
  
  def toString(self,style):
    if style==1:
      return "%s++"%self.id
    elif style==-1:
      return "%s|"%self.id
    else:
      return "%s!"%self.id

class FSMEdge:
  def __init__(self, source):
    self.checkers=[]
    self.maxers=[]
    self.source = source
    source.addEdge(self)

  def compare(self,other):
    if self.rank<other.rank:
      return -1
    elif self.rank>other.rank:
      return 1
    else:
      return self.compare(other)

  def addChecker(self,cnt):
    self.checkers.append(cnt)

  def addMaxer(self,cnt):
    self.maxers.append(cnt)

  def descC(self):
    first=1
    res=""
    for c in self.checkers:
      if not first:
        res=res+";"+c.toString(0)
      else:
        res=res+c.toString(0)
      first=0
    for c in self.maxers:
      if not first:
        res=res+";"+c.toString(-1)
      else:
        res=res+c.toString(-1)
      first=0
    return res

  def printC(self,file):
    for c in self.checkers:
      file.write(";")
      file.write(c.toString(0))
    for c in self.maxers:
      file.write(";")
      file.write(c.toString(-1))

class RealEdge(FSMEdge):
  # persists in determinised automata
  def __init__(self,source):
    FSMEdge.__init__(self,source)

  def checkMins(self):
    for c in self.checkers:
      if not c.checkMin():
        c.errmsg="Min not reached: %s"%c.min
        return False
    return True

  def initMins(self):
    for c in self.checkers:
      c.init()

  def maxedOut(self):
    for c in self.maxers:
      if c.maxedOut():
        return True
    return False

  def guardsOK(self):
    return self.checkMins()

  def overlap(self,other):
    # does this edge overlap with other
    if (other.__class__ is ExitEdge or
        other.__class__ is IncrEdge):
      # we're not, or E/I E.overlap would have caught this
      return
    elif other.__class__ is ElementEdge:
      return self.overlapWithE(other)
    elif other.__class__ is WildEdge:
      return self.overlapWithW(other)
    else:
      return self.overlapWithM(other)

  def clone(self,other):
    other.checkers=self.checkers
    other.maxers=self.maxers
  
  def match(self,c):
    return
  
  def matchEnd(self):
    return
  
class EmptyEdge(FSMEdge):
  rank = 10
  def __init__(self,source,dest):
    FSMEdge.__init__(self,source)
    self.dest=dest

  def clone(self,source,dest):
    e=EmptyEdge(source,dest)
    RealEdge.clone(self,e)
    return e

  def printme(self,file):
    file.write("    L->%d" % self.dest.id)
    self.printC(file);

  def compare(self,other):
    return 0

class ExitEdge(RealEdge):
  rank = 6
  dest = None

  def __init__(self,source):
    RealEdge.__init__(self,source)

  def __str__(self):
    return "$"

  def clone(self,source):
    e=ExitEdge(source)
    RealEdge.clone(self,e)
    return e

  def printme(self,file):
    file.write("    $->")
    self.printC(file);

  def subsumes(self,other):
    if (other.__class__ is ExitEdge and
        self.guardsOK() and
        other.guardsOK()):
      return 3
    else:
      return 0

  def compare(self,other):
    return 0

  def matchEnd(self):
    if self.guardsOK():
      return True

  def overlap(self,other):
    return

class TestEdge(RealEdge):
  def __init__(self,source,dest,decl):
    RealEdge.__init__(self,source)
    self.dest=dest
    self.decl=decl

  def printme(self,file):
    file.write("    %s->%s"%(unicode(str(self),'utf-8'),self.dest.id))
    self.printC(file);

class ElementEdge(TestEdge):
  rank = 2
  def __init__(self,qname,decl,source,dest,maybeFaL=None):
    TestEdge.__init__(self,source,dest,decl)
    self.qname=qname
    self.uri=self.qname.uri or None
    self.local=self.qname.local

  def __str__(self):
    if self.decl is None:
      # no decl yet
      return str(self.qname)+"*"
    else:
      return str(self.qname)

  def clone(self,source,dest):
    e=ElementEdge(self.qname,self.decl,source,dest)
    RealEdge.clone(self,e)
    return e

  def compare(self,other):
    if self.qname < other.qname:
      return -1
    elif self.qname > other.qname:
      return +1
    else:
      return 0

  def guardsOK(self):
    return ((not self.maxedOut()) and
            self.checkMins())

  def canStep(self,nsName,localName):
    return (self.guardsOK() and
            nsName==self.uri and
            localName==self.local)

  def match(self,c):
    if self.canStep(c.namespaceName,c.localName):
      self.initMins()
      return self.dest
    
  def subsumes(self,other):
    if (other.__class__ is ElementEdge and
        other.guardsOK() and
        self.canStep(other.qname.uri,other.qname.local)):
      # what about nillable/value constraints/entity constraints?
      other.initMins()
      self.initMins()
      return 2
    elif (other.__class__ is WildEdge and
          other.guardsOK()):
      ow = other.decl
      if ow.allows(self.qname.uri):
        if ow.processContents=="skip":
          # definite loss
          return ('uwNoType',self,other)
        else:
          # may be OK if there's only one hit for this wildcard and it's us
          tc = 0
          for s in ow.schema.sschema.schemas.values():
            print ('wc',s.targetNS,ow.allows(s.targetNS or None),len(s.elementTable))
            if ow.allows(s.targetNS or None):
              tc = tc+len(s.elementTable)
          print ('ew',self.qname.local,tc)
          if tc==0:
            return 0
          else:
            if (ow.schema.vElementTable.has_key(self.qname) and
                ow.schema.vElementTable[self.qname] is not None):
              gd=ow.schema.vElementTable[self.qname]
              print ('wsc',gd.typeDefinition.name,self.decl.typeDefinition.name)
              if (self.decl is not None and
                  gd.typeDefinition.isSubtype(self.decl.typeDefinition,['extension']+self.decl.typeDefinition.final)):
                if tc==1:
                  self.initMins();
                  other.initMins();
                  return 1
                else:
                  # we can't cover everything, but maybe someone else can
                  return 0
              else:
                return ('uwNotSubType',self,other,gd)
            else:
              if ow.decl=='lax':
                return ('uwNoType',self,other)
              else:
                return 0
      else:
        return 0
    else:
      return 0

  def overlapWithW(self,other):
    return other.overlapWithE(self)

  def overlapWithE(self,other):
    if self.qname==other.qname:
      return "%s/%s" % (self.qname,other.qname)

  def overlapWithM(self,other):
    pass

class WildEdge(TestEdge):
  rank = 3
  def __init__(self,decl,source,dest,maybeFaL=None):
    TestEdge.__init__(self,source,dest,decl)

  def __str__(self):
    return str(self.decl)

  def clone(self,source,dest):
    e=WildEdge(self.decl,source,dest)
    RealEdge.clone(self,e)
    return e

  def compare(self,other):
    if self.decl.allowed < other.decl.allowed:
      return -1
    elif self.decl.allowed > other.decl.allowed:
      return +1
    else:
      return 0

  def guardsOK(self):
    return ((not self.maxedOut()) and
            self.checkMins())

  def match(self,c):
    if (self.guardsOK() and
        self.decl.allows(c.namespaceName or None)):
      self.initMins()
      return self.dest

  def subsumes(self,other):
    if not self.guardsOK():
      return 0
    bw=self.decl
    if other.__class__ is ElementEdge:
      if not other.guardsOK():
        return 0
      # element (other) vs. wildcard (self)
      if bw.allows(other.uri or None):
        # Wildcard vis a vis explicit decl -- by cases wrt processContents
        if bw.processContents=="skip":
          self.initMins();
          other.initMins();
          return 1
        else:
          # I don't _think_ it makes sense to tryHardForDecl here -- there
          # might not _be_ any instance
          if (bw.schema.vElementTable.has_key(other.qname) and
              bw.schema.vElementTable[other.qname] is not None):
            gd=bw.schema.vElementTable[other.qname]
            if (other.decl is not None and
                other.decl.typeDefinition.isSubtype(gd.typeDefinition,['extension']+gd.typeDefinition.final)):
              self.initMins();
              other.initMins();
              return 1
            else:
              return gd.typeDefinition.name
          else:
            # lose if strict, as base wouldn't allow elt (no global defn)
            if bw.processContents=="lax":
              self.initMins();
              other.initMins();
              return 1
            else:
              return 0
      else:
        return 0
    elif other.__class__ is WildEdge:
      if not other.guardsOK():
        return 0
      if other.decl.subsumed(bw):
        self.initMins();
        other.initMins();
        return 1
    else:
      return 0

  def overlapWithW(self,other):
    if not self.decl.intersect(other.decl).isEmpty():
      return "%s/%s" % (self.decl,other.decl)

  def overlapWithE(self,other):
    if self.decl.allows(other.uri):
      return "%s/%s" % (self.decl,other.qname)

  def overlapWithM(self,other):
    pass

class IncrEdge(TestEdge):
  rank = 5
  def __init__(self,cnt,source,dest):
    TestEdge.__init__(self,source,dest,None)
    self.cnt=cnt

  def __str__(self):
    return "++(%s)"%self.cnt.id

  def clone(self,source,dest):
    e=IncrEdge(self.cnt,source,dest)
    RealEdge.clone(self,e)
    dest.addCounter(self.cnt)
    return e

  def compare(self,other):
    if self.cnt.id < other.cnt.id:
      return -1
    elif self.cnt.id > other.cnt.id:
      return +1
    else:
      return 0

  def guardsOK(self):
    return (self.checkMins() and
            not self.cnt.maxedOut())

  def matchEnd(self):
    return self.match(None)

  def match(self,c):
    if self.guardsOK():
      self.cnt.incr()
      self.initMins()
      return self.dest

  def subsumes(self,other):
    if self.guardsOK():
      self.cnt.incr()
      self.initMins()
      return 1

  def overlap(self,other):
    if other.__class__ is IncrEdge:
      if self.cnt is other.cnt:
        return "%s/%s"%(unicode(str(self),'utf-8'),unicode(str(other),'utf-8'))

class FSMNode:
  id=None
  def __init__(self, fsm):
    fsm.nodes.append(self)
    self.fsm = fsm
    self.edges = []
    self.label = None
    self.mmark = None
    self.counters = []

  def isEndNode(self):
    for e in self.edges:
      if e.__class__ is ExitEdge:
        return True
    return False

  def makeEndNode(self):
    ExitEdge(self)

  def compareIDs(self,other):
    if self.id < other.id:
      return -1
    elif self.id > other.id:
      return +1
    else:
      return 0

  def addEdge(self,edge):
    # This means Incr's come _last_, because
    # validateElementModel iterates backwards
    # That means we defer to a real edge,
    # (Only happens at beginning of loop?)
    # which is what makes us greedy
    if edge.__class__ is IncrEdge:
      self.edges.insert(0,edge)
    else:
      self.edges.append(edge)

  def addCounter(self,cnt):
    if cnt not in self.counters:
      self.counters.append(cnt)

# cf Aho & Ullman p92

def _eclosure(n):
  # we use the marks to accumulate all the counters involved in
  # reaching a particular state
  #print ('ec',n.id)
  fsm=n.fsm
  n.cmark=[]
  n.mmark=[]
  STACK = [n]
  ECLOSURE = [fsm.newNodePlus(n,n.cmark,n.mmark)]
  while STACK:
    s = STACK.pop()
    #print ('s',s.id)
    for e in s.edges:
      if e.__class__ is EmptyEdge:
	t = e.dest
	if t.mmark is None:
          #          print ('ecy',t.id)
          if len(e.checkers)>0:
            ncmark=s.cmark+[e]
          else:
            ncmark=s.cmark
          t.cmark=ncmark
          if len(e.maxers)>0:
            nmmark=s.mmark+[e]
          else:
            nmmark=s.mmark
          t.mmark=nmmark
	  ECLOSURE.append(fsm.newNodePlus(t,ncmark,nmmark))
	  STACK.append(t)
#        else:
 #         print('ecn',t.id)
  ECLOSURE.sort() # so == will work
  for m in ECLOSURE:
    m.node.cmark=None
    m.node.mmark=None
  # print ('ec',n.id,map(lambda e:e.id,ECLOSURE))
  return ECLOSURE

# Check a FSM is deterministic

def _checkFSM(fsm):
  for n in fsm.nodes:
    for e in range(len(n.edges)):
      l = n.edges[e]
      for f in range(0,e):
        m = n.edges[f]
        r = l.overlap(m)
        if r is not None:
          return r

def _translateA(self, next, loopOverhead, maybeFaL):
  # Could be more efficient if we did a lot of work to unpack
  # the particles inside, but as it is this will work whatever
  # relaxing we do on all-group contents
  fsm = next.fsm
  first = FSMNode(fsm)
  postIncr = FSMNode(fsm)
  minsExit = EmptyEdge(first, next)
  EmptyEdge(postIncr,first)
  for particle in self.particles:
    mbfal = True
    for p in self.particles:
      if p is not particle:
        mbfal = mbfal and particle.occurs[0]==0
    cnt = Counter(particle,fsm,1,1)
    subLast = FSMNode(fsm)
    IncrEdge(cnt,subLast,postIncr)
    subFirst = particle.translate(subLast, loopOverhead, mbfal)
    EmptyEdge(first, subFirst).addMaxer(cnt)
    minsExit.addChecker(cnt)
  return first

def _translateE(self, next, loopOverhead, maybeFaL):
  # what do I do if there are no edges, i.e. abstract element with
  # no descendants?
  fsm = next.fsm
  eltTab = fsm.eltTab
  n = FSMNode(fsm)
  if self.abstract!='true':
    ElementEdge(self.qname,self, n, next, maybeFaL)
  if eltTab.has_key(self.qname):
    if self.typeDefinition  is not  eltTab[self.qname].typeDefinition:
      self.error("illegal redeclaration of %s" % self.qname)
  else:
    eltTab[self.qname]=self
  if (type(self.scope) is types.StringType and
      'substitution' not in self.prohibitedSubstitutions):
    # used to be self.schema.vElementTable[qname].equivClass -- why???
    for e in self.equivClass:
      if e.abstract!='true':
        ElementEdge(e.qname, e, n, next, maybeFaL)
      if eltTab.has_key(e.qname):
        if e.typeDefinition  is not  eltTab[e.qname].typeDefinition:
          self.error("illegal redeclaration of %s" % e.qname)
      else:
        eltTab[e.qname]=e
  return n

def _translateW(self, next, loopOverhead, maybeFaL):
  n = FSMNode(next.fsm)
  WildEdge(self, n, next, maybeFaL)
  return n

def _translateC(self, next, loopOverhead, maybeFaL):
  n = FSMNode(next.fsm)
  for particle in self.particles:
    m = particle.translate(next,loopOverhead, True)
    EmptyEdge(n, m)
  return n

def _translateS(self, next, loopOverhead, maybeFaL):
  n = next
  rmodel = copy.copy(self.particles)
  rmodel.reverse()
  subMBF = []
  mbf = True
  for p in self.particles:
    subMBF.append(mbf)
    mbf = mbf and p.occurs[0]==0
  subMBL = True
  for particle in rmodel:
    smbf = subMBF.pop()
    n = particle.translate(n,loopOverhead,smbf and subMBL)
    subMBL = subMBL and particle.occurs[0]==0
  return n

def _translateP(self, next, loopOverhead, maybeFaL):
  fsm = next.fsm
  if self.term is None:
    # undefined ref?
    if self.termType=='element' and self.termName:
      # we can check the content model, recursive type check may fail
      qq=self.termName
    else:
      qq=Particle.UndefQName
  min=self.occurs[0]
  max=self.occurs[1]
  if (loopOverhead!=0 and maybeFaL and
      (not (min==0 or
            min==max or
            (loopOverhead==2 and
             (max is None))))):
    self.error("violation of constraints on exponents",
               1)
  if max is None or max > 1:
    # need a loop, overkill if no counter needed
    cnt = None
    postIncr = FSMNode(fsm)
    subLast = FSMNode(fsm)
    if self.term is not None:
      if min < 2:
        lo = 2
      else:
        lo = 1
      subFirst = self.term.translate(subLast,lo,maybeFaL)
    else:
      subFirst = FSMNode(fsm)
      ElementEdge(qq, None, subFirst, subLast, maybeFaL)
    first = FSMNode(fsm)
    entry = EmptyEdge(first,subFirst)
    EmptyEdge(postIncr,first)
    if min>1 or max is not None:
      # do counter stuff
      if min==0:
        outEdge = EmptyEdge(first,next)
      else:
        outEdge = EmptyEdge(postIncr,next)
      cnt = Counter(self,fsm,min,max)
      IncrEdge(cnt,subLast,postIncr)
      outEdge.addChecker(cnt)
      entry.addMaxer(cnt)
    else:
      # simple Kleene * and + cases
      EmptyEdge(subLast,postIncr)
      if min==0:
        EmptyEdge(first,next)
      else:
        EmptyEdge(postIncr,next)
  else:
    # either (0,1) or (1,1)
    if self.term is not None:
      first = self.term.translate(next,maybeFaL and loopOverhead, maybeFaL)
    else:
      first = FSMNode(fsm)
      ElementEdge(qq, None, first, next, maybeFaL)
    if min==0:
      EmptyEdge(first, next)
  return first

def UniqueFSM(particle):
  ndfsm = FSM()
  end = FSMNode(ndfsm)
  ExitEdge(end)
  start = particle.translate(end,False,True)
  ndfsm.startNode = start
  #ndfsm.printme(sys.stdout)
  fsm = ndfsm.determinise()
  #fsm.assignIDs(0)
  #fsm.printme(sys.stdout)
  return (fsm,_checkFSM(fsm))

# With thanks to Simon Brunning, see
#    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/426333

CHAR_RANGES = [
#  [ord('0'), ord('9')], # digits
#  [ord('A'), ord('Z')], # upper case
  [ord('a'), ord('z')], # lower case
  ]

def incrString(string):
  '''Increment a string.'''
  string_chars = list(string)
  string_chars[-1] = chr(ord(string_chars[-1]) + 1)
  for index in range(-1, -len(string_chars), -1):
    for char_range in CHAR_RANGES:
      if ord(string_chars[index]) == char_range[1] + 1:
        string_chars[index] = chr(char_range[0])
        string_chars[index-1] = chr(ord(string_chars[index-1]) + 1)
  for char_range in CHAR_RANGES:
    if ord(string_chars[0]) == char_range[1] + 1:
      string_chars[0] = chr(char_range[0])
      string_chars.insert(0, chr(char_range[0]))
  return ''.join(string_chars)

def init():
  Particle.Particle.translate=_translateP
  Sequence.translate=_translateS
  Choice.translate=_translateC
  Wildcard.translate=_translateW
  Element.translate=_translateE
  All.translate=_translateA

# $Log: FSM.py,v $
# Revision 1.22  2007-10-12 18:47:49  ht
# another list optimisation consequence missed
#
# Revision 1.21  2006/03/19 19:20:26  ht
# weird wildcard subsumption case
#
# Revision 1.20  2006/03/16 15:06:41  ht
# fix UPA bug wrt as it were a+ by slight rearrangement to empty arcs,
# test fixed value constraints OK as part of checking edge subsumption
#
# Revision 1.19  2005/10/10 14:09:17  ht
# forestall post-error crash
#
# Revision 1.18  2005/08/22 12:31:22  ht
# better, i hope, handling of displaying non-ascii qnames
#
# Revision 1.17  2005/08/19 11:58:33  ht
# Allow for more than 26 counters in a schema
#
# Revision 1.16  2005/04/15 13:52:15  ht
# give up on MaxEdge, handle max checking more like min checking,
# implement all groups properly
#
# Revision 1.15  2005/04/14 10:31:41  ht
# fix over-counting cases
#
# Revision 1.14  2005/04/13 16:32:51  ht
# first attempt at proper handling of numeric exponents during subsumption checking
#
# Revision 1.13  2005/04/12 18:42:02  ht
# Having moved the greedy counter/backtracking/resetting code
# to a branch, this attempts to re-implement the other changes from
# that branch, i.e.
#  * short explanation wrt counters
#  * distinguish weak and strong overhead loops
#  * <all> bug fix
#  * Fix kleene + bug (was == *)
#
# Revision 1.12  2004/05/20 09:50:20  ht
# remove some performance bottlenecks
#
# Revision 1.11  2004/05/18 18:02:07  ht
# changed min check to plain guard
#
# Revision 1.10  2004/05/17 17:31:15  ht
# plus-edge approach to numeric exponents working?
#
# Revision 1.9  2004/05/16 16:41:19  ht
# cul-de-sac wrt counters
#
# Revision 1.6  2004/04/01 13:31:43  ht
# work on final/block a bit
#
# Revision 1.5  2003/12/04 10:52:42  ht
# handle display of subsumption failures locally
#
# Revision 1.4  2002/11/25 11:39:35  ht
# protect against missing decl
#
# Revision 1.3  2002/11/11 18:18:40  ht
# use unicode properly for names/dumping
#
# Revision 1.2  2002/11/05 14:18:22  ht
# package FSM construction and checking and move to FSM
#
# Revision 1.1  2002/06/28 09:40:22  ht
# XSV as package: components
#
# Revision 1.2  2002/06/10 14:38:53  ht
# fix uba
#
# Revision 1.1  2002/05/24 22:33:14  ht
# split out of XMLSchema
#
