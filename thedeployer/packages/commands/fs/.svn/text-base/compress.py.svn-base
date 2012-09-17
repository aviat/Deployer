#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *
from thedeployer.packages.compression.compress import *

class CompressCommand(Command):

	"""@__from: The path of the file or directory to compress."""
	"""@__to: The destination directory or file to compress to."""
	"""@__replace: Whether to replace existing files or not."""
	"""@__retry: The number of times to retry execution on error."""
	"""@__excludes: list of the excluded files from the compressed archive"""

	def __init__(self, project, source, destination, _from, to, excludes = None, replace = False, retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param exclusions: list of files will be excluded from the compressed archive
		@param _from: The path of the file or directory to compress.
		@param to: The destination directory or file to compress to.
		@param replace: Whether to replace existing files or not.
		@param retry: The number of times to retry execution on error.
		 

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""


		self.__from = _from
		self.__to = to
		self.__replace = replace
		self.__retry = retry
		self.__excludes = excludes
		
		super(CompressCommand, self).__init__(project, source, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a CompressCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "contents_only", "excludes", "recursive", "create_dirs", "replace" and "retry".

		@return: An instance of CompressCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"replace": False, "retry": 1, "excludes": None},
			{"source": "variable_name", "destination": "variable_name", "from": "non_empty_string", "to": "non_empty_string", "replace": "boolean", "retry": "integer", "exclusion":"variable_name"}
			)
		
		return CompressCommand(project, parameters["source"], parameters["destination"], parameters["from"], parameters["to"], parameters["excludes"], parameters["replace"], parameters["retry"])

	def execute_local_to_local(self, project):
		"""
		compress a file from the local server to another local location.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info("compress \"" + self.__from + "\" to \"" + self.__to + "\"")

		excludes_fileset = self.get_fileset(self.__excludes)
		return Compress.compress(self.__from, self.__to, excludes_fileset, self.__replace, self.__retry)
