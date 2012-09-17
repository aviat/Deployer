#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class VcCheckoutCommand(Command):

	"""@__from: The path on repository."""
	"""@__to: The local path."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, _from, to, revision = 0, retry = 1):
		"""
		Constructor for the class.

		@param source: The id of subversion server.
		@param destination: The id of local server.
		@param _from: The path of the file or directory to copy.
		@param to: The destination directory or file to copy to.
		@param revision: revision number to checkout, 0 to checkout the last revision.
		@param retry: The number of times to retry execution on error.

		@raise InvalidParameterError: If the command is a 0-length string.
		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		local_server = project.get_server(destination)
		to = local_server.to_absolute(to)

		self.__from = _from
		self.__to = to
		self.__revision = revision
		self.__retry = retry

		super(VcCheckoutCommand, self).__init__(project, source, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a VcCheckoutCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "revision" and "retry".

		@return: An instance of VcCheckoutCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"revision": 0, "retry": 1},
			{
				"source": "variable_name", "destination": "variable_name", "from": "non_empty_string",
				"to": "non_empty_string", "revision": "integer", "retry": "integer"
			}
		)

		return VcCheckoutCommand(
			project, parameters["source"], parameters["destination"], parameters["from"],
			parameters["to"], parameters["revision"], parameters["retry"]
		)

	def execute_remote_to_local(self, project):
		"""
		Checkout a directory on the subversion server to local location.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		subversion_server = project.get_server(self.source)
		checkout_path = os.path.join(subversion_server.get_repository_path(), self.__from.lstrip("/"))

		AppLogger.info('Checking out "%s" to "%s".' % (checkout_path, self.__to))

		return subversion_server.checkout(self.__to, self.__from, self.__revision, self.__retry)
