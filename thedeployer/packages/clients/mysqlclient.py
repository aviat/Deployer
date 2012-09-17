#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.clients.sqlclient import SqlClient
from thedeployer.packages.application import Application

import MySQLdb
import _mysql

import warnings
warnings.filterwarnings("ignore", "Unknown table.*")
warnings.filterwarnings("ignore", ".*; database exists")
warnings.filterwarnings("ignore", ".*; database does")

class MysqlClient(SqlClient):

	def __init__(self, host, port, username = "", password = ""):
		"""
		"""

		if not Validator.validate_non_empty_string(host):
			raise InvalidParameterError("host", "Must be non-empty String")
		if not Validator.validate_integer(port):
			raise InvalidParameterError("port", "Must be an integer value")
		if not Validator.validate_string(username):
			raise InvalidParameterError("username", "Must be a string value")
		if not Validator.validate_string(password):
			raise InvalidParameterError("password", "Must be a string value")

		super(SqlClient, self).__init__()

		self.__host = host
		self.__port = port
		self.__username = username
		self.__password = password
		self.__platform = Platform.get_current()

	def create_db(self, name, character_set = "", collate = "", if_not_exists = True, retry = 1):
		"""
		creates new database using data base name, character_set, and collate

		@param name: name of database to be created
		@param character_set: character set of the database
		@param collate: the collation of the database
		@param if_not_exist: only creates the database if it does not exist
		@param retry: The number of times to retry execution on error

		@rtype: bool
		@return: True on success

		@raise InvalidParameterError:  If method parameters are invalid in type.
		@raise DbCreateError: if failed to create the database.
		"""

		if False == Validator.validate_non_empty_string(name):
			raise InvalidParameterError('name', 'name should be a non-empty string')
		if False == Validator.validate_string(character_set):
			raise InvalidParameterError('character_set', 'character_set should be a string')
		if False == Validator.validate_string(collate):
			raise InvalidParameterError('collate', 'collate should be a string')
		if False == Validator.validate_boolean(if_not_exists):
			raise InvalidParameterError('if_not_exist', 'should be a boolean')

		while True:
			try:
				statement = "CREATE DATABASE %s %s"
				conn = MySQLdb.connect(host = self.__host, user = self.__username, passwd = self.__password, port = self.__port)
				transaction = conn.cursor()

				if True == if_not_exists:
					statement = statement % ("IF NOT EXISTS", name)
				else:
					statement = statement % ("", name)

				if 0 != len(character_set):
					statement = statement + " CHARACTER SET = %s " % (character_set)
				if 0 != len(collate):
					statement = statement + " COLLATE = %s " % (collate)

				AppLogger.debug('Executing SQL command "%s"' % (statement))
				transaction.execute(statement)

				return True

			except Exception, e:

				retry = retry - 1
				if 0 == retry:
					raise DbCreateError, str(e)

	def drop_db(self, name, if_exists = True, retry = 1):
		"""
		drops a database.

		@param name: name of database to be dropped
		@param if_exists: only drop the database if it did not exist
		@param retry: The number of times to retry execution on error

		@rtype: bool
		@return: True on success

		@raise InvalidParameterError:  If method parameters are invalid in type.
		@raise DbDropError: if method fails in creating database or connecting to database
		"""

		if False == Validator.validate_non_empty_string(name):
			raise InvalidParameterError('name', 'name should be a non-empty string')
		if False == Validator.validate_boolean(if_exists):
			raise InvalidParameterError('if_exists', 'should be a boolean')

		while True:
			try:
				statement = "DROP DATABASE %s %s"
				conn = MySQLdb.connect(host = self.__host, user = self.__username, passwd = self.__password, port = self.__port)
				transaction = conn.cursor()

				if True == if_exists:
					statement = statement % ("IF EXISTS", name)
				else:
					statement = statement % ("", name)

				AppLogger.debug('Executing SQL command "%s"' % (statement))
				transaction.execute(statement)

				return True

			except Exception, e:

				retry = retry - 1
				if 0 == retry:
					raise DbDropError, str(e)

	def select(self, query, retry = 1):
		pass

	def execute_sql(self, statements, database, transaction = False):
		"""
		Executes a sequence of SQL statements.

		@param statements: list of statements to be executed.
		@param database: the name of the database to run the statements.
		@param transaction: if it is True, statements will be executed as a single transaction.

		@rtype: bool
		@return: True on success

		@raise InvalidParameterError:  If method parameters are invalid in type.
		@raise DbStatementError: if method fails in executing statements or connecting to database.
		"""

		if statements.__class__ != list:
			raise InvalidParameterError('statements', 'statements should be a list of statements')
		if False == Validator.validate_non_empty_string(database):
			raise InvalidParameterError('database', 'must be a non empty string')
		if False == Validator.validate_boolean(transaction):
			raise InvalidParameterError('transaction', 'must be a boolean')

		while True:

			try:
				cursor = None
				conn = MySQLdb.connect(host = self.__host, user = self.__username, passwd = self.__password, port = self.__port, db = database)
				cursor = conn.cursor()

				for statement in statements:
					cursor.execute(statement)
					if not transaction:
						conn.commit()

				cursor.close()
				conn.commit()
				conn.close()

				return True

			except Exception, e:

				if cursor:
					cursor.close()
					conn.rollback()
					conn.close()

				raise DbStatementError, str(e)

	def dump(self, target_file, databases = [], tables = [], options = {}, retry = 1):
		"""
		Uses mysqldump to backup one or more databases to a file. The function prepares the mysqldump command to
		execute by using the server information (host, port, username, password), adding the databases or tables
		or the respective flags the describes them, and adding the options with the exception of the options to
		ignore (the reason some options are ignored is so that they do not conflict with their implicit usage.

		Documentation of mysqldump is at http://dev.mysql.com/doc/refman/5.0/en/mysqldump.html.

		Note: The function expects the options to be specified without the initial - or --, but internally, it
		anyway trims any leading dashes from the options.

		@param target_file: The path of the file to write the backup to.
		@param databases: An array of database names. If empty, all databases are backed up.
		@param tables: An array of table names. If empty, backs up all tables. Not used if databases is empty
			or more than one database was specified.
		@param options: An array of options, as defined by mysqldump. Example options are compact and
			add-drop-database. The following option are ignored help, ?, all-databases, A,
			databases, B, debug, #, debug-info, host, h, port, user, tables, verbose, v,
			version, V, password, p, pipe, W

		@return: True on success.

		@raise SqlBackupError: If it failed to perform the backup for whatever reason.
		"""

		while True:

			try:

				if not Validator.validate_non_empty_string(target_file):
					raise InvalidParameterError("target_file", "Must be non-empty String")
				if databases.__class__ != list:
					raise InvalidParameterError("databases", "Must be an instance of list")
				if tables.__class__ != list:
					raise InvalidParameterError("tables", "Must be an instance of list")
				if options.__class__ != dict:
					raise InvalidParameterError("options", "Must be an instance of dict")

				command = Application.get_option("bin", "mysqldump") + " "

				ignored = {"--help": "", "-?": "", "--all-databases": "", "-A": "", "--databases": "", "-B": "", "--debug": "", "-#":" ", "--debug-info": "", "--host": "", "-h": "", "--port": "", "-user": "", "--tables": "", "--verbose": "", "-v": "", "--version": "", "-V": "", "--password": "", "-p": "", "--pipe": "", "-W": ""}

				for option in options:
					if not ignored.has_key(option):
						command += option
						if "" != options[option]:
							command += "=" + options[option]
						command += " "

				command += "--host=%s " % (self.__host)
				command += "--port=%s " % (self.__port)

				if "" != self.__username:
					command += "--user=%s " % (self.__username)
				if "" != self.__password:
					command += "--password=%s " % (self.__password)

				if databases:
					if len(databases) == 1:
						command += databases[0] + " "
						if tables:
							command += "--tables "
							for table in tables:
								command += table + " "

					else:
						command += "--databases "
						for database in databases:
							command += database + " "
				else:
					command += "--all-databases "

				command += "> %s 2> /dev/null" % (target_file)

				result = os.system(command)
				if 0 != result:
					raise SqlDumpError()

				return True

			except Exception:

				retry -= 1

				if 0 == retry:
					raise

	def _import(self, source_file, database, options = {}, retry = 1):
		"""
		Uses mysqlimport to import a SQL file into the database. The function prepares the mysqlimport command to
		execute by using the server information (host, port, username, password), adding the databases or tables
		or the respective flags the describes them, and adding the options with the exception of the options to
		ignore (the reason some options are ignored is so that they do not conflict with their implicit usage.

		Documentation of mysqlimport is at http://dev.mysql.com/doc/refman/5.0/en/mysqlimport.html.

		Note: The function expects the options to be specified without the initial - or --, but internally, it
		anyway trims any leading dashes from the options.

		@param source_file: The path of the file to read the data from.
		@param database: The name of the database to apply the SQL commands to.
		@param options: An array of options, as defined by mysqlimport. Example options are compact and
			add-drop-database. The following option are ignored help, ?, databases, B, debug, #, debug-info,
			host, h, port, user, tables, verbose, -v, version, V, password, p, pipe, W, local

		@return: True on success.

		@raise SqlImportError: If it failed to perform the backup for whatever reason.
		"""

		while True:

			try:

				if not Validator.validate_non_empty_string(database):
					raise InvalidParameterError("database", "Must be non-empty string")
				if not Validator.validate_non_empty_string(source_file):
					raise InvalidParameterError("source_file", "Must be non-empty string")
				if options.__class__ != dict:
					raise InvalidParameterError("options", "Must be a instance of dict")

				command = Application.get_option("bin", "mysql") + " "

				ignored = {"--help": "", "-?": "", "--debug": "", "-#":" ", "--debug-info": "", "--host": "", "-h": "", "--port": "", "-user": "", "--tables": "", "--verbose": "", "-v": "", "--version": "", "-V": "", "--password": "", "-p": "", "--pipe": "", "-W": "", "local": ""}

				for option in options:
					if not ignored.has_key(option):
						command += option
						if "" != options[option]:
							command += "=" + options[option]
						command += " "

				command += "--host=%s " % (self.__host)
				command += "--port=%s " % (self.__port)

				if "" != self.__username:
					command += "--user=%s " % (self.__username)
				if "" != self.__password:
					command += "--password=%s " % (self.__password)

				command += " %s < %s 2> /dev/null" % (database, source_file)

				result = os.system(command)
				if 0 != result:
					raise SqlImportError()

				return True

			except Exception:

				retry -= 1

				if 0 == retry:
					raise

	def get_platform(self):
		return self.__platform
