#!/usr/bin/env python
#
# Copyright (c) 2008 vimov
#

try:
	# standard library imports
	import base64
	import locale
	import logging
	import os
	import sys
	import zlib
	import zipimport
	import platform as py_platform
	from optparse import OptionParser

	# make life easier
	sys.path.append("thedeployer/libs")

	# libs
	import paramiko
	from phpserializer import PhpSerializer

	# our own
	from thedeployer.packages.logger import *
	from thedeployer.packages.customexceptions import *
	from thedeployer.packages.depfile.parser import DepFileParser
	from thedeployer.packages.depfile.executor import DepFileExecutor
	from thedeployer.packages.depfile.factory import DepFileFactory
	from thedeployer.packages.application import Application

except Exception, e:

	print 'An exception was thrown: %s: %s' % (e.__class__, e)
	sys.exit(1)

# globals

__app_version__	= "1.0-alpha1"
__app_name__ = "The Deployer"

__app_parent_path__ = sys.path[0]
if True == os.path.isfile(__app_parent_path__):
	__app_parent_path__ = dirname(__app_parent_path__)

__default_config_file_path__ = os.path.join(__app_parent_path__, "thedeployer.conf")
__depfile_map_file_name__ = os.path.join(__app_parent_path__, "depfile/depfile.map")

def initialize(
	configuration_file_name,
	is_verbose
	):
	"""
	Perform applicantion instance-specific initializations, like initializing the locale and log files.
	"""

	global __depfile_map_file_name__

	# set the locale
	locale.setlocale(locale.LC_ALL, '')

	# load the configuration file
	Application.load_configuration_file(configuration_file_name)

	# get some values from the config file
	log_file_path = Application.get_option("logs", "log")
	backtrace_file_path = Application.get_option("logs", "backtrace")
	log_level = Application.get_option("logs", "level")

	try:
		log_level = int(log_level)
	except Exception:
		pass

	# log errors and such
	result = AppLogger.initialize(log_file_path, log_level, is_verbose)
	if 0 != len(result):
		exit_with_error(result)
	logging.setLoggerClass(AppLogger)

	# log the backtrace on error
	result = AppBacktrace.initialize(backtrace_file_path, is_verbose)
	if 0 != len(result):
		exit_with_error(result)

	# initialize the object Factory
	DepFileFactory.initialize(__depfile_map_file_name__)

# command line options
def get_options():
	"""
	Returns a list of two elements, the first is an instance of optparse.Values (the command line options, like -v),
	and the second is an array of the remaining command line arguments.

	Expected command line arguments:
		depFilePath: The path of the DepFile to process. Must be specified.
		execution_arguments: Zero or more key=value strings that are evaluated in processing as values for <argument> tags.
		options: Application command line options.

	Examples:
		./program_name site.dep -v title=helloworld
		./program_name site.dep title=hello email=me@you.com -g -v
		./program_name site.dep -v
	"""

	global __default_config_file_path__

	option_parser = OptionParser(usage = "Usage: %prog depFilePath [execution_arguments] [options]")

	option_parser.set_defaults(version = False, help = False)

	option_parser.add_option("-c", "", dest = "config", default = __default_config_file_path__,
		help = "Path to the configuration file.")
	option_parser.add_option("", "--version", dest = "version", action = "store_true", default = False,
		help = "Retrieve version information.")
	option_parser.add_option("-q", "--quiet", dest = "quiet", action = "store_true", default = False,
		help = "Supress status messages.")

	return option_parser

def get_depfile_path(cl_arguments):
	"""
	Returns the path of the DepFile from the command line arguments. It is expected to be the first parameter.

	@param cl_arguments: The array of arguments returned by option_parser.parse_args.

	@rtype: string
	@return: The path of the file on success, an empty string on failure.
	"""

	if list == type(cl_arguments) and 0 != len(cl_arguments):
		return cl_arguments[0]
	else:
		return ""

def get_execution_arguments(cl_arguments):
	"""
	Returns the execution arguments (the ones specified as key=value in the command line).

	@rtype: dict
	@return: A dictionary of zero or more key/value pairs of the command line arguments.
	"""

	arguments = cl_arguments[1:]
	execution_arguments = {}

	for argument in arguments:
		if argument.find("="):
			name, value = argument.split("=", 2)
			execution_arguments[name] = value

	return execution_arguments

def exit_with_error(message, code = 1):
	"""
	Exit the program with an error code.

	@param message: A message describing the error.
	@param code: The code to exit the program with.
	"""

	print "Error: " + message
	exit(code)

# main function
def main():

	# parse the command line arguments
	option_parser = get_options()
	(specified_options, arguments) = option_parser.parse_args(args = sys.argv[1:], values = None)

	# get the execution arguments, like a {"retry": 3} from a retry=3
	execution_arguments = get_execution_arguments(arguments)

	initialize(specified_options.config, not specified_options.quiet)

	if True == specified_options.version:

		print __app_name__, __app_version__
		sys.exit(0)

	else:

		# get the path of the DepFile
		dep_file_path = get_depfile_path(arguments)
		if 0 == len(dep_file_path):
			usage = option_parser.get_usage()
			print usage + "Try '%prog --help' for more information."
			exit(0)

		try:
			parser = DepFileParser(execution_arguments)
			project = parser.parse(dep_file_path)

			DepFileExecutor.execute(project)

		except Exception, e:
			raise#exit_with_error(str(e))

		sys.exit(0)

# run the main function
if __name__ == "__main__":

	try:
		main()
	except KeyboardInterrupt:
		exit_with_error("Execution interrupted.")
	except Exception, e:
		raise
