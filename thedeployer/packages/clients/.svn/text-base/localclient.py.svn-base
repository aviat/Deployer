#
# Copyright (c) 2008 vimov
#

import os
import re
import shutil
import time
from datetime import datetime
import inspect

from thedeployer.packages.customexceptions import *
from thedeployer.packages.clients.fileclient import FileClient
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.platform.file import FileObject
from thedeployer.packages.depfile.fileset import FileSet
from thedeployer.packages.filters.filterchain import FilterChain

class LocalClient(FileClient):
	
	def __init__(self, root = ""):
		
		platform = Platform.get_current()
		super(LocalClient, self).__init__(platform, root)

	def chmod(self, path, permissions, excludes = None, contents_only = False, recursive = False, retry = 1):
		"""
		Change the mode of path to the numeric mode. mode may take one of the following values (as defined in the stat module) or bitwise or-ed combinations of them:
		* S_IREAD, S_IWRITE, S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH
		
		Windows supports chmod() but you can only set the file's read-only flag with it (via the S_IWRITE and S_IREAD constants)
		
		@param path: path of the directory or file to be chmoeded 
		@param permissions: integer value of the permission
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if True it will chmod the directory contents
		@param recursive: if True, contents of directory will be chmoded recursively
		@param retry: number of retries 
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if file or directory does not exist
		@raise FileChmodError: if error occurred during chmod
		"""
		
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		if False == Validator.validate_non_empty_string(permissions):
			raise InvalidParameterError('permissions', 'should be string in form like "0777" , "777", "rwxr-xr-x"')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if contents_only.__class__ != bool:
			raise InvalidParameterError('contents_only', 'should be a boolean value')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be a boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		
		int_permissions = FileObject.convert_permissions(permissions, self.get_platform())
		
		#trim the '/' or '\' from the end of path
		path = self.get_platform().trim_path(path)
		
		if not os.path.exists(path):
			raise FileNotExistsError, 'file or directory does not exist'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
		
		if not os.path.isdir(path):
			recursive = False
			contents_only = False
		
		if recursive or contents_only:
			cont_list = os.listdir(path)
			for item in cont_list:
				new_path = path + self.get_platform().get_separator() + item
				
				base_name = self.get_platform().basename(new_path)
				parent_name = self.get_platform().dirname(new_path)
				
				if os.path.isfile(new_path):
					_type = FileObject.FILE
				else:
					_type = FileObject.DIRECTORY
						
				if not (excludes and excludes.match(parent_name, base_name, _type)):
					self.chmod(new_path, permissions, excludes, False, recursive, retry)
		
		if not contents_only:
			while retry:
				retry -= 1
				try:
					os.chmod(path, int_permissions)
				except Exception, e:
					if retry == 0:
						raise FileChmodError, str(e)
				else:
					break
			
		return True
	
	

	def chown(self, path, owner, group, excludes = None, contents_only = False, recursive = False, retry = 1):
		"""
		Change the ownership of a file or directory
		
		@param path: path of the file to be chowned
		@param owner: the new owner
		@param group: the new group
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if True, contents of directory only will be chowned
		@param recursive: if true changing owner will be executed recursively
		@param retry: number of retries
		   
		@rtype: bool
		@return: True on success
		
		@raise PlatformSupportError: if platform is windows platform
		@raise InvalidParameterError: if parameter are not valid
		@raise FileNotExistsError: if file or directory is not exist 
		"""
		
		if Platform.PLATFORM_WINDOWS == self.get_platform().get_platform():
			raise PlatformSupportError ('your platform does not support this method')
		
		import pwd
		
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		if False == Validator.validate_non_empty_string(owner):
			raise InvalidParameterError('owner', 'should be a non-empty string')
		if False == Validator.validate_non_empty_string(group):
			raise InvalidParameterError('group', 'should be a non-empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if contents_only.__class__ != bool:
			raise InvalidParameterError('contents_only', 'should be boolean value')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		
		
		try:
			user_data = pwd.getpwnam(owner)
			uid = user_data[2]
			gid = user_data[3]
		except:
			raise InvalidParameterError('owner', 'not  exist')
		
		
		#trim the '/' or '\' from the end of path
		path = self.get_platform().trim_path(path)
		
		if not os.path.exists(path):
			raise FileNotExistsError, 'file or directory does not exist'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
		
		if not os.path.isdir(path):
			recursive = False
			contents_only = False
		
		if recursive or contents_only:
			cont_list = os.listdir(path)
			for item in cont_list:
				new_path = path + self.get_platform().get_separator() + item
				
				base_name = self.get_platform().basename(new_path)
				parent_name = self.get_platform().dirname(new_path)
				
				if os.path.isfile(new_path):
					_type = FileObject.FILE
				else:
					_type = FileObject.DIRECTORY
						
				if not (excludes and excludes.match(parent_name, base_name, _type)):
					self.chown(new_path, owner, group, excludes, False, recursive, retry)
		
		if not contents_only:
			while retry:
				retry -= 1
				try:
					os.chown(path, uid, gid)
				except Exception, e:
					if retry == 0:
						raise FileChownError, str(e)
				else:
					break
		
		return True
	
	
	def delete(self, path, excludes = None, contents_only = False, recursive = False, retry = 1):
		"""
		deletes file or directory recursively or non  recursively
		
		@param path: path of the file or directory to be deleted
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if True, contents of directory only will be chowned
		@param recursive: if it is True the contents of non empty directory will be removed recursively else only file or
		empty directories will be deleted
		@param retry: number of retries 
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileRemoveError: if error occurred during removing
		"""
		
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if contents_only.__class__ != bool:
			raise InvalidParameterError('contents_only', 'should be a boolean value')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be a boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		
		#trim the '/' or '\' from the end of path
		path = self.get_platform().trim_path(path)
		
		if not os.path.exists(path):
			raise FileNotExistsError, 'file or directory does not exist'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
		
		if not os.path.isdir(path):
			recursive = False
			contents_only = False
						
			while retry:
				retry -= 1
				try:
					os.remove(path)
				except Exception, e:
					if retry == 0:
						raise FileRemoveError, str(e)
				else:
					break
		else:	
			if recursive or contents_only:
				cont_list = os.listdir(path)
				for item in cont_list:
					new_path = path + self.get_platform().get_separator() + item
					
					base_name = self.get_platform().basename(new_path)
					parent_name = self.get_platform().dirname(new_path)
				
					if os.path.isfile(new_path):
						_type = FileObject.FILE
					else:
						_type = FileObject.DIRECTORY
						
					if not (excludes and excludes.match(parent_name, base_name, _type)):
						self.delete(new_path, excludes, False, recursive, retry)
				
			if not contents_only:
				while retry:
					retry -= 1
					try:
						os.rmdir(path)
					except Exception, e:
						if retry == 0 and not excludes:
							raise FileRemoveError, str(e)
					else:
						break			
					
		return True
	
	

	def mkdir(self, path, mode = "0777", recursive = False, retry = 1):
		"""
		Create a directory named path
		
		@param path: path of directory to be created
		@param mode: the of the created file
		@param recursive: if true the method could create path tree 
		@param retry: number of retries
		 
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileExistsError: if path directory is already exist
		@raise MakeDirError: if error occurred while making a directory
		"""	
			
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		if mode.__class__ != str:
			raise InvalidParameterError('mode', 'should be a not empty string')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be a not empty string')
		
		mode = FileObject.convert_permissions(mode, self.get_platform())
		
		#trim the '/' or '\' from the end of path
		path = self.get_platform().trim_path(path)
		
		if os.path.exists(path):
			raise FileExistsError, 'file of directory exists'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
		
		while retry:
			retry -= 1
			try:
				if recursive:
					os.makedirs(path, mode)
				else:
					os.mkdir(path, mode)
			except Exception, e:
				if retry == 0:
					raise MakeDirError, str(e)
			else:
				break
		
		return True
	
	
	def list(self, path, excludes = None, recursive = False, retry = 1):
		"""
		lists the file and directories in the path directory
		
		@param path : path of directory to be listed
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param recursive: if True ,contents of inner directories will be listed also. 
		@param retry: number of retries
		 
		@rtype : list
		@return: list of instances of FileObject
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if path directory is not exist
		@raise ListDirectoryError: if error occurred in listing the directory
		"""
		
		file = self.__list(path, excludes, recursive, retry)
		return file.get_childs()
	
	
	def __list(self, path, excludes = None, recursive = False, retry = 1):
		
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be a bool')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be a bool')
		
		#trim the '/' or '\' from the end of path
		path = self.get_platform().trim_path(path)
		
		if not os.path.exists(path):
			raise FileNotExistsError, 'file or directory does not exist'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
		
		if not os.path.isdir(path):
			recursive = False
			
			if os.path.isfile(path):
				file_type = FileObject.FILE
			else:
				file_type = FileObject.LINK
				
			if Platform.PLATFORM_WINDOWS == self.get_platform().get_platform():
				user_id = ""
				group_id = ""
			else:
				user_id = os.stat(path).st_uid
				group_id = os.stat(path).st_gid
			
			return FileObject(self.get_platform(), path, file_type, os.stat(path).st_mode & 0777 , time.localtime(os.path.getmtime(path)), time.localtime(os.path.getctime(path)), time.localtime(os.path.getatime(path)), user_id, group_id)
				
		else:
			if Platform.PLATFORM_WINDOWS == self.get_platform().get_platform():
				user_id = ""
				group_id = ""
			else:
				user_id = os.stat(path).st_uid
				group_id = os.stat(path).st_gid
			
			file = FileObject(self.get_platform(), path, FileObject.DIRECTORY, os.stat(path).st_mode & 0777 , time.localtime(os.path.getmtime(path)), time.localtime(os.path.getctime(path)), time.localtime(os.path.getatime(path)), user_id, group_id)
			
			if recursive or inspect.stack()[1][3] == 'list':
				cont_list = os.listdir(path)
				for item in cont_list:
					new_path = path + self.get_platform().get_separator() + item
					
					base_name = self.get_platform().basename(new_path)
					parent_name = self.get_platform().dirname(new_path)
					
					if os.path.isfile(new_path):
						_type = FileObject.FILE
					else:
						_type = FileObject.DIRECTORY
					
					if not (excludes and excludes.match(parent_name, base_name, _type)):
						file.add_child(self.__list(new_path, excludes, recursive, retry))
			
			return file
	
	
	
	def put(self, source, destination, excludes = None, contents_only = False, recursive = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
		copy an directory or file recursively or not depending on recursive flag
		if create_dirs is True, the destination directory, named by destination, must not already exist; 
		it will be created as well as missing parent directories. Permissions and times of directories are copied
		If source is equal to destination and contents only is True the method do nothing
		
		@param source: the file or directory source to be copied.
		@param destination: the path where file or directory will be copied to.
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if true only contents of directory will be copied.
		@param recursive: if true files and directories will be copied and its contents recursively.
		@param create_dirs: if True destination must not already exist. It will be created as well as missing parent directories.
		@param replace: if true then if destination already exists it will be replaced.
		@param filter_chain: An instance of FilterChain, or None if no filtering is specified.
		@param retry: number of retries on fail.
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileExistsError: if destination already exists and and replace is false
		@raise FilePutError: if error occurred during copying
		"""
		
		if False == Validator.validate_non_empty_string(source):
			raise InvalidParameterError('source', 'should be a not empty string')
		if False == Validator.validate_non_empty_string(destination):
			raise InvalidParameterError('destination', 'should be a not empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if contents_only.__class__ != bool:
			raise InvalidParameterError('contents_only', 'should be a boolean value')
		if recursive.__class__ != bool:
			raise InvalidParameterError('recursive', 'should be a boolean value')
		if create_dirs.__class__ != bool:
			raise InvalidParameterError('create_dirs', 'create_dirs should be a bool')
		if replace.__class__ != bool:
			raise InvalidParameterError('replace', 'should be a boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		if filter_chain.__class__ != FilterChain and filter_chain != None:
			raise InvalidParameterError("filter_chain", "should be instance of FilterChain")
		
		#trim the '/' or '\' from the end of path
		source = self.get_platform().trim_path(source)
		destination = self.get_platform().trim_path(destination)
		
		#test if source is relative
		if self.get_platform().is_relative(source) :
			source = self.__root + source
		
		#test if destination is relative
		if self.get_platform().is_relative(destination) :
			destination = self.__root + destination
		
		if not os.path.exists(source):
			raise FileNotExistsError, 'the file or directory to be copied is not exist'
		
		#get source file or directory name
		base_name = self.get_platform().basename(source)
		tmp_dest = destination + self.get_platform().get_separator() + base_name
		source_permission = os.stat(source).st_mode & 0777
		
		#list the contents of source
		if os.path.isdir(source):
			cont_list = os.listdir(source)
		
		if re.match(re.escape(source+self.get_platform().get_separator())+'(.)+', destination):
			raise FilePutError('cannot copy a directory into itself')
		
		tem_retry = retry
		while tem_retry:
			tem_retry -= 1
			try:
				if not os.path.exists(destination):
					if not create_dirs:
						raise FileNotExistsError, 'destination directory is not exist'
					else:
						os.makedirs(destination, 0777)
				else:
					if not os.path.isdir(destination):
						raise FileExistsError, 'Destination should be a directory'
				
				if os.path.exists(tmp_dest):
					if source != tmp_dest:
						if os.path.isfile(source):
							if os.path.isfile(tmp_dest):
								if replace:
									self.delete(tmp_dest, None, False, True, 1)
								else:
									raise FileExistsError, 'destination already has file with the same name'
							else:
								raise FileExistsError, "cannot replace a non file with a file"
						elif os.path.isdir(source) and not contents_only:
							if os.path.isfile(tmp_dest):
								raise FileExistsError, 'cannot replace a non directory with a directory'
					else:
						if not replace:
							raise FileExistsError, "file already exists"
						else:
							return True
				else:
					if os.path.isdir(source):
						if not contents_only:
							os.mkdir(tmp_dest, source_permission)
						
				#if source path is a file
				if os.path.isfile(source):
					contents_only = False
					recursive = False
					shutil.copy2(source, destination)
					if filter_chain:
						filter_chain.apply_to_file(tmp_dest)
							 	
				if os.path.isdir(source):
					if not contents_only:
						destination = tmp_dest
					
					if recursive or contents_only:
						for item in cont_list:
							new_source = source + self.get_platform().get_separator() + item
							
							base = self.get_platform().basename(new_source)
							parent = self.get_platform().dirname(new_source)
							
							if os.path.isfile(new_source):
								_type = FileObject.FILE
							else:
								_type = FileObject.DIRECTORY
							
							if not (excludes and excludes.match(parent, base, _type)):
								self.put(new_source, destination, excludes, False, recursive, create_dirs, replace, filter_chain, retry)
			except Exception, e:
				if tem_retry == 0:
					#raise FilePutError, str(e)
					raise
			else:
				break
		
		return True


	def move(self, source, destination, excludes = None, contents_only = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
		move a file or directory to another location either recursively or not depending on the recursive flag. 
		If source is equal to destination and contents only is True the method do nothing
		
		@param source: the file or directory source to be moved.
		@param destination: the path where file or directory will be moved to.
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if true only contents of directory will be copied.
		@param create_dirs: if True destination must not already exist. It will be created as well as missing parent directories.
		@param replace: if true then if destination already exists it will be replaced.
		@param filter_chain: An instance of FilterChain, or None if no filtering is specified.
		@param retry: number of retries on fail.
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileExistsError: if destination already exists and and replace is false
		@raise FileMoveError: if error occurred during moving
		"""
		
		if False == Validator.validate_non_empty_string(source):
			raise InvalidParameterError('source', 'should be a not empty string')
		if False == Validator.validate_non_empty_string(destination):
			raise InvalidParameterError('destination', 'should be a not empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if contents_only.__class__ != bool:
			raise InvalidParameterError('contents_only', 'should be a boolean value')
		if create_dirs.__class__ != bool:
			raise InvalidParameterError('create_dirs', 'create_dirs should be a bool')
		if replace.__class__ != bool:
			raise InvalidParameterError('replace', 'should be a boolean value')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		if filter_chain.__class__ != FilterChain and filter_chain != None:
			raise InvalidParameterError("filter_chain", "should be instance of FilterChain")
		
		#trim the '/' or '\' from the end of path
		source = self.get_platform().trim_path(source)
		destination = self.get_platform().trim_path(destination)
		
		#test if source is relative
		if self.get_platform().is_relative(source) :
			source = self.__root + source
		
		#test if destination is relative
		if self.get_platform().is_relative(destination) :
			destination = self.__root + destination
		
		if not os.path.exists(source):
			raise FileNotExistsError, 'the file or directory to be moved is not exist'
		
		#get source file or directory name
		base_name = self.get_platform().basename(source)
		tmp_dest = destination + self.get_platform().get_separator() + base_name
		source_permission = os.stat(source).st_mode & 0777
		
		#list the contents of source
		if os.path.isdir(source):
			cont_list = os.listdir(source)
		
		if re.match(re.escape(source+self.get_platform().get_separator())+'(.)+', destination):
			raise FileMoveError, 'cannot move a directory into itself'
		
		tmp_retry = retry
		while tmp_retry:
			tmp_retry -= 1
			try:
				if not os.path.exists(destination):
					if not create_dirs:
						raise FileNotExistsError, 'destination directory is not exist'
					else:
						os.makedirs(destination, 0777)
				else:
					if not os.path.isdir(destination):
						raise FileExistsError, 'cannot replace a non directory with a directory'
				
				if os.path.exists(tmp_dest):
					if source != tmp_dest:
						if os.path.isfile(source):
							if os.path.isfile(tmp_dest):
								if replace:
									self.delete(tmp_dest, None, False, True, 1)
								else:
									raise FileExistsError, 'destination already has file with the same name'
							else:
								raise FileExistsError, "cannot replace a non file with a file"
						elif os.path.isdir(source) and not contents_only:
							if os.path.isfile(tmp_dest):
								raise FileExistsError, 'cannot replace a non directory with a directory'
					else:
						if not replace:
							raise FileExistsError, "file already exists"
						else:
							return True
				else:
					if os.path.isdir(source):
						if not contents_only:
							os.mkdir(tmp_dest, source_permission)
						
				#if source path is a file
				if os.path.isfile(source):
					contents_only = False
					shutil.move(source, destination)
					if filter_chain:
						filter_chain.apply_to_file(tmp_dest)
						 	
				if os.path.isdir(source):
					if not contents_only:
						destination = tmp_dest
					
					for item in cont_list:
						new_source = source + self.get_platform().get_separator() + item
							
						base = self.get_platform().basename(new_source)
						parent = self.get_platform().dirname(new_source)
						
						if os.path.isfile(new_source):
							_type = FileObject.FILE
						else:
							_type = FileObject.DIRECTORY
						
						if not (excludes and excludes.match(parent, base, _type)):
							self.move(new_source, destination, excludes, False, create_dirs, replace, filter_chain, retry)
					
					if not os.listdir(source) and not contents_only:
						os.rmdir(source)
			except Exception, e:
				if tmp_retry == 0:
					raise FileMoveError, str(e)
			else:
				break
		
		return True
	
	
	def rename(self, source, destination, retry = 1):
		"""
		rename a file or dirctory
		
		@param source: the source path to be renamed
		@param destination: the new name of file or dorectory
		@param retry: number of retries befor fail
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileRenameError: if error occurred during moving
		"""
		
		if False == Validator.validate_non_empty_string(source):
			raise InvalidParameterError('source', 'should be a not empty string')
		if False == Validator.validate_non_empty_string(destination):
			raise InvalidParameterError('destination', 'should be a not empty string')
		if retry.__class__ != int:
			raise InvalidParameterError('retry', 'should be an integer value')
		
		#trim the '/' or '\' from the end of path
		source = self.get_platform().trim_path(source)
		
		#test if source is relative
		if self.get_platform().is_relative(source) :
			source = self.__root + source
		
		if not os.path.exists(source):
			raise FileNotExistError, 'the file or directory to be moved is not exist'
		
		while retry:
			retry -= 1
			try:
				parent = self.get_platform().dirname(source)
				destination = parent + self.get_platform().get_separator() + destination
				os.rename(source, destination)
			except Exception, e:
				if retry == 0:
					raise FileRenameError, str(e)
			else:
				break
		
		return True
	
	def execute(self, command, retry = 1):
		"""
		executes a shell command
		
		@param command: command to be executed
		 
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise CommandExecuteError: if command execution failed
		"""	
			
		if False == Validator.validate_non_empty_string(command):
			raise InvalidParameterError('command', 'should be a not empty string')
		
		while retry:
			retry -= 1
			try:
				os.system(command)
			except Exception, e:
				if retry == 0:
					raise CommandExecuteError, str(e)
	
	
	def get_last_modified_time(self, path):
		"""
		gets the last modification time of a file or directory
		
		@param path: path of directory to
		 
		@rtype: tuple
		@return: last modification time
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if path directory is already exist
		"""	
			
		if False == Validator.validate_non_empty_string(path):
			raise InvalidParameterError('path', 'should be a not empty string')
		
		if not (re.match(r'/', path) or re.match(r'[a-zA-Z]:\\', path)):
			path = path.rstrip(self.get_platform().get_separator())
		if not os.path.exists(path):
			raise FileNotExistsError, 'file or directory not exists'
		
		#test if path is relative
		if self.get_platform().is_relative(path) :
			path = self.__root + path
			
		tmp_time = time.localtime(os.path.getmtime(path))
		
		return datetime(tmp_time[0], tmp_time[1], tmp_time[2], tmp_time[3], tmp_time[4], tmp_time[5],)
	
	
	def get_temp_name(self, parent, prefix = ""):
		"""
		Returns the path to a non-existing temporary file name in the directory parent. The file can be
		optionally prefixed with "prefix".
		
		@param parent: The parent directory to store the file at.
		@param prefix: A prefix to add to the file name.
		
		@rtype: string
		@return: The path of the file.
		
		@raise TemporaryFileError: If it cannot return such path.
		"""
		
		if not Validator.validate(parent, 'non_empty_string'):
			raise InvalidParameterError('parent', 'should be a non-empty string')
		if not Validator.validate(prefix, 'string'):
			raise InvalidParameterError('prefix', 'should be a string value')
		
		try:
			return self.get_platform().basename(os.tempnam(parent, prefix))
		except Exception, e:
			raise TemporaryFileError, str(e)
	
	
	def is_exists(self, path):
		"""
		Checks whether a file or directory exists at the specified path.

		@param path: The path to check.

		@rtype: Boolean
		@return: True on success, False on failure.
		"""

		if not Validator.validate(path, 'non_empty_string'):
			raise InvalidParameterError('path', 'should be a non-empty string')
		
		return os.path.exists(path)
