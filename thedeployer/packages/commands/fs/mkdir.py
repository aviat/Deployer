#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class MkdirCommand(Command):

	"""@__path: The path of directory to make."""
	"""@__mode: The mode of directory to make."""
	"""@__recursive: If a directory, whether to copy recursively or not."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, path, mode = 0777, recursive = False, retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param path: The path of the directory to mode.
		@param mode: the mode of the directory to make.
		@param recursive: create more than one level path
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__path = path
		self.__mode = mode
		self.__recursive = recursive
		self.__retry = retry
		
		super(MkdirCommand, self).__init__(project, source, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a MkdirCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "path".
			Optional keys are "mode", "recursive" and "retry".

		@return: An instance of MkdirCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "path"],
			{"mode": 0777, "recursive": False, "retry": 1},
			{"source": "variable_name", "destination": "variable_name", "path": "non_empty_string", "mode": "integer", "recursive": "boolean", "retry": "integer"}
			)

		return MkdirCommand(project, parameters["source"], parameters["destination"], parameters["path"], parameters["mode"], parameters["recursive"], parameters["retry"])

	def execute_local_to_local(self, project):
		"""
		Make a directory on the local server.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Making directory \"" + self.__path)
		
		local_server = project.get_server(self.source)
		excludes_fileset = self.get_fileset(self.__excludes)
		return local_server.mkdir(self.__path, self.__mode, self.__recursive, self.__retry)
 