#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class DeleteCommand(Command):

	"""@__path: The path of the file or directory to delete."""
	"""@__excludes: the files to be excluded"""
	"""@__contents_only: If a directory, whether to copy the directory itself or only its contents."""
	"""@__recursive: If a directory, whether to copy recursively or not."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, path, excludes = None, contents_only = False, recursive = False, retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param path: The path of the file or directory to delete.
		@param excludes: list of files will be excluded
		@param contents_only: If a directory, whether to delete the directory itself or only its contents.
		@param recursive: If a directory, whether to delete recursively or not.
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__path = path
		self.__excludes = excludes
		self.__contents_only = contents_only
		self.__recursive = recursive
		self.__retry = retry
		
		super(DeleteCommand, self).__init__(project, source, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a CopyCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination" and "path".
			Optional keys are "excludes", "contents_only", "recursive" and "retry".

		@return: An instance of DeleteCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "path"],
			{"excludes": None, "contents_only": False, "recursive": False, "retry": 1},
			{"source": "variable_name", "destination": "variable_name", "path": "non_empty_string", "excludes":"variable_name", "contents_only": "boolean", "recursive": "boolean", "retry": "integer"}
			)

		return DeleteCommand(project, parameters["source"], parameters["destination"], parameters["path"], parameters["excludes"], parameters["contents_only"], parameters["recursive"], parameters["retry"])

	def execute_local_to_local(self, project):
		"""
		Deletes a file on the local server

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Deleting \"" + self.__path)
		
		local_server = project.get_server(self.source)
		excludes_fileset = self.get_fileset(self.__excludes)
		return local_server.delete(self.__path, excludes_fileset, self.__contents_only, self.__recursive, self.__retry)
