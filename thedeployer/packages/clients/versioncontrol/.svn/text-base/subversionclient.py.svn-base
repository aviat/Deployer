#
# Copyright (c) 2008 vimov
#

import os
import pysvn
import shutil

from thedeployer.packages.customexceptions import *
from thedeployer.packages.clients.versioncontrol.versioncontrolsystemclient import VersionControlSystemClient
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.clients.localclient import LocalClient

class SubversionClient(VersionControlSystemClient):

	"""@__client: an instance of a pysvn client object."""

	def __init__(self, repository_path, username = '', password = ''):
		"""
		@param repository_path: path of the root of the repository
		@param username: user name to access the subversion (if it was authenticated)
		@param password: password to access the subversion (if it was authenticated)
		"""

		if not Validator.validate_non_empty_string(repository_path):
			raise InvalidParameterError("repository_path", "Must be a non-empty string")
		if not Validator.validate_string(username):
			raise InvalidParameterError("username", "Must be a string")
		if not Validator.validate_string(password):
			raise InvalidParameterError("password", "Must be a string")

		VersionControlSystemClient.__init__(self, repository_path, username, password)
		self.__client = pysvn.Client()

		if username and password:
			self.set_user(username, password)

		self.local_client = LocalClient()

	def checkout(self, local_path, path = "/", revision = 0, retry = 1):
		"""
		check out a directory from the subversion server that is spesified by path parameter

		@param local_path: local path on local machine where the directory will be checked out.
		@param path: path of directory on subversion servern that will be checked out.
		@param replace: if true replaces the existing local working diretory.
		@param revision: revision number to checkout, 0 to checkout the last revision.
		@param retry: number of retries before fail.

		@raise CheckOutError in case of failure
		"""

		if not Validator.validate_non_empty_string(local_path):
			raise InvalidParameterError("local_path", "Must be non-empty string")
		if not Validator.validate_string(path):
			raise InvalidParameterError("path", "Must be a string value")
		if not Validator.validate_integer(revision):
			raise InvalidParameterError("revision", "Must be an integer value")
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "Must be an integer value")

		checkout_path = os.path.join(self.repository_path, path.lstrip("/"))

		if os.path.exists(local_path):
			raise FileExistsError, "the path where you check out is already exists"

		while True:
			try:
				if 0 == revision:
					return self.__client.checkout(
						checkout_path,
						local_path,
						True,
					)
				else:
					return self.__client.checkout(
						checkout_path,
						local_path,
						True,
						pysvn.Revision(pysvn.opt_revision_kind.number, revision)
					)

			except Exception, e:

				retry -= 1
				if 0 == retry:
					raise CheckOutError(
						'Failed to checkout "%s" to "%s"."' % (checkout_path, local_path)
					)
				else:
					shutil.rmtree(local_path, True)

	def export(self, local_path, path = "/", revision = 0, retry = 1):
		"""
		export a directory from the subversion server that is spesified by path parameter

		@param local_path: local path on local machine where the directory will be checked out.
		@param path: path of directory on subversion servern that will be checked out.
		@param replace: if true replaces the existing local working diretory.
		@param revision: revision number to checkout, 0 to checkout the last revision.
		@param retry: number of retries before fail.

		@raise CheckOutError in case of failure
		"""

		if not Validator.validate_non_empty_string(local_path):
			raise InvalidParameterError("local_path", "Must be non-empty string")
		if not Validator.validate_string(path):
			raise InvalidParameterError("path", "Must be a string value")
		if not Validator.validate_integer(revision):
			raise InvalidParameterError("revision", "Must be an integer value")
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "Must be an integer value")

		export_path = os.path.join(self.repository_path, path.lstrip("/"))

		if os.path.exists(local_path):
			raise FileExistsError, "the path where you check out is already exists"

		while True:
			try:
				if 0 == revision:
					return self.__client.export(
						export_path,
						local_path,
						True,
					)
				else:
					return self.__client.export(
						export_path,
						local_path,
						True,
						pysvn.Revision(pysvn.opt_revision_kind.number, revision)
					)

			except Exception, e:

				retry -= 1
				if 0 == retry:
					raise CheckOutError(
						'Failed to export "%s" to "%s"."' % (export_path, local_path)
					)
				else:
					shutil.rmtree(local_path, True)

	def get_file(self, local_path, file_path, replace = False, retry = 1):
		"""
		get a file spesified by file path from the server

		@param local_path: local path on local machine where the directory will be checked out
		@param file_path: path of file on subversion  that will be got
		@param replace: if true replaces the existing local working diretory
		@param retry: number of retries before fail

		@raise GetFileError on failure
		"""

		if not Validator.validate_non_empty_string(local_path):
			raise InvalidParameterError("local_path", "Must be non-empty string")
		if not Validator.validate_non_empty_string(file_path):
			raise InvalidParameterError("file_path", "Must be non-empty string")
		if not Validator.validate_boolean(replace):
			raise InvalidParameterError("replace", "Must be a boolean value")
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "Must be an integer value")

		local_path = self.local_client.get_platform().trim_path(local_path)
		file_path = self.local_client.get_platform().trim_path(file_path)

		if os.path.exists(local_path):
			if os.path.isdir(local_path):
				base_name = self.local_client.get_platform().basename(file_path)
				local_path += self.local_client.get_platform().get_separator() + base_name

		while retry:
			retry -= 1
			try:
				file_str = self.__client.cat(self.repository_path + file_path)
			except:
				if retry == 0:
					raise GetFileError("repository path: ")

			try:
				if os.path.exists(local_path):
					if os.path.isfile(local_path):
						if replace:
							self.local_client.delete(local_path, None, False, True, retry)
						else:
							raise FileExistsError(local_path + " already exists")

				local_file = open(local_path, 'w')
				local_file.write(file_str)
				local_file.close()

			except Exception, e:
				if retry == 0:
					raise FileWriteError ()
			else:
				break

	def get_file_list(self, path, recursive = False, retry = 1):
		"""
		list file on subversion server given a  spesified path
		raise ListFileError on failure
		"""

		if not Validator.validate_string(path):
			raise InvalidParameterError("local_path", "Must be a string value")
		if not Validator.validate_boolean(recursive):
			raise InvalidParameterError("recursive", "Must be a boolean value")
		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "Must be an integer value")

		path = self.local_client.get_platform().trim_path(path)

		while retry:
			retry -= 1
			try:
				return self.__client.ls(self.repository_path + path, recurse = recursive)
			except Exception, e:
				if retry == 0:
					raise ListFileError("Repository path: " + self.repository_path + path, str(e))
			else:
				break

	def set_user(self, username, password):
		"""
		set usernames ans password for connection to subversion server
		return true on succes oan false on failure

		@param username:
		@param password:
		"""

		try:
			self.__client.set_default_username(username)
			self.__client.set_default_password(password)

			return True

		except:
			return False
