#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class ExecuteCommand(Command):

	"""@__command: The command to execute."""
	"""@__retry: The number of times to retry execution on error"""

	def __init__(self, project, destination, command, retry = 1):
		"""
		Constructor for the class.

		@param destination: The destination server that the command will execute on.
		@param command: The string of the command to execute.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__command = command
		self.__retry = retry

		super(ExecuteCommand, self).__init__(project, None, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of an ExecuteCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "command" and "destination".
			Optional keys are "retry".

		@return: An instance of ExecuteCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["command", "destination"],
			{"retry": 1},
			{"command": "non_empty_string", "destination": "variable_name", "retry": "integer"}
			)

		return ExecuteCommand(project, parameters["destination"], parameters["command"], parameters["retry"])

	def execute_local(self, project):
		"""
		Executes a system command on the host server.

		@return: XXXXXXXXXXX.
		"""

		AppLogger.info("Executing command \"" + self.__command + "\" on the local server.")

	def execute_remote(self, project):
		"""
		Executes a system command on a remote server.

		@return: XXXXXXXXXXX.
		"""

		AppLogger.info("Executing command \"" + self.__command + "\" on the remote server \"" + self.destination + "\".")
