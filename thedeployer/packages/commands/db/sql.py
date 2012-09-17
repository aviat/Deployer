#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import Command
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.project import Project

from thedeployer.packages.clients.mysqlclient import MysqlClient

class DbSqlCommand(Command):

	"""
	Execute one or more SQL statements.
	"""

	"""@__statements: list of statements to be executed."""
	"""@__database: the name of the database to run the statements."""
	"""@__transaction: if it is True, statements will be executed as a single transaction."""

	def __init__(self, project, destination, statements, database, transaction = False):
		"""
		Constructor for the class.

		@param project: The project this command belongs to.
		@param destination: The destination server that the command will execute on.
		@param statements: list of statements to be executed.
		@param database: the name of the database to run the statements.
		@param transaction: if it is True, statements will be executed as a single transaction.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		self.__statements = statements
		self.__database = database
		self.__transaction = transaction

		super(DbSqlCommand, self).__init__(project, None, destination)
		self.accept_list(0, 1, [statements])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Drops an instance of a DbSqlCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "destination", "statements" and "database".
			Optional keys are "transaction".

		@return: An instance of DbSqlCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["destination", "statements", "database"],
			{"transaction": True},
			{"destination": "variable_name", "statements": "variable_name", "database": "non_empty_string", "transaction": "boolean"}
			)

		return DbSqlCommand(project, parameters["destination"], parameters["statements"], parameters["database"], parameters["transaction"])

	def execute_remote(self, project):
		"""
		Drop a new database.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		statements = []
		statements = self.get_list(self.__statements)

		AppLogger.info('Executing list of statements "%s" on database "%s" at "%s"' % (self.__statements, self.__database, self.destination))

		server = project.get_server(self.destination)
		server.execute_sql(statements, self.__database, self.__transaction)
