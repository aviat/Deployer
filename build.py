#!/usr/bin/env python

# python standard library imports
import shutil
import sys
import os

# platform-specific includes
try:
	if 'win32' == sys.platform:
		from setuptools import setup
		import py2exe
	elif 'darwin' == sys.platform:
		from setuptools import setup
		import py2app

except Exception, e:
	print "Error: setuptools was not found. Download it from http://pypi.python.org/pypi/setuptools/"
	exit(1)

# make life easier
sys.path.append("thedeployer/libs")

#
# build constants
#

BUILD_PLATFORM_LINUX		= "linux"
BUILD_PLATFORM_WINDOWS_32BIT	= "win32"
BUILD_PLATFORM_MACOSX		= "macosx"

BUILD_CREATE_PERMISSIONS	= 0777
BUILD_ROOT_DIR 			= "build/dist"

#
# general configuration parameters
#

APPLICATION_NAME		= "The Deployer"
APPLICATION_VERSION		= "1.0"
APPLICATION_AUTHOR		= "vimov"
APPLICATION_AUTHOR_EMAIL	= "thedeployer@vimov.com"
APPLICATION_URL			= "www.vimov.com"
APPLICATION_DESCRIPTION		= "The Deployer"
APPLICATION_IDENTIFIER		= "com.vimov.thedeployer"

MAIN_APP_FILE 			= "thedeployer.py"
INCLUDE_PATHS 			= ["thedeployer/libs/"]
INCLUDE_MODULES 		= ["paramiko", "encodings.ascii"]

#
# icon
#

APPLICATION_ICON_WINDOWS	= "build/resources/icons/executable.ico"

#
# Linux-specific constants
#

FREEZE_EXECUTABLE		= "freeze"

#
# exit_with_error
#

IS_PROCESSING_MESSAGE_RUNNING = 0
def exit_with_error(message):

	global IS_PROCESSING_MESSAGE_RUNNING

	if 1 == IS_PROCESSING_MESSAGE_RUNNING:
		print_processing_status(0)

	print
	print "Error: " + message

	sys.exit(1)

#
# print_processing_message
#

def print_processing_message(message):

	global IS_PROCESSING_MESSAGE_RUNNING

	print message + "...",

	IS_PROCESSING_MESSAGE_RUNNING = 1

#
# print_processing_status
#

def print_processing_status(statusCode):

	global IS_PROCESSING_MESSAGE_RUNNING

	if 0 == statusCode:
		print "failed."
	else:
		print "done."

	IS_PROCESSING_MESSAGE_RUNNING = 0

#
# remdir
#

def rmdir_recursive(path):

	if not os.path.isdir(path):
		return
	
	files = os.listdir(path)

	for file in files:

		fullPath = os.path.join(path, file)

		if os.path.isfile(fullPath):
			
			os.remove(fullPath)
			
		elif os.path.isdir(fullPath):
			
			rmdir_recursive(fullPath)
			os.rmdir(fullPath)

#
# compile
#

def compile(platform):

	global BUILD_PLATFORM_LINUX, BUILD_PLATFORM_WINDOWS_32BIT, BUILD_PLATFORM_MACOSX, BUILD_CREATE_PERMISSIONS, BUILD_ROOT_DIR
	global APPLICATION_NAME, APPLICATION_VERSION, APPLICATION_DESCRIPTION, APPLICATION_AUTHOR, APPLICATION_AUTHOR_EMAIL, APPLICATION_URL
	global MAIN_APP_FILE
	global INCLUDE_PATHS, INCLUDE_MODULES
	global FREEZE_EXECUTABLE

	# concatenate the build directory
	buildDirectory = os.path.normpath(os.path.join(BUILD_ROOT_DIR, platform))

	# create the build directory or clear it if it was already there

	print_processing_message("Checking build directory \"" + buildDirectory + "\"")

	if False == os.path.isdir(buildDirectory):
		
		try:
			os.makedirs(buildDirectory)
		except Exception, e:
			exit_with_error("Cannot create directory \"" + buildDirectory + "\"")

	else:

		print_processing_status(1)
		print_processing_message("Clearing build directory \"" + buildDirectory + "\"")

		try:
			rmdir_recursive(buildDirectory)
		except Exception, e:
			exit_with_error("Cannot delete the contents of directory \"" + buildDirectory + "\"")

	print_processing_status(1)

	if BUILD_PLATFORM_LINUX == platform:

		includePathArguments = ""
		for path in INCLUDE_PATHS:
			path = os.path.normpath(path)
			includePathArguments = includePathArguments + " --include-path=" + path + " "

		includeModuleArguments = "--include-modules="
		for module in INCLUDE_MODULES:
			includeModuleArguments = includeModuleArguments + module + ","
		includeModuleArguments = includeModuleArguments.rstrip(",")

		command = FREEZE_EXECUTABLE + " " + MAIN_APP_FILE + " " + "--target-dir=" + buildDirectory + " " + includePathArguments + " " + includeModuleArguments

		os.system(command)

	elif BUILD_PLATFORM_WINDOWS_32BIT == platform:

		sys.argv.insert(1, "py2exe")

		setup(
			name = APPLICATION_NAME,
			version = APPLICATION_VERSION,
			description = APPLICATION_DESCRIPTION,
			author = APPLICATION_AUTHOR,
			author_email = APPLICATION_AUTHOR_EMAIL,
			url = APPLICATION_URL,
			options = {
				"py2exe": {
					"compressed": 1,
					"optimize": 2,
					"bundle_files": 1,
					"dll_excludes": ["w9xpopen.exe", "MSVCR71.dll"],
					"includes": INCLUDE_MODULES
				}
			},
			zipfile = None,
			console = [{
				"script": MAIN_APP_FILE,
				"icon_resources": [(1, APPLICATION_ICON_WINDOWS)],
			}],
		)

		shutil.move(os.path.join("dist", MAIN_APP_FILE[0:-2] + "exe"), buildDirectory)
		shutil.rmtree("dist")
		shutil.rmtree("build\bdist.win32", True)

	elif BUILD_PLATFORM_MACOSX == platform:

		sys.argv.insert(0, "py2app")

		currentDirectory = os.getcwd()
		os.chdir(buildDirectory)

		setup(
			app = MAIN_APP_FILE,
			name = APPLICATION_NAME,
			version = APPLICATION_VERSION,
			description = APPLICATION_DESCRIPTION,
			author = APPLICATION_AUTHOR,
			author_email = APPLICATION_AUTHOR_EMAIL,
			url = APPLICATION_URL,
			options = dict(py2app = dict(
				plist=dict(
					LSPrefersPPC = True,
					CFBundleGetInfoString = APPLICATION_NAME,
					CFBundleIdentifier = APPLICATION_IDENTIFIER

				),
				argv_emulation = True
			)),
			setup_requires = ['py2app'],
		)

		os.chdir(currentDirectory)

	else:
		exit_with_error("No build rules are available for the platform \"" + platform + "\"")
#
# main
#

def main():

	if 'win32' == sys.platform:
		compile(BUILD_PLATFORM_WINDOWS_32BIT)
	elif 'darwin' == sys.platform:
		compile(BUILD_PLATFORM_MACOSX)
	else:
		exit_with_error("No build targets for this platform.")

#
# run the main function
#

if __name__ == "__main__":
	
	try:
		main()
		
	except Exception, e:

		print
		print "Error: An error occured while building. Failed with exception %s (%s)" % (e.__class__.__name__, str(e))
		print
