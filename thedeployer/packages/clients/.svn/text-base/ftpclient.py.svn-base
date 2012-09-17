#
# Copyright (c) 2008 vimov
#

import datetime
import ftplib
import os
import sys

from thedeployer.packages.customexceptions import *
from thedeployer.packages.clients.ftpbase import FtpBase
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.platform.file import FileObject

class FtpClient(FtpBase):
	
	"""@param __blocksize: used for block buffering while store and retrieve binary data from the server""" 
	
	def __init__(self, platform, host, username = "", password = "", port = 21, root = ""):
		"""
		constructor for the class
		"""

		self.__blocksize = 1024*256

		FtpBase.__init__(self, platform, host, username, password, port, root)
		self.connect()

	def connect(self):
		"""
		connect with the server and add instance to the local variable __ftp_client
		
		@raise FtpConnectionError: if failed to connect with the server 
		"""
		try:
			self.set_client(ftplib.FTP())
			self.get_client().connect(self.host, self.port)
			self.get_client().login(self.username, self.password)

		except Exception, e:
			raise FtpConnectionError, str(e)

	def _FtpBase__put_file(self, source, destination, replace, retry):
		"""
		upload file from the source into the destination with name included in the destination
		"""

		while retry > 0:
			retry = retry - 1
			exist = self.is_exists(destination)
			try:
				if exist and not replace:
					retry = 0
					raise FileExistsError('File ' + destination + ' exists on server')
				filehandler = open(source, "rb")
				self.get_client().storbinary("STOR " + destination , filehandler, self.__blocksize)
				filehandler.close()
				return 
			except Exception, e:
				if retry == 0 :
					raise

	def _FtpBase__delete_file(self, path, retry):
		"""
		delete file from the server
		""" 
		while retry > 0:
			retry = retry - 1         
			try:
				self.get_client().delete(path)
				return 
			except Exception, e:
				if retry == 0:
					raise

	def _FtpBase__delete_empty_dir(self, path, retry):
		"""
		delete empty directory from the server
		Note:
			if the directory is not empty, it can not be deleted
		"""
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().rmd(path);
				return 
			except Exception, e:
				if retry == 0:
					raise
 
	def _FtpBase__get_file(self, source, destination, replace, retry):
		"""
		get file from the source(server) into destination
		Note:
			this function does not called directly, it called by get()
		"""
		while retry > 0:
			retry = retry - 1
			try:
				if os.path.exists(destination) and not replace:
					retry = 0
					raise FileExistsError, destination
				f = open(destination, 'a+w')
				self.get_client().retrbinary("RETR " + source, f.write, self.__blocksize)
				f.close()
				return 
			except Exception, e:
				if retry == 0:
					raise

	def _FtpBase__get_dir_list(self, path, retry):
		"""
		return list of strings represents the long list format of files

		there are a problem in list if we write 'LIST New Folder' it will consider the file name is 'New' only, 
		and will neglect the other file name 'Folder' so first we must change the the current directory to 
		the New Folder the list the current directory 
		"""
		res = FtpString()
		files_list = []

		while retry > 0:
			retry = retry - 1
			try:
				cwd = self.get_cwd()
				self.chdir(path)
				self.get_client().retrbinary("LIST", res.append, self.__blocksize)
				self.chdir(cwd)
				if len(res) > 0 :
					str_obj = res.get_str()
					files_list =  str_obj.splitlines()
				return  files_list
			except Exception, e:
				if retry == 0:
					raise

	def _FtpBase__chdir(self, path):
		self.get_client().cwd(path)

	def cdup(self):
		'''
		go to the parent directory
		
		@raise FtpCommandError: If the server can not go the parent directory 
		'''
		
		try:
			self.get_client().sendcmd("CDUP")
		except Exception, e:
			raise FtpCommandError('can not go to the parent directory', str(e)) 
	
	def get_cwd(self):
		'''
		get the current working directory
		
		@return: the current working directory
		
		@raise FtpCommandError: If the function fails to get the current working directory 
		'''
		try:
			return self.get_client().pwd()
		except Exception, e:
			raise FtpCommandError('can not get the current working directory', str(e))

	def get_type(self, path):
		"""
		check the type of the path is directory or file assuming the if it is not a file it will be a directory
		
		@return: type of the path
		@rtype: FileObject.FILE or FileObject.DIRECTORY
		
		@raise FileNotExistsError:	if the path is not found in the server
		@raise others: if any other exception occurred
		"""
		try:
			path = self.append_to_root(path)
			self._FtpBase__get_last_modified_time(path)
			return FileObject.FILE
		except Exception, e:
			message  = str(e)
			if message.find('regular files') > 0 or message.find("not a plain file") > 0:
				return FileObject.DIRECTORY
			elif message.find("No such file") > 0:
				raise FileNotExistsError, path
			else:
				raise

	def _FtpBase__get_permissions(self, permissions):
		return FileObject.convert_permissions(permissions, self.get_platform(), convert_type = FileObject.PERMISSIONS_AS_INT)
	
	def _FtpBase__mkdir(self, path, mode, retry):
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().mkd(path)
				self.chmod(path, str(mode))
				return 
			except Exception, e:
				if retry == 0:
					raise	

	def _FtpBase__get_last_modified_time(self, path):

		res = self.get_client().sendcmd("MDTM " + path)
		lmd = res.split()[1]
		return (lmd[0:4], lmd[4:6], lmd[6:8], lmd[8:10], lmd[10:12], lmd[12:14])

	def _FtpBase__rename(self, source, destination):
		self.get_client().rename(source, destination)

	def _FtpBase__chmod(self, path, mode, retry):
		"""
		in the ftplib there are not direct method called chmod so the site command used fot that
		"""
		while retry > 0:
			retry = retry - 1
			try:
				self.__site('chmod', str(mode), path)
				return 
			except Exception, e:
				if retry == 0:
					raise
		
	def __site(self, command, *args):
		'''
		Perform a SITE command with the given arguments.
		The following only the site commands that supports only with the python module ftplib
			ALIAS
			CHMOD
			IDLE
			UTIME
		
		Note: Parameter checks made by the caller function, and you can not call this method directly
			
		@raise FtpCommandError: if the site command fails 
		'''
		args = " ".join(('SITE', command.upper()) + args)
		try:
			self.get_client().sendcmd(args)
		except Exception, e:
			raise

	def disconnect(self, retry = 1):
		'''
		Disconnect to the ftp server and set the __ftp_client to None
		
		@raise FtpDisconnectionError: If any failure occurred while disconnecting with the server		
		'''
		
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().quit()
				self.set_client(None)
				return 
			except Exception, e:
				pass
		raise FtpDisconnectionError('can not disconnect to the ftp server', str(e))

	
	def set_block_size(self, blocksize):
		'''
		set block size of the buffer wile sending and receiving any binary data to the server
		
		@param blocksize: size of the buffer used in sending and receiving data from the server 
		'''
		self.__blocksize = blocksize

class FtpString:
	'''
	this class representing String Object used in the list_dir function
	the list_dir function use the function ftplib.retrbinary(cmd, callback, blocksize)
	the callback function called according to the size of returned binary data and the buffer block size
	
	this calss instade of using member function to the class ftp and local variable
	local variable case some problems on using one innstance of the ftp class (singletone) 
	but by using this FtpString Class there are an Object will be create every function call of list_dir() 
	'''

	"""	@param __str: String local variable"""
	
	def __init__(self):
		self.__str = ''
	
	def append(self, str):
		'''
		append the incomming String to the local variable
		
		@param str: string to append
		
		@raise InvalidParameterError: If the required argument(s) are not specified. 
		'''

		if str is None:
			raise InvalidParameterError("str", "str can not be None")
		
		self.__str = self.__str + str
		
	def get_str(self):
		'''
		@return: the local variable string
		'''
		return self.__str
	
	def __len__(self):
		return len(self.__str)
	