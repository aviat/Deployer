#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *
from thedeployer.packages.compression.decompress import *

class DecompressCommand(Command):

	"""@__from: The path of the file or directory to decompress."""
	"""@__to: The destination directory or file to decompress to."""
	"""@__replace: Whether to replace existing files or not."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, _from, to, replace = False, retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param _from: The path of the file or directory to decompress.
		@param to: The destination directory or file to decompress to.
		@param replace: Whether to replace existing files or not.
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__from = _from
		self.__to = to
		self.__replace = replace
		self.__retry = retry
		
		super(DecompressCommand, self).__init__(project, source, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a DecompressCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "contents_only", "recursive", "create_dirs", "replace" and "retry".

		@return: An instance of DecompressCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"replace": False, "retry": 1},
			{"source": "variable_name", "destination": "variable_name", "from": "non_empty_string", "to": "non_empty_string", "replace": "boolean", "retry": "integer"}
			)
		
		return DecompressCommand(project, parameters["source"], parameters["destination"], parameters["from"], parameters["to"], parameters["replace"], parameters["retry"])

	def execute_local_to_local(self, project):
		"""
		Copies a file on the local server to another local location.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("Decompress \"" + self.__from + "\" to \"" + self.__to + "\"")
				
		return Decompress.decompress(self.__from, self.__to, self.__replace, self.__retry)
