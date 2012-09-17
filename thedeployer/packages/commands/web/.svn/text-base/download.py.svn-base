#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class DownloadCommand(Command):

	"""@__from: The URL of the file to download."""
	"""@__to: The destination to store the downloaded file to, can be a directory or a file path."""
	"""@__replace: If True, will replace the destination file if it exists."""
	"""@__retry: The number of times to retry execution on error.."""

	def __init__(self, project, destination, _from, to, replace = False, retry = 1):
		"""
		Constructor for the class.

		@param destination: The destination server that the command will execute on.
		@param _from: The URL of the file to download.
		@param to: The destination to store the downloaded file to, can be a directory or a file path.
		@param replace: If True, will replace the destination file if it exists.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__from = _from
		self.__to = to
		self.__replace = replace
		self.__retry = retry
		
		super(DownloadCommand, self).__init__(project, None, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a DownloadCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "destination", "from" and "to".
			Optional keys are "replace" and "retry".

		@return: An instance of DownloadCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["destination", "from", "to"],
			{"replace": False, "retry": 1},
			{"destination": "variable_name", "from": "non_empty_string", "to": "non_empty_string", "replace": "boolean", "retry": "integer"}
			)

		return DownloadCommand(project, parameters["destination"], parameters["from"], parameters["to"], parameters["replace"], parameters["retry"])

	def execute_remote(self, project):
		"""
		Downloads a file to a remote server

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Downloading \"" + self.__from + "\" to \"" + self.__to + "\" on server " + self.destination)
		return True

	def execute_local(self, project):
		"""
		Downloads a file to the local server.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Downloading \"" + self.__from + "\" to \"" + self.__to + "\"")
		return True
