#
# Copyright (c) 2008 vimov
#

'''
Abstract class that represents a version control system.
'''

class VersionControlSystemClient(object):

	"""@repository_path: path of the root of the repository."""
	"""@username: user name to access the subversion (if it was authenticated)."""
	"""@password: password to access the subversion (if it was authenticated)."""

	def __init__(self, repository_path, username, password):
		self.repository_path = repository_path
		self.username = username
		self.password = password

	def checkout(self, local_path, path = "/", replace = False, retry = 1):
		raise NotImplementedError

	def get_file(self, local_path, file_path, replace = False, retry = 1):
		raise NotImplementedError

	def checkout_by_revision(self, revision, local_path, path = '/', replace = False, retry = 1):
		raise NotImplementedError

	def checkout_by_tag(self, tag, replace = False, retry = 1):
		raise NotImplementedError

	def get_file_list(self, path, recursive = False, retry = 1):
		raise NotImplementedError

	def set_user(self, username, password):

		self.username = username;
		self.password = password;

		return True

	def get_repository_path(self):
		return self.repository_path