#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class MoveCommand(Command):

	"""@__from: The path of the file or directory to copy."""
	"""@__to: The destination directory or file to copy to."""
	"""@__excludes: the files to be excluded"""
	"""@__contents_only: If a directory, whether to copy the directory itself or only its contents."""
	"""@__create_dirs: Whether to create non-existing directories in the specified parent destination."""
	"""@__replace: Whether to replace existing files or not."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, _from, to, excludes = None, contents_only = False, create_dirs = False, replace = False, retry = 1):
		"""
		Constructor for the class.

		@project: An instance of the project of this command.
		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param _from: The path of the file or directory to move.
		@param to: The destination directory or file to move to.
		@param excludes: list of files will be excluded.
		@param contents_only: If a directory, whether to move the directory itself or only its contents.
		@param create_dirs: Whether to create non-existing directories in the specified parent destination.
		@param replace: Whether to replace existing files or not.
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__from = _from
		self.__to = to
		self.__excludes = excludes
		self.__contents_only = contents_only
		self.__create_dirs = create_dirs
		self.__replace = replace
		self.__retry = retry
		
		super(MoveCommand, self).__init__(project, source, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a MoveCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "excludes", "contents_only", "create_dirs", "replace" and "retry".

		@return: An instance of MoveCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"contents_only": False, "create_dirs": False, "replace": False, "retry": 1, "excludes": None},
			{"source": "variable_name", "destination": "variable_name", "from": "non_empty_string", "to": "non_empty_string", "excludes":"variable_name", "contents_only": "boolean", "create_dirs": "boolean", "replace": "boolean", "retry": "integer"}
			)

		return MoveCommand(project, parameters["source"], parameters["destination"], parameters["from"], parameters["to"], parameters["excludes"], parameters["contents_only"], parameters["create_dirs"], parameters["replace"], parameters["retry"])

	def execute_local_to_local(self, project):
		"""
		Moves a file on the local server to another local location.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Moving \"" + self.__from + "\" to \"" + self.__to + "\"")
		
		local_server = project.get_server(self.source)
		excludes_fileset = self.get_fileset(self.__excludes)
		return local_server.move(self.__from, self.__to, excludes_fileset, self.__contents_only, self.__create_dirs, self.__replace, None,self.__retry)
	
	def execute_local_to_remote(self, project):
		"""
		Moves a file on the local server to a remote server.

		@return: XXXXXXXXXXX.
		"""
		print "PRINT REMOTE-LOCAL"
		
	def execute_remote_to_local(self, project):
		"""
		Moves a file on a remote server to the local server.

		@return: XXXXXXXXXXX.
		"""

		print "PRINT REMOTE-LOCAL"

	def execute_remote_to_remote(self, project):
		"""
		Moves a file on a remote server to another or the same remote server.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		if self.source == self.destination:
			AppLogger.info("Moving \"" + self.__from + "\" to \"" + self.__to + "\" on the same server \"" + self.source + "\"")

		#if self.source == self.destination:
			#remote_server = project.get_server(self.source)
			#return remote_server.move(self.__from, self.__to, self.__contents_only, self.__create_dirs, self.__replace, self.__retry)
