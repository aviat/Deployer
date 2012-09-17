#
# Copyright (c) 2008 vimov
#

import sys
import re
import platform as py_platform

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.validator import Validator

class Platform(object):

	"""
	Represents a server's platform (operating system).
	"""

	PLATFORM_POSIX = "posix"
	PLATFORM_WINDOWS = "windows"
	PLATFORM_OTHER = "other"

	OS_LINUX = "linux"
	OS_WINDOWS_9X = "9x"
	OS_WINDOWS_NT = "nt"
	OS_MAC_CLASSIC = "mac"
	OS_MAC_OSX = "osx"

	"""@__platform: The identifier for the platform."""
	"""@__os_class: The identifier of the operating system's class"""
	"""@__os_release: A string describing the release version of an operating system."""
	"""@__bits: The number of bits of this platform, can be 32 or 64."""

	def __init__(self, platform, os_class, os_release = "", bits = 32):
		"""
		Constructor for the class.

		@param platform: Can be Platform.PLATFORM_POSIX or Platform.PLATFORM_WINDOWS or PLATFORM_OTHER.
		@param os_class: The identifier of the operating system's class, like OS_WINDOWS_9X.
		@param os_release: A string describing the release version of an operating system.
		@param bits: The number of bits of the platform, like 32 or 64.

		@raise InvalidParameterError: If an unsupported platform or bit-length was specified.
		"""

		if Platform.PLATFORM_POSIX != platform and Platform.PLATFORM_WINDOWS != platform and Platform.PLATFORM_OTHER != platform:
			raise InvalidParameterError("platform", "Must be PLATFORM_POSIX, PLATFORM_WINDOWS or PLATFORM_OTHER.")

		if Platform.OS_LINUX != os_class and Platform.OS_WINDOWS_9X != os_class and Platform.OS_WINDOWS_NT != os_class and Platform.OS_MAC_CLASSIC != os_class and Platform.OS_MAC_OSX != os_class:
			raise InvalidParameterError("platform", "Must be OS_LINUX, OS_WINDOWS_9X, OS_WINDOWS_NT, OS_MAC_CLASSIC or OS_MAC_OSX.")

		if 32 != bits and 64 != bits:
			raise InvalidParameterError("bits", "Supported platforms are 32 and 64-bits.")

		self.__platform = platform
		self.__os_class = os_class
		self.__os_release = os_release
		self.__bits = bits

	@classmethod
	def get_current(cls):
		"""
		Returns an instance of the current platform running the program.

		@rtype: Platform
		@return: An instance of Platform

		@raise PlatformNotSupportedError: If the current platform is not supported.
		"""

		uname_array = py_platform.uname()

		if "linux" == uname_array[0].lower() or "darwin" == uname_array[0].lower():
			platform = Platform.PLATFORM_POSIX
		elif 'windows' == uname_array[0].lower():
			platform = Platform.PLATFORM_WINDOWS
		else:
			raise PlatformNotSupportedError()

		if "linux" == uname_array[0].lower():

			os_class = Platform.OS_LINUX
			os_release = uname_array[2]
		
		elif "darwin" == uname_array[0].lower():

			mac_version = py_platform.mac_ver()[0]

			if "10" == mac_version.split(".")[0]:
				os_class = Platform.OS_MAC_OSX
			else:
				os_class = Platform.OS_MAC_CLASSIC

			os_release = mac_version

		elif "windows" == uname_array[0].lower():

			os_release = uname_array[2].lower()

			if "2000" == os_release or "xp" == os_release or "vista" == os_release:
				os_class = Platform.OS_WINDOWS_NT
			else:
				os_class = Platform.OS_WINDOWS_9X

			os_release = uname_array[2]

		else:
			raise PlatformNotSupportedError()

		return Platform(platform, os_class, os_release, 32)

	@classmethod
	def get_instance(cls, os_class):
		"""
		Returns an instance of Platform based on the specified operating system class.
		"""

		if Platform.OS_LINUX == os_class or Platform.OS_MAC_OSX == os_class:
			return Platform(Platform.PLATFORM_POSIX, os_class, "", 32)
		elif Platform.OS_WINDOWS_9X == os_class or Platform.OS_WINDOWS_NT == os_class or Platform.OS_MAC_CLASSIC == os_class:
			return Platform(Platform.PLATFORM_WINDOWS, os_class, "", 32)
		else:
			raise PlatformNotSupportedError(os_class)

	def get_root(self):
		"""
		Returns the root of the current platform.
		For Windows, this is always "C:\", for Linux and Mac OSX, this is always "/".

		@rtype: String
		@return: The root path.
		"""

		if Platform.PLATFORM_WINDOWS == self.__platform:
			return "C:\\"
		else:
			return "/"

	def get_platform(self):
		"""
		Returns Platform.PLATFORM_POSIX or Platform.PLATFORM_WINDOWS.
		"""
		return self.__platform

	def get_os_class(self):
		"""
		Returns OS_LINUX, OS_WINDOWS_9X, OS_WINDOWS_NT, OS_MAC_CLASSIC or OS_MAC_OSX.
		"""
		return self.__os_class

	def get_bits(self):
		"""
		Returns th number of bits of the platform, like "32" if it was a 32-bit platform.
		"""
		return self.__bits

	def join(self, arg0, arg1):
		'''
		join two strings into one path
		
		@param arg0: parent of the path
		@param arg1: base of the path
		
		@return: the full path
		
		@raise InvalidParameterError: If the required argument(s) are not specified. 
		'''
		
		if arg0 is None or "" == arg0:
			raise InvalidParameterError("arg0", "arg0 can not be None or empty string")

		if arg1 is None or "" == arg1:
			raise InvalidParameterError("arg1", "arg1 can not be None or empty string")

		return arg0.rstrip(self.get_separator()) + self.get_separator() + arg1

	def dirname(self, path):
		'''
		get the directrory name of path
		i.e. dirname of /a/b/c is /a/b
		
		@param paht: path that you want to get dirname of it
		@type path: String
		
		@rtype: String
		@return: the dirname of the path
		
		@raise InvalidParameterError: If the required argument(s) are not specified.
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "Cannot be an empty string")
		
		path = self.trim_path(path)
		
		if path[len(path)-1] == self.get_separator():
			return path
		
		index = path.rfind(self.get_separator())
		name = path[0:index]
		
		return name
	
	def basename(self, path):
		"""
		get the base name of path
		i.e. basename of /a/b/c is c
		i.e. basename of /a/b/c/ is ""
		
		@param paht: path that you want to get the base parent of.
		
		@rtype: string
		@return: the directory parent of the path.
		
		@raise InvalidParameterError: If the path is empty.
		"""
		
		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "Cannot be an empty string")
		
		path = self.trim_path(path)
		
		if path[len(path)-1] == self.get_separator():
			return ""
		
		index = path.rfind(self.get_separator())
		name = path[index+1:]
		
		return name

	def trim_path(self, path):
		"""
		Trims the trailing slashe (forward or backward) from a path.

		@param path: The path to trim.

		@return: Trimmed path.
		"""
		
		re.match(r'[a-zA-Z]:\\', path)
		if re.match(r'/$', path) == None and re.match(r'[a-zA-Z]:\\', path) == None:
			path = path.rstrip(self.get_separator())
		
		return path
	
	def get_separator(self):
		if Platform.PLATFORM_WINDOWS == self.__platform:
			return "\\"
		else:
			return "/"
	
	def is_relative(self, path):

		if self.get_platform() == Platform.PLATFORM_WINDOWS:
			if re.match(r'[a-zA-Z]:\\', path[0:3]):
				return False
		elif path[0] == '/':
				return False

		return True
	
	def get_temp_dir(self):
		if Platform.PLATFORM_WINDOWS == self.__platform:
			return "c:\\WINDOWS\\Temp"
		else:
			return "/tmp"
