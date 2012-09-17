#!/usr/bin/env python
#
# Copyright (c) 2008 vimov

try:
	# python standard library imports
	import sys, locale, base64
	import zlib, zipimport
	import unittest
	from optparse import OptionParser

	# make life easier
	sys.path.append("../../libs")
	sys.path.append("../../packages")

except Exception, e:

	print 'An exception was thrown: %s: %s' % (e.__class__, e)
	sys.exit(1)

# initialize
def initialize():

	locale.setlocale(locale.LC_ALL, '')

# run tests
def run_tests():

	print "ran tests!"

# command line options
def get_options():

	optionParser = OptionParser(usage = "Usage: %prog [options]")

	#optionParser.set_defaults(gui=False)
	#optionParser.add_option("-g", "--gui", dest="gui", action="store_true", default=False, help="Start in GUI mode")

	return optionParser

# main function
def main():

	optionParser = get_options()
	(specifiedOptions, args) = optionParser.parse_args(args = sys.argv[1:], values = None)
	
	#if True == specifiedOptions.version:

		#print __app_name__, __app_version__
		#sys.exit(0)

	#if True == specifiedOptions.gui:

		#result = ssh_test()
		#open_window(result)
		#sys.exit(0)

	#else:

	run_tests()
	sys.exit()

# run the main function
if __name__ == "__main__":
	
	try:
		initialize()
		main()

	except Exception:
		
		raise
