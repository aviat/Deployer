"""W3C XML Schema compilation and validity assessment"""

__version__="$Revision: 1.22 $ of $Date: 2007-12-11 16:20:05 $"

__all__=['driver',
         'commandLine',
         'util',
         'compile',
         'infoset',
         'validate']

major_version=3
minor_version=1
release=1

xsvNS="http://www.w3.org/2000/05/xsv"

useLT = True     # set to False to never use PyLTXML even if installed

if useLT:
  try:
    import PyLTXML
  except ImportError:
    useLT = False

def useLTXML():
  return useLT
