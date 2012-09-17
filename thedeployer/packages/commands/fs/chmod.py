#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class ChmodCommand(Command):

	"""@__path: The path of the file or directory to chmod."""
	"""@__permissions: new mode permissions"""
	"""@__excludes: the files to be excluded"""
	"""@__contents_only: If a directory, whether to copy the directory itself or only its contents."""
	"""@__recursive: If a directory, whether to copy recursively or not."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, destination, path, permissions, excludes = None, contents_only = False, recursive = False, retry = 1):
		"""
		Constructor for the class.

		@param destination: The destination server that the command will execute on.
		@param path: The path of the file or directory to chmod.
		@param permissions: new mode permissions
		@param excludes: list of files will be excluded
		@param contents_only: If a directory, whether to chmod the directory itself or only its contents.
		@param recursive: If a directory, whether to chmod recursively or not.
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__path = path
		self.__permissions = permissions
		self.__excludes = excludes
		self.__contents_only = contents_only
		self.__recursive = recursive
		self.__retry = retry
		
		super(ChmodCommand, self).__init__(project, None, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a ChmodCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "destination", "path" and "permissions".
			Optional keys are "excludes", "contents_only", "recursive", and "retry".

		@return: An instance of ChmodCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["destination", "path", "permissions"],
			{"excludes": None, "contents_only": False, "recursive": False, "retry": 1},
			{"destination": "variable_name", "path": "non_empty_string", "permissions": "string", "excludes":"variable_name", "contents_only": "boolean", "recursive": "boolean", "retry": "integer"}
			)

		return ChmodCommand(project, parameters["destination"], parameters["path"], parameters["permissions"], parameters["excludes"], parameters["contents_only"], parameters["recursive"], parameters["retry"])

	def execute_local(self, project):
		"""
		Changing mode of a file on the local server.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Changing mode of "%s"' % (self.__path))
		
		local_server = project.get_server(self.destination)
		excludes_fileset = self.get_fileset(self.__excludes)
		return local_server.chmod(self.__path, self.__permissions , excludes_fileset, self.__contents_only, self.__recursive, self.__retry)
	