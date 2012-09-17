"""Drive XSV from command line"""

__version__="$Revision: 1.16 $ of $Date: 2007-03-28 14:23:45 $"
# $Id: commandLine.py,v 1.16 2007-03-28 14:23:45 ht Exp $

import sys

_usageString="Usage: [-ktwilDNend] [-u baseURI] [-T type] [-E elt] [-r [-r [-r]] [ind|alt]] [-s stylesheet] [-o outputFile] [-p profileOut] file [schema1 schema2 . . .]\n"

debug = 0

class SchemaValidationError(Exception):
  def __init__(self,arg):
    Exception.__init__(self,arg)

def parseAndRun(argl):
  global runitAndShow, debug
  k=0
  dw=1
  timing=0
  style=None
  outfile=None
  reflect=0
  reflect2=0
  independent=0
  proFile=None
  scanForLocs=0
  useDTD=0
  topType=None
  topElt=None
  derefNSNs=1
  control=2
  baseURI=None
  preserveRedirect=0
  serialise=0
  while argl:
    if argl[0]=='-k':
      k=1
    elif argl[0]=='-s':
      style=argl[1]
      argl=argl[1:]
    elif argl[0]=='-u':
      baseURI=argl[1]
      argl=argl[1:]
    elif argl[0]=='-o':
      outfile=argl[1]
      argl=argl[1:]
    elif argl[0]=='-p':
      proFile=argl[1]
      argl=argl[1:]
    elif argl[0]=='-T':
      topType=argl[1]
      argl=argl[1:]
    elif argl[0]=='-E':
      topElt=argl[1]
      argl=argl[1:]
    elif argl[0]=='-w':
      dw=0
    elif argl[0]=='-l':
      scanForLocs=1
    elif argl[0]=='-n':
      serialise=1
    elif argl[0]=='-D':
      useDTD=1
    elif argl[0]=='-d':
      debug=1
    elif argl[0]=='-N':
      derefNSNs=0
    elif argl[0]=='-t':
      timing=1
    elif argl[0]=='-r':
      while (len(argl)>1 and argl[1]=='-r'):
        argl=argl[1:]
        control=control-1
      if len(argl)>1:
        if argl[1]=='alt':
          reflect=2
          argl=argl[2:]
          continue
        elif argl[1]=='ind':
          reflect=1
          argl=argl[2:]
          continue
      reflect=1
    elif argl[0]=='-R':
      reflect2=1
    elif argl[0]=='-i':
      independent=1
    elif argl[0]=='-e':
      preserveRedirect=1
    elif argl[0][0]=='-':
      sys.stderr.write(_usageString)
      sys.exit(-1)
    else:
      break
    argl=argl[1:]

  if debug:
    from XSV import useLTXML
    sys.stderr.write("Using PyLTXML: %s\n"%useLTXML())
  import XSV.driver
  runitAndShow=XSV.driver.runitAndShow
  if argl:
    if proFile:
      import profile
      profile.Profile.bias = 5.0e-6
      res=profile.run("""runitAndShow(%s,%s,%s,
                         %s,%s,%s,%s,%s,%s,%s,
                         %s,%s,%s,%s,%s,
                         %s,%s,%s,%s)"""%(repr(argl[0]),repr(argl[1:]),k,
                         style,None,outfile,dw,timing,reflect,independent,
                         reflect2,scanForLocs,useDTD,topType,topElt,
                         derefNSNs,control,baseURI,preserveRedirect,serialise),
                      proFile)
    else:
      res=runitAndShow(argl[0],argl[1:],
                       k,style,None,outfile,dw,timing,reflect,
                       independent,reflect2,scanForLocs,useDTD,topType,
                       topElt,derefNSNs,control,baseURI,preserveRedirect,serialise)
  else:
    res=runitAndShow(None,[],k,
                     style,None,outfile,dw,timing,reflect,independent,
                     reflect2,scanForLocs,useDTD,topType,topElt,derefNSNs,
                     control,baseURI,preserveRedirect,serialise)

  if res is not None:
    raise SchemaValidationError,res

if __name__=='__main__':
#  if sys.argv[1]=="-debug":
#    parseAndRun(sys.argv[2:])
  try:
    parseAndRun(sys.argv[1:])
  except SchemaValidationError, ex:
    if debug:
      sys.stderr.write(ex.args[0])
    sys.exit(1)
  sys.exit(0)

# $Log: commandLine.py,v $
# Revision 1.16  2007-03-28 14:23:45  ht
# show input mech. if debugging
#
# Revision 1.15  2005/04/14 14:41:44  ht
# update usage string
#
# Revision 1.14  2005/03/16 09:22:20  ht
# move SchemaValidationError
#
# Revision 1.13  2005/03/14 09:25:52  ht
# debug (-d) flag
#
# Revision 1.12  2004/10/07 09:29:27  ht
# make sure stderr is clean from command line
#
# Revision 1.11  2004/09/28 11:35:11  ht
# update usage string
#
# Revision 1.10  2004/08/31 15:11:18  ht
# add serialisation support,
# including use of SNV
#
# Revision 1.9  2004/06/30 10:45:27  ht
# get profile working again
#
# Revision 1.8  2004/04/01 12:52:39  ht
# add -e flag for preserving captured stderr
#
# Revision 1.7  2003/09/01 15:32:33  ht
# add baseURI command line arg
#
# Revision 1.6  2003/03/30 20:05:46  ht
# give command-line control over amount of schema material reflected
#
# Revision 1.5  2003/02/14 09:36:25  ht
# add -N switch to supress derefing namespace names
#
# Revision 1.4  2002/10/09 09:47:11  ht
# change 'rel' to 'alt' (which is what it is, after all)
#
# Revision 1.3  2002/10/08 21:10:05  ht
# minor
#
# Revision 1.2  2002/09/01 19:23:23  ht
# allow for command line spec. of type or elt
#
# Revision 1.1  2002/06/28 09:39:17  ht
# XSV as package: top level
#
