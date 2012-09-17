#!/usr/bin/env python

import glob
import os
import shutil
import sys

# attempt to install setuptools if it was not there.
try:

	from ez_setup import use_setuptools
	use_setuptools()

except KeyboardInterrupt:
	print "\nExecution interrupted.\n"
	sys.exit(1)
except Exception, e:
	print "\nError: An error occured while building. Failed with exception %s (%s)\n" % (e.__class__.__name__, str(e))
	sys.exit(1)

try:
	from setuptools import setup, find_packages

	if 'win32' == sys.platform:
		import py2exe
	elif 'darwin' == sys.platform:
		import py2app

except Exception, e:
	print "\nError: setuptools was not found."
	print "Download it from http://pypi.python.org/pypi/setuptools/.\n"
	sys.exit(1)

# make life easier
sys.path.append("thedeployer/libs")

class ApplicationConfig(object):

	#
	# build constants
	#

	SETUP_PLATFORM_WINDOWS_32BIT	= "win32"
	SETUP_PLATFORM_MACOSX		= "macosx"
	FREEZE_EXECUTABLE		= "freeze"

	#
	# general configuration parameters
	#

	NAME		= "thedeployer"
	VERSION		= "1.0"
	AUTHOR		= "vimov"
	AUTHOR_EMAIL	= "thedeployer@vimov.com"
	URL		= "www.vimov.com"
	DESCRIPTION	= "The Deployer"
	IDENTIFIER	= "com.vimov.thedeployer"
	LICENSE		= "X"
	KEYWORDS	= "X Y Z"
	DOWNLOAD_URL	= "http://code.vimov.com/files/thedeployer/thedeployer-%s.tar.gz" % (VERSION)
	LONG_DESCRIPTION= """
	The Deployer
	"""

	CLASSIFIERS	= [
		'Development Status :: 5 - Production/Stable',
		'Environment :: No Input/Output (Daemon)',
		'Environment :: Web Environment',
		'Environment :: Win32 (MS Windows)',
		'Intended Audience :: Customer Service',
		'Intended Audience :: Developers',
		'Intended Audience :: Education'
	],

	MAIN_APP_FILE 	= "thedeployer.py"
	INCLUDE_PATHS 	= ["thedeployer/libs/"]
	INCLUDE_MODULES = ["paramiko", "encodings.ascii"]

	ICON_WINDOWS	= "resources/icons/executable.ico"

	#
	# Release-specific
	#

	DEPENDENCIES	= [
				"paramiko>=1.7.2",
				"pycrypto>=2.0.1",
				"pysvn>=1.6.0",
				"pexpect>=2.3",
				"MySQL-python>=1.2.2",
	]

	NON_PYPI_DEPENDENCIES = [
				"http://pysvn.tigris.org/project_downloads.html"
	]

def rec_glob(pattern):
	
	result = []
	
	entries = glob.glob(pattern)
	for entry in entries:
		if not os.path.isdir(entry):
			result.append(entry)
		else:
			called_result = rec_glob(os.path.join(entry, "*"))
			for element in called_result:
				result.append(element)
				
	return result

def data_file_copy(ignored_parent, files, destination, verbose = False):
	
	if False == os.path.isdir(destination):
		os.makedirs(destination)
	
	for path in files:
		file_destination = path.replace(
			ignored_parent.rstrip(os.sep),
			destination.rstrip(os.sep),
			1
		)

		if False == os.path.isdir(os.path.dirname(file_destination)):
			os.makedirs(os.path.normpath(os.path.dirname(file_destination)))
			pass

		if True == verbose:
			print 'Adding file "%s"...' % (os.path.normpath(file_destination))
		shutil.copyfile(os.path.normpath(path), os.path.normpath(file_destination))

def copy_data(platform):

	example_files = rec_glob("examples/*")
	doc_files = rec_glob("docs")
	depfile_files = rec_glob("depfile")	

	data_file_copy("examples", example_files, "dist/examples", True)
	data_file_copy("docs", doc_files, "dist/docs", True)
	data_file_copy("depfile", depfile_files, "dist/depfile", True)

	if ApplicationConfig.SETUP_PLATFORM_WINDOWS_32BIT == platform:
		bin_files = rec_glob("thedeployer/bin/win32/*")
		data_file_copy("thedeployer/bin/win32", bin_files, "dist/bin", True)

def run_setup(platform = ""):
	"""
	"""

	if ApplicationConfig.SETUP_PLATFORM_WINDOWS_32BIT == platform:		

		setup(
			name = ApplicationConfig.NAME,
			version = ApplicationConfig.VERSION,

			description = ApplicationConfig.DESCRIPTION,
			long_description = ApplicationConfig.LONG_DESCRIPTION,
			author = ApplicationConfig.AUTHOR,
			author_email = ApplicationConfig.AUTHOR_EMAIL,
			url = ApplicationConfig.URL,
			download_url = ApplicationConfig.DOWNLOAD_URL,
			license = ApplicationConfig.LICENSE,
			keywords = ApplicationConfig.KEYWORDS,
			classifiers = ApplicationConfig.CLASSIFIERS,

			install_requires = ApplicationConfig.DEPENDENCIES,
			dependency_links = ApplicationConfig.NON_PYPI_DEPENDENCIES,

			include_package_data = False,
			#packages = ["xxx"],
			#package_dir = {"": "thedeployer"},
			packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

			options = {
				"py2exe": {
					"compressed": 1,
					"optimize": 2,
					"bundle_files": 1,
					"dll_excludes": ["w9xpopen.exe"],
					"includes": ApplicationConfig.INCLUDE_MODULES
				}
			},
			
			zipfile = None,
			console = [{
				"script": ApplicationConfig.MAIN_APP_FILE,
				"icon_resources": [(1, ApplicationConfig.ICON_WINDOWS)],
			}],
		)

		print find_packages()

	elif ApplicationConfig.SETUP_PLATFORM_MACOSX == platform:

		pass

	else:

		setup(
			name = ApplicationConfig.NAME,
			version = ApplicationConfig.VERSION,

			description = ApplicationConfig.DESCRIPTION,
			long_description = ApplicationConfig.LONG_DESCRIPTION,
			author = ApplicationConfig.AUTHOR,
			author_email = ApplicationConfig.AUTHOR_EMAIL,
			url = ApplicationConfig.URL,
			download_url = ApplicationConfig.DOWNLOAD_URL,
			license = ApplicationConfig.LICENSE,
			keywords = ApplicationConfig.KEYWORDS,
			classifiers = ApplicationConfig.CLASSIFIERS,

			install_requires = ApplicationConfig.DEPENDENCIES,
			dependency_links = ApplicationConfig.NON_PYPI_DEPENDENCIES,
		)
		
	if sys.argv[1] == "py2exe":
		copy_data(platform)
		shutil.copyfile("thedeployer.conf.win", "dist\\thedeployer.conf")

	return True

def main():
	"""
	"""

	if 'win32' == sys.platform:
		run_setup(ApplicationConfig.SETUP_PLATFORM_WINDOWS_32BIT)
	elif 'darwin' == sys.platform:
		run_setup(ApplicationConfig.SETUP_PLATFORM_MACOSX)
	else:
		run_setup()

#
# run the main function
#
if __name__ == "__main__":
	
	try:
		main()
		sys.exit(0)

	except KeyboardInterrupt:
		print "\nExecution interrupted.\n"
		sys.exit(1)
	except Exception, e:
		print "\nError: An error occured while building. Failed with exception %s (%s)\n" % (e.__class__.__name__, str(e))
		sys.exit(1)
