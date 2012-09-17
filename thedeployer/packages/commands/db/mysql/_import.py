#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import Command
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.project import Project

from thedeployer.packages.clients.mysqlclient import MysqlClient

class DbMysqlImportCommand(Command):

	"""
	Import from a file to a MySQL server.
	Uses the mysqlimport binary from the MySQL client distribution.
	"""

	"""@__from: The file to import from."""
	"""@__to: The name of the database to import to."""
	"""@__options: The name of a Dictionary of options."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, _from, to, options = "", retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param _from: The file to import from.
		@param to: The name of the database to import to.
		@param options: The name of a Dictionary of options.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		local_server = project.get_server(source)
		_from = local_server.to_absolute(_from)

		self.__from = _from
		self.__to = to
		self.__options = options
		self.__retry = retry

		super(DbMysqlImportCommand, self).__init__(project, source, destination)
		self.accept_dictionary(0, 1, [options])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a DbMysqlImportCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "options" and "retry".

		@return: An instance of DbMysqlImportCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"options": "", "retry": 1},
			{
				"source": "variable_name", "destination": "variable_name", "from": "non_empty_string",
				"to": "non_empty_string", "options": "variable_name", "retry": "integer"
			}
		)

		return DbMysqlImportCommand(
			project, parameters["source"], parameters["destination"], parameters["from"], parameters["to"],
			parameters["options"], parameters["retry"]
		)

	def execute_local_to_remote(self, project):
		"""
		Imports to a MySQL server from one or more local files.
		All MySQL servers are considered remote, whether they are installed on the same machine or not.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Importing to MySQL server "%s"' % (self.destination))

		options = {}
		if 0 != len(self.__options):
			options = self.get_dictionary(self.__options)

		mysql_server = project.get_server(self.destination)
		mysql_server._import(self.__from, self.__to, options, self.__retry)

	def execute_remote_to_remote(self, project):
		"""
		Dumps from a MySQL server to a remote file.
		All MySQL servers are considered remote, whether they are installed on the same machine or not.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Dumping from MySQL server to file "%s" at "%s"' % (self.__to, self.destination))
