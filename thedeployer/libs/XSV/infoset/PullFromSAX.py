"""
PullFromSAX version 1.0

Copyright (C) 2006 Henry S. Thompson

This software is hereby licensed for use, modification and
redistribution.

Please acknowledge Henry S. Thompson in any onward distribution.

Henry S. Thompson makes no representations about the suitability of
this software and data for any purpose.  It is provided "as is" without
express or implied warranty.  Henry S. Thompson disclaims all
warranties with regard to this software, including all implied
warranties of merchantability and fitness.  In no event shall Henry
S. Thompson be liable for any special, indirect or consequential
damages or any damages whatsoever, action of contract, negligence or
other tortious action, arising out of or in connection with the use or
performance of this software.

Henry S. Thompson
Human Communication Research Centre,
Edinburgh University,
2 Buccleuch Place, Edinburgh EH8 9LW, SCOTLAND
Tel:(44) 131 650-4440
Fax:(44) 131 650-4587 email: ht@inf.ed.ac.uk
http://www.ltg.ed.ac.uk/~ht/

Turn SAX into a pull parser

Use ASyncPullFromSAX or SyncPullFromSAX

Create an instance giving a source and optionally a handler,
  features to set (as a Mapping),
  a parser classname list

Then use the getEvent() method to get events, None is EOF

Use the feature map to set features of the SAX parser, e.g.

 pfs = SyncPullFromSAX(xml.sax.saxutils.prepare_input_source("xyzzy.xml",
                               TupleEvent,
                               {xml.sax.handler.feature_namespaces:True})
 
 firstEvent = pfs.getEvent()

If you supply a handler, it must create 'events' and pass them back
 by calling self.deliver(event) -- this in turn will appear as the
 value of PullFromSax.getEvent().  In other words, you can completely control
 what events look like, if you don't like the builtins 

If you don't supply a handler, the SAX default handler will ignore all events,
 but if e.g. you just want to validate or check well-formedness that
 _might_ not be unreasonable. . .

Two builtin handlers are supplied for illustration/debugging:
 SummaryEvent, which produces strings and TupleEvent, which produces tuples
 whose first member is a package constant which identifies the type of event

You can subclass TupleEvent to turn off some events by e.g.
 def startPrefixMapping(self,p,n):
   return

Alternatively define your own subclass of xml.sax.handler.ContentHandler
Define handlers for any events you care about
Deliver them with self.deliver, e.g.
 def startElement(self,name,attrs):
   self.deliver(name)

 def startElementNS(self,name,qname,attrs):
   self.deliver((START,name,qname,attrs))
"""

version = 1.0

from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces
from xml.sax.saxutils import prepare_input_source

from threading import Thread, Event

START = 1
END = 2
DOCLOC = 3
STARTD = 4
ENDD = 5
STARTPM = 6
ENDPM = 7
CHARS = 8
WHITE = 9
PI = 10
SKIPPED = 11

class PullFromSAX:
  # Abstract, use SyncPullFromSAX or ASyncPullFromSAX
  def __init__(self,workerClass,handlerClass,features,parsers):
    if handlerClass is None:
      self.jointClass=type('pfsJoint',(workerClass,object),{})
    else:
      if not issubclass(handlerClass,ContentHandler):
        raise Exception, \
              "Must use subclass of ContentHandler, but %s isn't"%handlerClass
      self.jointClass=type('pfsJoint',(workerClass,handlerClass,object),{})
    if parsers is None:
      self.parser = make_parser()
    else:
      self.parser = make_parser(parsers)
    self.eventReady = Event()
    if features is not None:
      for f in features:
        self.parser.setFeature(f,features[f])

class SyncPullFromSAX(PullFromSAX):
  # Synchronous -- parser waits while user processes event
  def __init__(self,source,
               handlerClass=None,features=None,parsers=None):
    PullFromSAX.__init__(self,SyncWorker,handlerClass,features,parsers)
    self.eventProcessed = Event()
    self.worker=self.jointClass(self.parser,self.eventReady,
                                self.eventProcessed,source)
    self.worker.setDaemon(True)
    self.worker.start()

  def getEvent(self):
    self.eventProcessed.set()
    self.eventReady.wait()
    event = self.worker.event
    self.eventReady.clear()
    return event

class ASyncPullFromSAX(PullFromSAX):
  # Asynchronous -- parser will run while user is processing an event
  def __init__(self,source,handlerClass=None,features=None,parsers=None):
    PullFromSAX.__init__(self,ASyncWorker,handlerClass,features,parsers)
    self.eventTaken = Event()
    self.worker=self.jointClass(self.parser,self.eventReady,
                                self.eventTaken,source)
    self.worker.setDaemon(True)
    self.eventTaken.set()
    self.worker.start()

  def getEvent(self):
    self.eventReady.wait()
    event = self.worker.event
    self.eventReady.clear()
    self.eventTaken.set()
    return event

