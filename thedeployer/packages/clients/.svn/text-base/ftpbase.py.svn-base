#
# Copyright (c) 2008 vimov
#

import datetime
import os
import shutil

from thedeployer.packages.customexceptions import *
from thedeployer.packages.logger import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.clients.fileclient import *
from thedeployer.packages.depfile.fileset import * 
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.platform.file import FileObject
from thedeployer.packages.clients.ftplistparser import *

class FtpBase(FileClient):

	'''
	
	this class is interface of the ftp available functions, and all the child class must implement all its methods 
	the interface functions are

	'''
	
	"""@param host: server host name""" 
	"""@param username: server user name """
	"""@param passwd: server password"""
	"""@param port: server port number"""
	"""@param __ftp_client: local ftp client""" 
	"""@param root: the root directory of the ftp server""" 
	
	def __init__(self, platform, host, username, password, port, root):
		
		"""
		constructor of the class
		"""
		
		if self.__class__ == FtpBase:
			raise NotImplementedError, "can not create Instance from FtpBase"
		
		if not Validator.validate_non_empty_string(host):
			raise InvalidParameterError("host", "host server can not be None")
		
		if platform is None:
			raise InvalidParameterError("platform", "Platform can not be None")

		super(FtpBase, self).__init__(platform, root)

		self.host = host
		self.username = username
		self.password = password
		self.port = port
		self.__ftp_client = None

	def set_client(self, client):
		"""
		set the local client
		"""
		self.__ftp_client = client
		
	def get_client(self):
		"""
		get instance of the local client
		"""
		return  self.__ftp_client
	
	def append_to_root(self, path):
		path = path.rstrip(' ')
		path = path.rstrip(self.get_platform().get_separator())
		if self.get_platform().is_relative(path):
			path = self.get_root() + path
		return path
	
	def connect(self):
		'''
		connect with the ftp server with the specified conf        
		return ture on success
		return false on failure
		'''
		raise NotSupportedError()
	
	def __put_file(self, source, destination, replace, retry):
		"""
		it will be implemented by the child class according to the used ftp library  
		"""
		raise NotSupportedError()

	def __put(self, source, destination, excludes, replace, recursive, filter_chain, retry):
		"""
		put the file or directory recursively
		"""
		if os.path.isfile(source):
			if not (excludes and excludes.match(source, os.path.basename(source), FileObject.FILE)):
				destination = self.get_platform().join(destination, os.path.basename(source))
				source = self.__filter_remote(source, filter_chain)
				self.__put_file(source, destination, replace, retry)
		elif os.path.isdir(source):
			if not( excludes and excludes.match(source, os.path.basename(source), FileObject.DIRECTORY)):
				files = os.listdir(source)
				for file in files:
					newsource = os.path.join(source, file)
					if os.path.isfile(newsource):
						self.__put(newsource, destination, excludes, replace, recursive, filter_chain, retry)
					elif os.path.isdir(newsource):
						newdestination = self.get_platform().join(destination, file)
						self.mkdir(newdestination)
						if recursive:
							self.__put(newsource, newdestination, excludes, replace, recursive, filter_chain, retry)
			
	def __filter_remote(self, filepath, filter_chain):
		"""
		if the filter chain is not None it will apply the changes to the file
		"""
		newpath = filepath
		if filter_chain:
			newpath = self.get_platform().get_temp_dir() + os.sep + os.path.basename(filepath) 
			shutil.copy2(filepath, newpath)
			filter_chain.apply_filter_to_file(newpath)
		return newpath
				
	def put(self, source, destination, excludes = None, contents_only = False, recursive = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		'''
		upload file or folder from the source into the destination
		
		@param source: local path
		@param destination: destination path
		@param excludes: list of excluded files or folders from the uploading operation 
		@param recusive: boolean for upload the folder with its subfolders or not
		@param contents_only: boolean for uploading the contents of the dir directly to the server without creating it on the server
								or create it first and upload the data inside it  
		@param create_dirs: boolean for creating the destination if not exist or not
		@param replace: replace the existing files or not
		@param filter_chain: filter for the uploaded files
		@param retry: if file uploading failed try again with number of retry 
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileExistsError: if destination already exists and and replace is false
		@raise FilePutError: if error occurred during copying
		'''
		if not Validator.validate_non_empty_string(source):
			raise InvalidParameterError("source", "source can not be None or empty string")

		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination can not be None")

		#if the client is None
		if self.__ftp_client is None:			
			self.connect()
		
		source = source.rstrip(' ')
		source = source.rstrip(os.sep)

		if destination == '.':
			destination = self.get_cwd()
		else:
			destination = self.append_to_root(destination)

		if not os.path.exists(source):
			raise FileNotExistsError, source

		if not self.is_exists(destination):
			if create_dirs:
				self.mkdir(destination, recursive = True)
			else:
				raise FileNotExistsError, destination
		else:
			if self.get_type(destination) == FileObject.FILE:
				raise FileExistsError, destination

		newdestination = self.get_platform().join(destination, os.path.basename(source))
		if self.is_exists(newdestination):
			 if not replace:
					raise FileExistsError, newdestination
		
		if os.path.isfile(source):
			try:
				self.__put(source, destination, excludes, replace, recursive, filter_chain, retry)
			except Exception, e:
				raise FilePutError('can not upload ' + source, str(e))
		else:
			if not contents_only:
				destination = self.get_platform().join(destination, os.path.basename(source))
				self.mkdir(destination)
			
			if recursive or contents_only:
				try:
					self.__put(source, destination, excludes, replace, recursive, filter_chain, retry)
				except Exception, e:
					raise FilePutError('can not upload ' + source, str(e))

	def __delete_file(self, path, retry):
		"""
		delete remote file 
		"""
		raise NotSupportedError()
	
	def __delete_empty_dir(self, path, retry):
		"""
		delete empty directory
		"""
		raise NotSupportedError()
 
	def __delete(self, files, excludes, recursive, retry):
		if files is not None:
			for file in files:
				filename = self.get_platform().basename(file.get_path())
				if not (excludes is not None and  excludes.match(file.get_path(), filename, file.get_type())):
					if file.get_type() == FileObject.DIRECTORY:
						self.__delete(file.get_childs(),excludes, True, retry)
						if recursive:
							self.__delete_empty_dir(file.get_path(), retry)
					else:
						self.__delete_file(file.get_path(), retry)
	
	def delete(self, path, excludes = None, contents_only = False, recursive = False, retry = 1):
		'''
		delete file or directory from the server
		
		@param path: path to be deleted
		@param excludes: list of the excluded file from the operation
		@param contents_only: boolean for deleting the contents of the file and only or the file its self also
		@param recursive: if the path is directory delete it recusively or not
		@param retry: retry count if the operation is failed 

		@raise InvalidParameterError: If the required argument(s) are not specified.
		'''
		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")

		if self.__ftp_client is None:			
			self.connect()

		if path == '.':
			path = self.get_cwd()
		else:
			path = self.append_to_root(path)
		
		try:
			if self.is_exists(path):
				path_type = self.get_type(path)
				file_name = self.get_platform().basename(path)
				
				if not (excludes is not None and  excludes.match(path, file_name, path_type)):
					if path_type is FileObject.DIRECTORY:
						"""
						delete directory 
						"""
						files = self.list(path , excludes, recursive)
						if not recursive and not contents_only and len(files) == 0:
							self.__delete_empty_dir(path, retry)
						elif not recursive and not contents_only and len(files) > 0:
							raise DirectoryNotEmptyError, path
						elif not recursive and contents_only:
							return 
						else:												
							self.__delete(files, excludes, recursive, retry)
							if not contents_only:
								self.__delete_empty_dir(path, retry)
					else:
						self.__delete_file(path, retry)

		except Exception, e:
			message = 'can not delete the file ' + path
			raise FileDeleteError(message, str(e))


	
	def __get_file(self, source, destination, replace, retry):
		"""
		it will be implemented by the child class according to the used ftp library 
		"""
		raise NotSupportedError()

	def __create_local_dir(self, path, recursive = False):
		"""
		create the local directory
		"""
		try:
			if not os.path.isfile(path):
				if recursive:
					os.makedirs(path, 0755)
				else:
					os.mkdir(path)
			else:
				raise FileExistsError(path)
		except Exception, e:
			message = str(e)
			"""
			possible error messages
			OSError: [Errno 17] File exists: '/home/leaf/new'
			OSError: [Errno 13] Permission denied: '/home/leaf/new/test'
			OSError: [Errno 2] No such file or directory: '/home/leaf/test/test'
			"""
			if message.find("File exists") < 0:
				raise
	
	def __get(self, files, destination, excludes, replace, filter_chain, retry):
		"""
		get file or directory recursively
		"""
		if files is not None:
			for file in files:
				filename = self.get_platform().basename(file.get_path())
				if not (excludes is not None and  excludes.match(file.get_path(), filename, file.get_type())):
					newdestination = os.path.join(destination, filename)
					if file.get_type() == FileObject.FILE:
						self.__get_file(file.get_path(), newdestination, replace, retry)
						if filter_chain:
							"""
							apply filter changes to files if filter is not none
							"""
							filter_chain.apply_filter_to_file(newdestination)
					elif file.get_type() == FileObject.DIRECTORY:
						self.__create_local_dir(newdestination)
						self.__get(file.get_childs(), newdestination, excludes, replace, filter_chain, retry)
						
	def get(self, source, destination, excludes = None, contents_only = False, recursive = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		'''
		download file or directory from the ftp server
		
		@param source: the remote path to be downloaded
		@param destination: local path to save downloaded file on it
		@param excludes: list of the excluded file from the operation
		@param contents_only: for deciding to download the the contents of the directory only or the directory its self
		@param recursive: for deciding to download the directory recursively (download its subdirectories also) or not
		@param create_dirs: boolean for creating the destination if not exist or not
		@param replace: replace the existing files or not
		@param filter_chain: filters applied on the downloaded files
		@param retry: if file uploading failed try again with number of retry 

		@raise InvalidParameterError: If the required argument(s) are not specified.
		@raise GetFileError: when the operation is failed
		'''
		if not Validator.validate_non_empty_string(source):
			raise InvalidParameterError("source", "source can not be None or empty string")

		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination can not be None")

		#if the client is not connected
		if self.__ftp_client is None:			
			self.connect()
		
		if source == '.':
			source = self.get_cwd()
		else:
			source = self.append_to_root(source)
		
		if not self.is_exists(source):
			raise FileNotExistsError(source)

		try:
			source_type = self.get_type(source)
			if not (excludes is not None and  excludes.match(source, self.get_platform().basename(source), source_type)):
				if not os.path.exists(destination):
					if create_dirs:
						self.__create_local_dir(destination, recursive = True)
					else:
						raise FileNotExistsError, destination
				else:
					if os.path.isfile(destination):
						raise FileExistsError, destination

				if source_type is FileObject.FILE:
					destination = os.path.join(destination, self.get_platform().basename(source))
					self.__get_file(source, destination, replace, retry)
					if filter_chain:
						"""
						apply filter changes to files if filter is not none
						"""
						filter_chain.apply_filter_to_file(destination)
				elif source_type is FileObject.DIRECTORY:

					if not contents_only:
						destination = os.path.join(destination, self.get_platform().basename(source))
						self.__create_local_dir(destination, recursive = False)
					
					if recursive or contents_only:
						files = self.list(source , excludes, recursive)
						self.__get(files, destination, excludes, replace, filter_chain, retry)
					
		except Exception, e:
			raise GetFileError('can not download the file ' + source, str(e))

	def __list(self, path, excludes, recursive, retry):
		files_list =  self.__get_dir_list(path, retry)
		files = []
		for file_list in files_list:
			ftp_file = FtpListParser(self.get_platform(), file_list)
			file_path = self.get_platform().join(path, ftp_file.get_name())
			file_type = ''
			if ftp_file.get_type() == 'd':
				file_type = FileObject.DIRECTORY
			elif ftp_file.get_type() == 'l':
				file_type = FileObject.LINK
			elif ftp_file.get_type() == 's':
				file_type = FileObject.SOCKET
			elif ftp_file.get_type() == 'c':
				file_type = FileObject.CHARCTER_DEVICE
			elif ftp_file.get_type() == 'p':
				file_type = FileObject.PIPE
			elif ftp_file.get_type() == 'b':
				file_type = FileObject.BLOCK_DEVICE
			elif ftp_file.get_type() == 'D':
				file_type = FileObject.DOOR
			else:
				file_type = FileObject.FILE

			if not (excludes is not None and excludes.match(path, ftp_file.get_name(), file_type)):
				resfile = FileObject(self.get_platform(), file_path, file_type, ftp_file.get_mode(), 
									 ftp_file.get_date(), '', '', ftp_file.get_owner(), ftp_file.get_group())
				children = []
				if ftp_file.get_type() == 'd' and recursive:
					children = self.__list(file_path, excludes, True, retry)
					for child in children:
						resfile.add_child(child)
				files.append(resfile)
		return files
	
	def list(self, path, excludes = None, recursive = False, retry = 1):
		'''
		list directory contents
		
		@param path: directory to be listed
		@param excludes: excluded files
		@param recursive: boolean for list the directory recursively or not
		@param retry: count of function retry
		
		@return: list of current working directory files  

		@raise InvalidParameterError: If the required argument(s) are not specified.
		@raise ListDirectoryError: If the specified directory can not be listed
		@raise FileNotExistsError: if the path not exist
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")
		
		if not Validator.validate_boolean(recursive):
			raise InavlidParameterError("recursive", "recursive must be boolean")

		if not Validator.validate_integer(retry):
			raise InavlidParameterError("retry", "retry must be integer")

		try:
			if path == '.':
				path = self.get_cwd()
			else:
				path = self.append_to_root(path)
			
			if not self.is_exists(path):
				raise FileNotExistsError(path)
			
			return self.__list(path, excludes, recursive, retry)
		except Exception, e:
			raise #ListDirectoryError('Can not list directory ' + path + " " + str(e))

	def __chdir(self, path):
		raise NotSupportedError
	
	def chdir(self, path):
		'''
		change the current working directory to specified path
		
		@param path: target current working directory
		
		@raise InvalidParameterError: If the required argument(s) are not specified.  
		@raise FtpCommandError: If the function can not change the current working directory  		
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")
		
		try:
			path = self.append_to_root(path)
			self.__chdir(path)
		except Exception, e:
			message = str(e)
			if message.find('No such file') > 0:
				raise FileNotExistsError, path
			else:
				raise FtpCommandError("can not change current working directory to " + path, str(e))
	
	def cdup(self):
		'''
		go to the parent directory
		
		@raise FtpCDUPError: If the server can not go the parent directory 
		'''
		raise NotSupportedError()
	
	def get_cwd(self):
		'''
		get the current working directory
		
		@rtype: String
		@return: the current working directory
		
		@raise FtpGetCWDError: If the function fails to get the current working directory 
		'''
		raise NotSupportedError()
	
	def __mkdir(self, path, mode, retry):
		raise NotSupportedError()
	
	def mkdir(self, path, mode = "755", recursive = False, retry = 1):
		'''
		make a directory on the remote server on the current directory, if the parameter is path 
		it must be found except the basename 
		Example:
		dir = a/b/c
		a/b must be found and c will be created
		 if dir = a then a will be created 
		
		@param path: directory path
		@param mode: mode of the directory
		@param recurisve : boolean for creating the full path or the last level only
		@param retry: count of the function retry 

		@raise InvalidParameterError: If the required argument(s) are not specified.
		  		
		@raise MakeDirError: If the function failed to make the directory
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")
		
		if not Validator.validate_non_empty_string(mode):
			raise InvalidParameterError("mode", "mode can not be None or empty string")
		
		try:
			mode = self.__get_permissions(mode)
			path = self.append_to_root(path)
			if not recursive:
					if self.is_exists(path):
						if  self.get_type(path) == FileObject.FILE:
							raise FileExistsError("can not replace file with directory " + path)
					else:
						self.__mkdir(path, mode, retry)
			else:
				base =  self.get_root()
				tmp = path[len(base):] 
				list = tmp.split(self.get_platform().get_separator())
				for dir in list:
					if len(dir) > 0:
						base = base + dir
						if self.is_exists(base):
							if  self.get_type(base) == FileObject.FILE:
								raise FileExistsError("can not replace file with directory " + base)
						else:
							self.__mkdir(base, mode, retry)
						base = base + self.get_platform().get_separator()
		except Exception, e:
			message = str(e)
			if message.find("Permission denied") > 0:
				raise PermissionDeniedError, path
			elif message.find("File exists") > 0:
				return 
			else:
				raise MakeDirError('can not make dir ' + path, message)

	def get_type(self, path):
		"""
		check the type of the path is directory or file assuming the if it is not a file it will be a directory
		
		@return: type of the path
		@rtype: FileObject.FILE or FileObject.DIRECTORY
		"""

		raise NotSupportedError
		
	def __get_last_modified_time(self, path):
		"""
		must return the time represented as tuple of minimum 6 element
		year month day hour minutes seconds
		"""
		
		raise NotSupportedError
	
	def get_last_modified_time(self, path, retry = 1):
		'''
		get the last modification time of file using the FTP command MDTM
		
		@param path: path of the file to get the last modification time
		@param retry: number of the retry on the function failure

		@rtype: datetime object
		@type last_modified_time: last modified time of the specified path
		
		@raise InvalidParameterError: If the required argument(s) are not specified. 
		@raise GetLastModificationTimeError: If any failure occurred while performing the command
		@raise FileNotExistError: if the file is not found     
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")
		
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "retry must be integer")

		while retry > 0:
			retry = retry - 1
			try:
				path = self.append_to_root(path)
				__time = self.__get_last_modified_time(path)
				return datetime.datetime(int(__time[0]), int(__time[1]), int(__time[2]), int(__time[3]), int(__time[4]), int(__time[5]))
			except Exception, e:
				message = str(e)
				if message.find('No such file') > 0:
					raise FileNotExistsError, path
		raise GetLastModificationTimeError(path, str(e))

	def move(self, source, destination, excludes = None, contents_only = False, create_dirs = False, replace = False, filter_chain = None, retry = 1):
		"""
		move file or directory from the source under the destination
		
		@param source: the file or directory source to be moved.
		@param destination: the path where file or directory will be moved to.
		@param excludes: An instance of FileSet that describes the exclusion patterns.
		@param contents_only: if true only contents of directory will be copied.
		@param create_dirs: if True destination must not already exist. It will be created as well as missing parent directories.
		@param replace: if true then if destination already exists it will be replaced.
		@param filter_chain: An instance of FilterChain, or None if no filtering is specified.
		@param retry: number of retries on fail.
		
		@rtype: boolean
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileExistsError: if destination already exists and and replace is false
		@raise FileMoveError: if error occurred during moving
		"""

		if not Validator.validate_non_empty_string(source):
			raise InvalidParameterError("source", "source can not be None or empty string")

		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination can not be None or empty string")

		if destination == '.':
			destination = self.get_cwd()
		else:	
			destination = self.append_to_root(destination)
			
		if source == '.':
			source = self.get_cwd()
		else:
			source = self.append_to_root(source)
			
		if not self.is_exists(source):
			raise FileNotExistsError, source
		
		if not (excludes and excludes.match(source, self.get_platform().basename(source), self.get_type(source))):
			if not self.is_exists(destination):
				if create_dirs:
					self.mkdir(destination, "755", True)
				else:
					raise FileNotExistsError, destination
			else:
				if self.get_type(destination) == FileObject.FILE:
					raise FileExistsError, destination
			
			target_path = self.get_platform().join(destination, self.get_platform().basename(source))
			
			if self.is_exists(target_path):
				if self.get_type(target_path) == FileObject.FILE:
					if replace:
						try:
							if source != target_path:
								self.delete(target_path, excludes = None, contents_only = False, recursive = False, retry = 2)
						except Exception, e:
							raise FileExistsError, target_path + " " + str(e)
					else:
						raise FileExistsError, target_path
				else:
					if not replace:
						raise FileExistsError, target_path
			
			if target_path != source:
				if self.get_type(source) == FileObject.FILE:
					self.rename(source, target_path, retry)
				elif not contents_only:
					self.rename(source, target_path, retry)
				else:
					files = self.list(source, excludes, True)
					self.__move_dir(files, destination, replace, retry)

	def __move_dir(self, files, destination, replace, retry):
		for file in files:
			newdestination = self.get_platform().join(destination, self.get_platform().basename(file.get_path()))
			try:
				self.rename(file.get_path(), newdestination, retry)
			except FileExistsError, e:
				if not replace:
					raise
				if file.get_type() == FileObject.DIRECTORY:
					if replace:
						self.__move_dir(file.get_childs(), newdestination, replace, retry)

	def __rename(self, source, destination):
		"""
		it is implemented by the child  class
		"""
		
		raise NotSupportedError()
	
	def rename(self, source, destination, retry = 1):
		"""
		rename a file or directory
		
		@param source: the source path to be renamed
		@param destination: the new name of file or dorectory
		@param retry: number of retries on failure
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: if parameters are not valid
		@raise FileNotExistsError: if source file or directory is not exist or if create_dirs equal False and destination directory is not exist
		@raise FileExistsError: if the destination exists
		@raise PermissionDeniedError: if the operation is not permitted
		@raise FileRenameError: if error occurred during moving
		"""
		
		if not Validator.validate_non_empty_string(source):
			raise InvalidParameterError("source", "source can not be None or empty string")

		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination can not be None or empty string")
		
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "retry must be integer")
		
		#add root if the paths is relative 
		source = self.append_to_root(source)
		destination = self.append_to_root(destination)
		
		if self.is_exists(destination):
			raise FileExistsError, destination
		
		while retry > 0:
			retry = retry - 1
			try:
				self.__rename(source, destination)
				return 
			except Exception, e:
				message = str(e)
				if message.find("No such file") > 0:
					raise FileNotExistsError(source)
				elif message.find("Permission denied") > 0:
					raise PermissionDeniedError
				else:
					if retry == 0:
						raise FileRenameError(source + " " + str(e)) 

	 	
						
						
	def __chmod(self, path, mode, retry):
		"""
		must be implemented by the child class according to the used library for the ftp server
		"""
		
		raise NotSupportedError() 
	
	def __chmod_list(self, list, mode, retry):
		if list is not None:
			for file in list:
				self.__chmod(file.get_path(), mode, retry)
				self.__chmod_list(file.get_childs(), mode, retry)
			

	def chmod(self, path, permissions, excludes = None, contents_only = False, recursive = False, retry = 1):
		'''
		Change the permissions of file or directory on ftp server.
		
		@param path: path of the remote file
		@param permissions: target permissions
		@param excludes: the excluded files from the operation
		@param contents_only: boolean for changing the contents of the directory only or also the directory itself
		@param recursive: boolean for chmoding the directory recursively or not
		@param retry: the retry count on failure 
		
		@raise InvalidParameterError: If the required argument(s) are not specified. 
		@raise FileChmodError: If the function fails to chmod the file
		'''

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")

		if not Validator.validate_non_empty_string(permissions):
			raise InvalidParameterError("permissions", "permissions can not be None or empty string")
		
		path = self.append_to_root(path)
		
		if not self.is_exists(path):
			raise FileNotExistsError, path
		try:
			permissions = self.__get_permissions(permissions)
			excluded = False
			path_type = self.get_type(path)
			if excludes is not None:
				if excludes.match(path, self.get_platform().basename(path), path_type):
					excluded = True
			if not contents_only and not excluded:
				self.__chmod(path, permissions, retry)
				
			if (contents_only or recursive) and path_type is FileObject.DIRECTORY:
				list = self.list(path, excludes,  recursive, retry)
				self.__chmod_list(list, permissions, retry)
		except Exception, e:
			message = str(e)
			if message.find("Operation not permitted") > 0:
				raise PermissionDeniedError
			else:
				raise FileChmodError(path, message)

	def __get_permissions(self, permissions):
		raise NotSupportedError
	
	def __chown(self, path, owner, group, retry):
		
		raise NotSupportedError
		
	def __chown_list(self, list, owner, group, retry):
		if list is not None:
			for file in list:
				self.__chown(file.get_path(), owner, group, retry)
				self.__chown_list(file.get_childs(), owner, group, retry)
	
	def chown(self, path, owner, group, excludes = None, contents_only = False, recursive = False, retry = 1):
		'''
		changing the ownership of file
		
		@param path: file path
		@param owner: the target owner id of the file 
		@param group: the target group id of the file
		@param excludes: list of the excluded file from the operation
		@param contents_only: if True the contents of the file only will be changed not the file itself
		@param recursive: if True the operation will be done recursively 
		@param retry: the number of retries on function failure
		
		@raise InvalidParameterError: If the required argument(s) are not specified.
		@raise FileNotExistError: if the path is not exist
		@raise FtpChownError: If the ownership can not be changed
		'''
		

		if not Validator.validate_non_empty_string(path):
			raise InvalidParameterError("path", "path can not be None or empty string")

		if not Validator.validate_integer(owner):
			raise InvalidParameterError("owner", "owner can not be None or empty string")

		if not Validator.validate_integer(group):
			raise InvalidParameterError("group", "group can not be None or empty string")

		try:
			path = self.append_to_root(path)
			if not self.is_exists(path):
				raise FileNotExistsError, path
			
			excluded = False
			path_type = self.get_type(path)
			if excludes is not None:
				if excludes.match(path, self.get_platform().basename(path), path_type):
					excluded = True
			if not contents_only and not excluded:
				self.__chown(path, owner, group, retry)
				
			if recursive and path_type is FileObject.DIRECTORY:
				children = self.list(path, excludes,  True, retry)
				self.__chown_list(child.get_path(), owner, group, retry)
		except Exception, e:
			raise FileChownError(path, str(e))

	
	def is_exists(self, path):
		'''
		check file exists or not
		
		@param file: path of the file
		
		@rtype: boolean
		@type exists:  True if exists else False
		'''
		path = self.append_to_root(path)
		try:
			self.__get_last_modified_time(path)
			return True
		except Exception, e:
			message = str(e)
			if message.find('No such file') > 0:
				return False
			if message.find('not a plain file') > 0:
				return True
			else:
				raise

	def disconnect(self, retry = 1):
		'''
		Disconnect to the ftp server and set the __ftp_client to None
		
		@raise FtpDisconnectionError: If any failure occurred while disconnecting with the server		
		'''
		
		raise NotSupportedError() 
