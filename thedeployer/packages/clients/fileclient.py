#
# Copyright (c) 2008 vimov
#

import re

from thedeployer.packages.customexceptions import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.clients.abstractclient import AbstractClient
from thedeployer.packages.depfile.validator import Validator

class FileClient(AbstractClient):

	def __init__(self, platform, root):
		"""
		This is an abstract class and cannot be instantiated directly.

		@param __platform: the server's platform
		"""

		if self.__class__ == FileClient:
			raise NotSupportedError()

		if Platform != platform.__class__:
			raise InvalidParameterError('platform', 'Must be instance of Platform')

		# prepare the root

		if False == Validator.validate_string(root):
			raise InvalidParameterError('root', 'root should be a string')

		if len(root) != 0 and (platform.get_platform() == Platform.PLATFORM_POSIX):
			if root[0] != '/':
				raise InvalidParameterError('root', "root should start with '/'")
		elif len(root) != 0 and platform.get_platform() == Platform.PLATFORM_WINDOWS:
			if not re.match(r'[a-zA-Z]:\\', root[0:3]):
				raise InvalidParameterError('root', "root should start format like 'C:\\'")
		
		#if len(root) != 0 and (platform.get_platform() == Platform.PLATFORM_POSIX) and root[-1] != '/':
			#root += '/'
		#elif len(root) != 0 and platform.get_platform() == Platform.PLATFORM_WINDOWS and root[-1] != '\\':
			#root += '\\'

		if len(root) == 0:
			root = platform.get_root()
		else:
			root = root.rstrip(platform.get_separator()) + platform.get_separator()


		self.__platform = platform
		self.__root = root

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
		
		raise NotSupportedError()

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
		
		@raise NotSupportedError: If the server's platform is Windows
		@raise InvalidParameterError: if parameter are not valid
		@raise FileNotExistsError: if file or directory is not exist 
		"""
		
		raise NotSupportedError()

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
		
		raise NotSupportedError()

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
		
		raise NotSupportedError()

	def list(self, path, excludes = None, recursive = False, retry = 1):
		"""
		lists the file and directories in the path directory
		
		@param path : path of directory to be listed
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param recursive: if True ,contents of inner directories will be listed also. 
		@param retry: number of retries
		 
		@rtype : list
		@return: list of instances of File
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if path directory is not exist
		@raise ListDirectoryError: if error occurred in listing the directory
		"""
		
		raise NotSupportedError()

	def put(self, source, destination, excludes = None, contents_only = False, recursive = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
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
		
		raise NotSupportedError()

	def get(self, source, destination, excludes = None, contents_only = False, recursive = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
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
		@raise FileGetError: if error occurred during copying
		"""
		
		raise NotSupportedError()
	
	def move(self, source, destination, excludes = None, contents_only = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
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
		
		raise NotSupportedError()
	
	def rename(self, source, destination, retry = 1):
		"""
		rename a file or directory
		
		@param source: the source path to be renamed
		@param destination: the new name of file or dorectory
		@param retry: number of retries befor fail
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileMoveError: if error occurred during moving
		"""
		
		raise NotSupportedError()
	
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
		
		raise NotSupportedError()

	def get_platform(self):
		"""
		Return's the the platform of the server the client is communicating with.
		"""
		return self.__platform

	def get_root(self):
		return self.__root

	def execute(self, command, retry = 1):
		"""
		executes a shell command
		
		@param command: command to be executed
		 
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise CommandExecuteError: if command execution failed
		"""	
		
		raise NotSupportedError() 

	def get_last_modified_time(self, path, retry = 1):
		"""
		gets the last modification time of a file or directory
		
		@param path: path of file or directory.
		@param retry: number of times to retry.
		 
		@rtype: datetime
		@return: last modification time
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if path directory is already exist
		"""	
		
		raise NotSupportedError()

	def is_exists(self, path):
		"""
		Checks whether a file or directory exists at the specified path.

		@param path: The path to check.

		@rtype: Boolean
		@return: True on success, False on failure.
		"""

		raise NotSupportedError()

	def to_absolute(self, paths):
		"""
		Converts one or more paths to absolute, if they were relative.

		@param paths: Can be a list, or a string.

		@return: A list, or a string, based on the type of the argument.
		"""

		if paths.__class__ == list:

			for i in range(0, len(paths)):
				if self.get_platform().is_relative(paths[i]):
					paths[i] = self.get_platform().join(self.get_root(), paths[i])

			return paths

		elif True == Validator.validate_non_empty_string(paths):

			if self.get_platform().is_relative(paths):
				return self.get_platform().join(self.get_root(), paths)
			else:
				return paths

		else:
			raise InvalidParameterError("paths", "Must be a string or a list.")
