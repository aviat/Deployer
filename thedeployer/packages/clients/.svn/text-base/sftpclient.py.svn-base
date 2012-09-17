#
# Copyright (c) 2008 vimov
#

import datetime
import os
import sys
import time
sys.path.append('/home/leaf/workspace/thedeployer/src/thedeployer/libs/')
from thedeployer.libs import paramiko
from thedeployer.packages.customexceptions import *
from thedeployer.packages.clients.ftpbase import FtpBase
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.platform.file import FileObject
from thedeployer.packages.platform.file import octstr_to_int 

class SftpClient(FtpBase):

	def __init__(self, platform, host, username, password, port = 22, root = ""):

		super(SftpClient, self).__init__(platform, host, username, password, port, root)
#		self.connect()

	def connect(self):
		"""
		connect to the sftp server and setting the sftp client
		"""
		try:
			self.__transport = paramiko.Transport((self.host, self.port))
			self.__transport.connect(username = self.username, password = self.password)
			ftp = self.__transport.open_sftp_client()
			self.set_client(ftp)
		except Exception, e:
			raise FtpConnectionError, str(e) 

	def _FtpBase__put_file(self, source, destination, replace, retry):
		try:
			exist = self.is_exists(destination)
			if exist and not replace:
				retry = 0
				raise FileExistsError(destination)			
			self.get_client().put(source, destination)
			return 
		except FtpCommandError, e:
			while retry > 0:
				retry = retry - 1
				self._FtpBase__put_file(source, destination, replace, 0)
			raise 

	def _FtpBase__delete_file(self, path, retry):
		try:
			self.get_client().remove(path)
		except Exception, e:
			while retry > 0:
				retry = retry - 1
				self._FtpBase__delete_file(path, 0)
			raise

	def _FtpBase__delete_empty_dir(self, path, retry):
		try:
			self.get_client().rmdir(path)
		except Exception, e:
			while retry > 0:
				retry = retry - 1
				self._FtpBase__delete_empty_dir(path, 0)
			raise

	def _FtpBase__get_file(self, source, destination, replace, retry):
		"""
		get file from the source(server) into destination
		Note:
			this function does not called directly, it called by get()
		"""
		try:
			if os.path.exists(destination) and not replace:
				retry = 0
				raise FileExistsError, destination
			self.get_client().get(source, destination)
		except Exception, e:
			while retry > 0:
				retry = retry - 1 
				self._FtpBase__get_file(source, destination, 0)
			raise

	def _FtpBase__get_dir_list(self, path, retry):
		files_list = []
		while retry > 0:
			retry = retry - 1
			try:
				res = self.get_client().listdir_attr(path)
				for line in res:
					files_list.append(str(line))
				return files_list
			except Exception, e:
				if retry == 0:
					raise
		
	def _FtpBase__get_permissions(self, permissions):
		return FileObject.convert_permissions(permissions, self.get_platform(), convert_type = FileObject.PERMISSIONS_AS_OCT)

	def _FtpBase__chdir(self, path):
		self.get_client().chdir(path)

	def cdup(self):
		'''
		go to the parent directory
		
		@raise FtpCDUPError: If the server can not go the parent directory 
		'''
		
		try:
			self.chdir('.')
			path = self.get_cwd()
			self.chdir(self.get_platform().dirname(path))
		except Exception, e:
			raise FtpCommandError('can not go to the parent directory', str(e)) 
	
	def get_cwd(self):
		'''
		get the current working directory
		
		@rtype: String
		@return: the current working directory
		
		@raise FtpCommandError: If the function fails to get the current working directory 
		'''
		try:
			cwd = self.get_client().getcwd()
			if cwd is None:
				self.chdir('.')
				cwd =  self.get_client().getcwd()
			return cwd
		except Exception, e:
			raise FtpCommandError('can not get the current working directory', str(e))

	def get_type(self, path):
		"""
		check the type of the path is directory or file assuming the if it is not a file it will be a directory
		
		@return: type of the path
		@rtype: FileObject.FILE or FileObject.DIRECTORY
		"""
		try:
			path = self.append_to_root(path)	
			state =  self.get_client().lstat(path)
			state = str(state)
			if state.startswith("d"):
				return FileObject.DIRECTORY
			elif state.startswith("-"):
				return FileObject.FILE
		except Exception, e:
			message = str(e)
			if message.find("No such file") > 0:
				raise FileNotExistsError, path
			else:
				raise

	def _FtpBase__mkdir(self, path, mode, retry):
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().mkdir(path, mode)
				return 
			except Exception, e:
				if retry == 0:
					raise

	def _FtpBase__get_last_modified_time(self, path):
		attr_object = self.get_client().lstat(path)
		st_mtime = getattr(attr_object, 'st_mtime')
		return time.localtime(st_mtime)


	def _FtpBase__rename(self, source, destination):
		self.get_client().rename(source, destination)
		
	def _FtpBase__chmod(self, path, mode, retry):
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().chmod(path, mode)
				return 
			except Exception, e:
				if retry == 0:
					raise 

	def _FtpBase__chown(self, path, owner, group):
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().chown(path, owner, group)
				return 
			except Exception, e:
				if retry == 0:
					raise 
		
	def disconnect(self, retry = 1):
		'''
		Disconnect to the ftp server and set the __ftp_client to None
		
		@raise FtpDisconnectionError: If any failure occurred while disconnecting with the server		
		'''
		
		while retry > 0:
			retry = retry - 1
			try:
				self.get_client().close()
				self.set_client(None)
				self.__transport.close()
				return 
			except Exception, e:
				pass
		raise FtpDisconnectionError('can not disconnect to the ftp server', str(e))
