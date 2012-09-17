#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.project import *

class DbMysqlDumpCommand(Command):

	"""
	Dump to a file from a MySQL server.
	Uses the mysqlump binary from the MySQL client distribution.
	"""

	"""@__name: The path of the file to dump to."""
	"""@__databases: The name of a List. If not specified, all databases are dumped."""
	"""@__tables: The name of a List. If not specified, all tables are dumped."""
	"""@__options: The name of a Dictionary of options."""
	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, to, databases = "", tables = "", options = "", retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param to: The path of the file to dump to.
		@param databases: The name of a List. If not specified, all databases are dumped.
		@param tables: The name of a List. If not specified, all tables are dumped.
		@param options: The name of a Dictionary of options.
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		local_server = project.get_server(destination)
		to = local_server.to_absolute(to)

		self.__to = to
		self.__databases = databases
		self.__tables = tables
		self.__options = options
		self.__retry = retry

		super(DbMysqlDumpCommand, self).__init__(project, source, destination)
		self.accept_list(0, 2, [databases, tables])
		self.accept_dictionary(0, 1, [options])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a DbMysqlDumpCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination" and "to".
			Optional keys are "databases", "tables", "options" and "retry".

		@return: An instance of DbMysqlDumpCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "to"],
			{"databases": "", "tables": "", "options": "", "retry": 1},
			{
				"source": "variable_name", "destination": "variable_name", "to": "string",
				"databases": "variable_name", "tables": "variable_name",
				"options": "variable_name", "retry": "integer"
			}
		)

		return DbMysqlDumpCommand(
			project, parameters["source"], parameters["destination"], parameters["to"],
			parameters["databases"], parameters["tables"], parameters["options"], parameters["retry"]
		)

	def execute_remote_to_local(self, project):
		"""
		Dumps from a MySQL server to a local file.
		All MySQL servers are considered remote, whether they are installed on the same machine or not.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Dumping from MySQL server "%s" to file "%s"' % (self.source, self.__to))

		databases = []
		if 0 != len(self.__databases):
			databases = self.get_list(self.__databases)

		tables = []
		if 0 != len(self.__tables):
			tables = self.get_list(self.__tables)

		options = {}
		if 0 != len(self.__options):
			options = self.get_dictionary(self.__options)

		mysql_server = project.get_server(self.source)
		mysql_server.dump(self.__to, databases, tables, options, self.__retry)

	def execute_remote_to_remote(self, project):
		"""
		Dumps from a MySQL server to a remote file.
		All MySQL servers are considered remote, whether they are installed on the same machine or not.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Dumping from MySQL server to file "%s" at "%s"' % (self.__to, self.destination))
