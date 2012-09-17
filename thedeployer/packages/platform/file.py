#
# Copyright (c) 2008 vimov
#

import time
from datetime import datetime
import re
import os

from thedeployer.packages.customexceptions import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.depfile.validator import Validator

def octstr_to_int(octal_string):
	if len(octal_string) == 0 or not octal_string.isdigit() or octal_string[0] != '0':
		raise InvalidParameterError
	value = 0
	for item in octal_string:
		temp = int(item)
		value = (value << 3) + temp
	return value

class FileObject(object):

	"""
	A representation of a file.
	This object does not directly access the file, and has to be passed all the information about the file.
	It is intended to be used by other classes that would creates instances of this object.
	"""

	FILE = 1001
	DIRECTORY = 1002
	LINK = 1003
	SOCKET = 1004
	CHARCTER_DEVICE = 1005
	BLOCK_DEVICE = 1006
	PIPE = 1007
	DOOR = 1008
	
	
	S_IREAD = 256
	S_IWRITE = 128
	
	
	S_IRUSR = 256
	S_IWUSR = 128
	S_IXUSR = 64
	S_IRGRP = 32 
	S_IWGRP = 16
	S_IXGRP = 8 
	S_IROTH = 4
	S_IWOTH = 2 
	S_IXOTH = 1
	
	PERMISSIONS_AS_OCT = 1000
	PERMISSIONS_AS_INT = 1001
	
	"""@__permissions: QWERTY"""

	def __init__(self, platform, path, file_type, permissions, modifiation_date, creation_date = "", access_date = "", user = "", group = ""):

		if Platform != platform.__class__:
			raise InvalidParameterError("platform", "Must be an instance of Platform.")
		elif "" == path:
			raise InvalidParameterError("path", "Must be a non-empty string.")
		elif not Validator.validate_integer(file_type):
			raise InvalidParameterError("type", "Must be FileObject.FILE, Fie.DIRECTORY or FileObject.LINK.")
		elif "" == modifiation_date:
			raise InvalidParameterError("modifiation_date", "Must be non empty string.")
		elif Platform.PLATFORM_POSIX == platform.get_platform():
			if "" == user:
				raise InvalidParameterError("user", "Must be non empty.")
			elif "" == group:
				raise InvalidParameterError("group", "Must be non empty.")
	
		self.__platform = platform
		self.__path = path
		self.__type = file_type
		
		self.__permissions = None
		self.__modification_date = None
		self.__creation_date = None
		self.__access_date = None
		
		
		self.set_permissions(permissions)
		self.set_modification_date(modifiation_date)

		if "" != creation_date:
			self.set_creation_date(creation_date)

		if "" != access_date:
			self.set_access_date(access_date)

		self.__user = user
		self.__group = group
		self.__childs = []

	def set_permissions(self, permissions):
		"""
		Sets the permisions of the file based on the passed.
		This function behaves differently based on whether the platform is Windows or (Linux or Mac OS X).
		For Windows, the permissions variable will be set to either S_IREAD or S_IWRITE. For the Linux and
		Mac OSX, ORs the required constants from S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH,
		S_IWOTH, and S_IXOTH.
		
		@param permissions: For Linux and Mac oSX: can be a decimal representation (755), an octal
			representation (0755), or string representation (rwxr-xr-x). For Windows, must be a string
			represetation: "r-" for read-only and "rw" otherwise.

		@raise PermissionsInvalid: If the specified permissions are invalid.
		"""

		if Platform.PLATFORM_POSIX == self.__platform.get_platform():
			if permissions.__class__ == str and re.match('([-r][-w][-xsStT]){3,3}', permissions):
				self.__permissions = 0
				if permissions[0] != '-':
					self.__permissions |= FileObject.S_IRUSR
				if permissions[1] != '-':
					self.__permissions |= FileObject.S_IWUSR
				if permissions[2] != '-':
					self.__permissions |= FileObject.S_IXUSR
				if permissions[3] != '-':
					self.__permissions |= FileObject.S_IRGRP
				if permissions[4] != '-':
					self.__permissions |= FileObject.S_IWGRP
				if permissions[5] != '-':
					self.__permissions |= FileObject.S_IXGRP
				if permissions[6] != '-':
					self.__permissions |= FileObject.S_IROTH
				if permissions[7] != '-':
					self.__permissions |= FileObject.S_IWOTH
				if permissions[8] != '-':
					self.__permissions |= FileObject.S_IXOTH
					
			elif permissions.__class__ == str and re.match('(0)?[0-7]{3,3}', permissions):
				if len(permissions) == 3:
					permissions = '0' + permissions
				self.__permissions = octstr_to_int(permissions)
			
			elif permissions.__class__ == int and 0 <= permissions <= 511:
				self.__permissions = permissions
			
			else:
				raise PermissionsInvalidError()

		elif Platform.PLATFORM_WINDOWS == self.__platform.get_platform():
			if permissions.__class__ == str and re.match('[-r][-w]', permissions):
				self.__permissions = 0
				if permissions[0] != '-':
					self.__permissions |= FileObject.S_IREAD
				if permissions[1] != '-':
					self.__permissions |= FileObject.S_IWRITE
			elif permissions.__class__ == int and 0 <= permissions <= 511:
				self.__permissions = permissions
			else:
				raise PermissionsInvalidError() 
		else:
			raise PlatformNotSupportedError()
	
	
	
	def set_modification_date(self, modification_date):
		"""
		sets the modification date of the file
		
		@param modification_date: is the modification date of the file and should be in format 'ss mm hh DD MM YYYY' or tuple of time
		
		@raise InvalidParameterError: if modification_date is empty of not a string 
		@raise InvalidDate: if date is not in valid format
		"""
		
		if (modification_date.__class__ != str or modification_date =="") and (modification_date.__class__ != time.struct_time or len(modification_date) != 9 ):
			raise InvalidParameterError("modification_date", "modification_date is not in a proper format")
		try:
			if modification_date.__class__ == str:
				tmp_md = time.strptime(modification_date, '%S %M %H %d %m %Y')
			elif modification_date.__class__ == time.struct_time:
				tmp_md = modification_date
			self.__modification_date = datetime(tmp_md[0], tmp_md[1], tmp_md[2], tmp_md[3], tmp_md[4], tmp_md[5])	
		except:
			raise InvalidDate, "date is not valid modification_date is not in a proper format"

	def set_creation_date(self, creation_date):
		"""
		sets the creation date of the file
		
		@param creation_date: is the creation date of the file and should be in format 'ss mm hh DD MM YYYY' or a tuple of time
		
		@raise InvalidParameterError: if creation_date is empty of not a string 
		@raise InvalidDate: if date is not in valid format
		"""
		
		if (creation_date.__class__ != str or creation_date =="") and (creation_date.__class__ != time.struct_time or len(creation_date) != 9 ):
			raise InvalidParameterError("creation_date", "creation_date is not in a proper format")
		try:
			if creation_date.__class__ == str:
				tmp_cd = time.strptime(creation_date, '%S %M %H %d %m %Y')
			elif creation_date.__class__ == time.struct_time:
				tmp_cd = creation_date
			self.__creation_date = datetime(tmp_cd[0], tmp_cd[1], tmp_cd[2], tmp_cd[3], tmp_cd[4], tmp_cd[5])
		except:
			raise InvalidDate, "date is not valid creation_date is not in a proper format"

	def set_access_date(self, access_date):
		"""
		sets the access date of the file
		
		@param access_date: is the access date of the file and should be in format 'ss mm hh DD MM YYYY' or a tuple of time
		
		@raise InvalidParameterError: if access_date is empty of not a string 
		@raise InvalidDate: if date is not in valid format
		"""
		
		if (access_date.__class__ != str or access_date =="") and (access_date.__class__ != time.struct_time or len(access_date) != 9 ):
			raise InvalidParameterError("access_date", "access_date is not in a proper format")
		try:
			if access_date.__class__ == str:
				tmp_ad = time.strptime(access_date, '%S %M %H %d %m %Y')
			elif access_date.__class__ == time.struct_time:
				tmp_ad = access_date
			self.__access_date = datetime(tmp_ad[0], tmp_ad[1], tmp_ad[2], tmp_ad[3], tmp_ad[4], tmp_ad[5])
		except:
			raise InvalidDate, "date is not valid access_date is not in a proper format"
	
	
	
	def get_modification_date(self):
		'''
		returns modification date
		@rtype: tuple
		@return: modification date
		'''
		return self.__modification_date

	def get_creation_date(self):
		'''
		returns creation date
		@rtype: tuple
		@return: creation date
		'''
		return self.__creation_date

	def get_access_date(self):
		'''
		returns access date
		@rtype: tuple
		@return: access date
		'''
		return self.__access_date
	
	
	def get_permissions(self):
		'''
		returns the permission of the file
		@rtype int
		@return: permision of the file
		'''
		
		return self.__permissions
	
	
	def get_permissions_octal(self):
		'''
		resturns the permission of the file in form of octal str
		
		@rtype: str
		@return: permission of the file
		'''
		
		if self.__platform.get_platform() == Platform.PLATFORM_POSIX :
			return oct(self.__permissions)
		else:
			raise PlatformSupportError, 'your platform does not support this method'
		
	
	def get_permissions_str(self):
		'''
		resturns the permission of the file in form of 'rwxrwxrwx'
		
		@rtype: str
		@return: permission of the file
		'''
		
		if self.__platform.get_platform() == Platform.PLATFORM_POSIX:
			factor = 256
			permission = ''
			for num in xrange(9):
				if self.__permissions == (self.__permissions | factor):
					if (num % 3) == 0:
						permission += 'r'
					elif (num % 3) == 1:
						permission += 'w'
					else:
						permission += 'x'
				else:
					permission += '-'
				factor = factor >> 1
			return permission
		else:
			raise PlatformSupportError, 'your platform does not support this method'
	
	def add_child(self, child):
		"""
		add a new file instance to childs of that file
		
		@param child: instance of FileObject
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		"""
		
		if child.__class__ != FileObject:
			raise InvalidParameterError('child', 'should be an instance of FileObject')
		
		self.__childs.append(child)
		return True
	
	def get_childs(self):
		"""
		return a list of fils those are childs of that file
		
		@rtype: list
		@return list of FileObject instances
		"""
		return self.__childs
	
	def __iter__(self):
		return self.__childs.__iter__()
	
	def get_path(self):
		return self.__path
	
	def get_name(self):
		return self.__platform.basename(self.__path)
	
	def get_user(self):
		return self.__user
	
	def get_group(self):
		return self.__group
	
	def get_type(self):
		return self.__type
	
	def get_platform(self):
		return self.__platform
	
	@classmethod
	def convert_permissions(cls, permissions, platform, convert_type = 1000):
		"""
		"""

		if not Validator.validate_non_empty_string(permissions):
			raise InvalidParameterError("permissions", "Must be non-empty string")
		if not Validator.validate_integer(convert_type):
			raise InvalidParameterError("convert_type", "Must be an integer value")
		
		if Platform.PLATFORM_POSIX == platform.get_platform():
			if True == Validator.validate_non_empty_string(permissions) and re.match('([-r][-w][-xsStT]){3,3}', permissions):

				result = 0
				if permissions[0] != '-':
					result |= FileObject.S_IRUSR
				if permissions[1] != '-':
					result |= FileObject.S_IWUSR
				if permissions[2] != '-':
					result |= FileObject.S_IXUSR
				if permissions[3] != '-':
					result |= FileObject.S_IRGRP
				if permissions[4] != '-':
					result |= FileObject.S_IWGRP
				if permissions[5] != '-':
					result |= FileObject.S_IXGRP
				if permissions[6] != '-':
					result |= FileObject.S_IROTH
				if permissions[7] != '-':
					result |= FileObject.S_IWOTH
				if permissions[8] != '-':
					result |= FileObject.S_IXOTH
					
			elif True == Validator.validate_non_empty_string(permissions) and re.match('(0)?[0-7]{3,3}', permissions):
				if len(permissions) == 3:
					permissions = '0' + permissions
				result = octstr_to_int(permissions)
			
			else:
				raise PermissionsInvalidError()

		elif Platform.PLATFORM_WINDOWS == platform.get_platform():
			if permissions.__class__ == str and re.match('[-r][-w]', permissions):
				result = 0
				if permissions[0] != '-':
					result |= FileObject.S_IREAD
				if permissions[1] != '-':
					result |= FileObject.S_IWRITE
			
			elif permissions.__class__ == str and re.match('(0)?[0-7]{3,3}', permissions):
				if len(permissions) == 3:
					permissions = '0' + permissions
				result = octstr_to_int(permissions)
			
			else:
				raise PermissionsInvalidError() 
		
		else:
			raise PlatformNotSupportedError()
		
		
		if convert_type != FileObject.PERMISSIONS_AS_INT:
			return result
		else:
			return int(oct(result))