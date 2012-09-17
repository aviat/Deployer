#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import Command
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.project import Project

from thedeployer.packages.clients.mysqlclient import MysqlClient

class DbDropCommand(Command):

	"""
	Drop a new database.
	"""

	"""@__name: The name of the database to create."""
	"""@__if_exists: Only drop the database if it exists."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, destination, name, if_exists = True, retry = 1):
		"""
		Constructor for the class.

		@param project: The project this command belongs to.
		@param destination: The destination server that the command will execute on.
		@param name: The name of the database to create.
		@param if_exists: Only drop the database if it exists.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__name = name
		self.__if_exists = if_exists
		self.__retry = retry

		super(DbDropCommand, self).__init__(project, None, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Drops an instance of a DbDropCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "destination" and "name".
			Optional keys are "if_exists" and "retry".

		@return: An instance of DbDropCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["destination", "name"],
			{"if_exists": True, "retry": 1},
			{"destination": "variable_name", "name": "non_empty_string", "if_exists": "boolean", "retry": "integer"}
			)

		return DbDropCommand(project, parameters["destination"], parameters["name"], parameters["if_exists"], parameters["retry"])

	def execute_remote(self, project):
		"""
		Drop a new database.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Dropping database "%s" on "%s"' % (self.__name, self.destination))

		mysql_server = project.get_server(self.destination)
		mysql_server.drop_db(self.__name, self.__if_exists, self.__retry)
