#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import Command
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.project import Project

from thedeployer.packages.clients.mysqlclient import MysqlClient

class DbCreateCommand(Command):

	"""
	Create a new database.
	"""

	"""@__name: The name of the database to create."""
	"""@__character_set: The character set of the database."""
	"""@__collate: The collation of the database."""
	"""@__if_not_exists: Only create the database if it does not already exists."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, destination, name, character_set = "", collate = "", if_not_exists = True, retry = 1):
		"""
		Constructor for the class.

		@param project: The project this command belongs to.
		@param destination: The destination server that the command will execute on.
		@param name: The name of the database to create.
		@param character_set: The character set of the database.
		@param collate: The collation of the database.
		@param if_not_exists: Only create the database if it does not already exists.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__name = name
		self.__character_set = character_set
		self.__collate = collate
		self.__if_not_exists = if_not_exists
		self.__retry = retry

		super(DbCreateCommand, self).__init__(project, None, destination)

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a DbCreateCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "destination" and "name".
			Optional keys are "character_set", "collate", "if_not_exists" and "retry".

		@return: An instance of DbCreateCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["destination", "name"],
			{"character_set": "", "collate": "", "if_not_exists": True, "retry": 1},
			{"destination": "variable_name", "name": "non_empty_string", "character_set": "string", "collate": "string", "if_not_exists": "boolean", "retry": "integer"}
			)

		return DbCreateCommand(project, parameters["destination"], parameters["name"], parameters["character_set"], parameters["collate"], parameters["if_not_exists"], parameters["retry"])

	def execute_remote(self, project):
		"""
		Create a new database.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Creating database "%s" on "%s"' % (self.__name, self.destination))

		mysql_server = project.get_server(self.destination)
		mysql_server.create_db(self.__name, self.__character_set, self.__collate, self.__if_not_exists, self.__retry)