class Worker(Thread,ContentHandler):
  # Abstract, we always use SyncWorker or ASyncWorker
  def __init__(self,parser,ready,source):
    self.parser = parser
    self.ready = ready
    self.source = source
    Thread.__init__(self)

class SyncWorker(Worker):
  def __init__(self,parser,ready,processed,source):
    Worker.__init__(self,parser,ready,source)
    self.processed = processed

  def run(self):
    self.parser.setContentHandler(self)
    self.processed.wait()
    self.processed.clear()
    self.parser.parse(self.source)
    self.event=None
    self.ready.set()
    # return, never to be seen again

  def deliver(self,event):
    self.event = event
    self.ready.set()
    self.processed.wait()
    self.processed.clear()

class ASyncWorker(Worker):
  def __init__(self,parser,ready,taken,source):
    Worker.__init__(self,parser,ready,source)
    self.taken = taken

  def run(self):
    self.parser.setContentHandler(self)
    self.parser.parse(self.source)
    self.deliver(None)
    # return, never to be seen again

  def deliver(self,event):
    self.taken.wait()
    self.event = event
    self.taken.clear()
    self.ready.set()

class TupleEvent(ContentHandler):
  def setDocumentLocator(self, locator):
    self.deliver((DOCLOC, locator))

  def startDocument(self):
    self.deliver((STARTD,))

  def endDocument(self):
    self.deliver((ENDD,))

  def startPrefixMapping(self, prefix, uri):
    self.deliver((STARTPM, prefix, uri))

  def endPrefixMapping(self, prefix):
    self.deliver((ENDPM, prefix))

  def startElement(self, name, attrs):
    self.deliver((START, name, attrs))

  def endElement(self, name):
    self.deliver((END, name))

  def startElementNS(self, name, qname, attrs):
    self.deliver((START, name, qname, attrs))

  def endElementNS(self, name, qname):
    self.deliver((END, name, qname))

  def characters(self, content):
    self.deliver((CHARS, content))

  def ignorableWhitespace(self, whitespace):
    self.deliver((WHITE, whitespace))

  def processingInstruction(self, target, data):
    self.deliver((PI, target, data))

  def skippedEntity(self, name):
    self.deliver((SKIPPED, name-last-kbd-macro))

class SummaryEvent(ContentHandler):
  def setDocumentLocator(self, locator):
    self.deliver("dl")

  def startDocument(self):
    self.deliver("<<")

  def endDocument(self):
    self.deliver(">>")

  def startPrefixMapping(self, prefix, uri):
    self.deliver("%s->%s"%(prefix, uri))

  def endPrefixMapping(self, prefix):
    self.deliver("%s->"%prefix)

  def startElement(self, name, attrs):
    self.deliver("< %s"%name)

  def endElement(self, name):
    self.deliver("> %s"%name)

  def startElementNS(self, name, qname, attrs):
    self.deliver("< %s"%qname)

  def endElementNS(self, name, qname):
    if qname is None:
      self.deliver("> %s"%name[1])
    else:
      self.deliver("> %s"%qname)

  def characters(self, content):
    if len(content)>3:
      self.deliver("- %s ..."%oneLine(content[0:3]))
    else:
      self.deliver("- %s"%oneLine(content))

  def ignorableWhitespace(self, whitespace):
    self.deliver("S")

  def processingInstruction(self, target, data):
    self.deliver("<?%s ..."%target)

  def skippedEntity(self, name):
    self.deliver("&%s"%name)

def oneLine(str):
  if '\n' in str or '\r' in str:
    return str.replace('\n','\\n').replace('\r','\\r')
  else:
    return str

if __name__ == '__main__':
  import sys
  fn = sys.argv.pop()
  pfs = SyncPullFromSAX
  evc = None
  ns = False
  while len(sys.argv)>1:
    flag = sys.argv.pop()
    if flag=='-a':
      pfs=ASyncPullFromSAX
    elif flag=='-s':
      evc = SummaryEvent
    elif flag=='-e':
      evc=TupleEvent
    elif flag=='-n':
      ns=True
    else:
      raise Exception, "Usage: python PullFromSAX.py [-a] [-n] [-e|-s] URI"
  p = pfs(prepare_input_source(fn),evc,
          {feature_namespaces:ns})
  while True:
    e = p.getEvent()
    print e
    if e is None:
      break
  
