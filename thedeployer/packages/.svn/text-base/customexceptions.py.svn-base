#
# Copyright (c) 2008 vimov
#


from thedeployer.packages.logger import *

import logging
import os

class CustomError(Exception):

	"""The base class for custom exceptions"""

	"""@message: The error's description message."""

	def __init__(self, class_name, message):
		"""
		Constructor for the class.

		@param message: The message describing the error.
		"""

		super(Exception, self).__init__()
		self.message = message

		# write to the log file
		log_message = message
		AppLogger.error(log_message)

		# write the backtrace to another file
		AppBacktrace.write()

	def __str__(self):
		return self.message

	def get_message(self):
		"""
		Returns the error's description message

		@rtype String
		@return The error's description message
		"""

		return self.message


# general exceptions

class InvalidParameterError(CustomError):

	"""An error thrown when a function is called with invalid argument types/ranges."""

	def __init__(self, parameter, allowed_type):
		"""
		Constructor for the class.

		@param parameter: The name of the parameter that is invalid.
		@param allowed_type: The allowed type of the parameter.
		"""

		message = 'The parameter "%s" is inavlid. Allowed type is "%s".' % (parameter, allowed_type)
		super(InvalidParameterError, self).__init__(self.__class__.__name__, message)

class MissingParameterError(CustomError):

	"""An error thrown when a function is called with missing arguments."""

	def __init__(self, parameter):
		"""
		Constructor for the class.

		@param parameter: The name of the parameter that is missing.
		"""

		message = 'The parameter "%s" is missing.' % (parameter)
		super(MissingParameterError, self).__init__(self.__class__.__name__, message)

class MissingConfigurationParameterError(CustomError):

	"""An error thrown when a a configuration parameter is requested but is not defined."""

	def __init__(self, section, name):
		"""
		Constructor for the class.

		@param section: The name of the section that the parameter belongs to.
		@param name: The name of the parameter that is missing.
		"""

		message = 'The configuration parameter "%s" in section "%s" is missing.' % (name, section)
		super(MissingConfigurationParameterError, self).__init__(self.__class__.__name__, message)

class KeyNotFoundError(CustomError):

	"""An error thrown when a key is not found in an associative data structure, like a dictionary."""

	def __init__(self, key):
		"""
		Constructor for the class.

		@param parameter: The name of the parameter that is missing.
		"""

		message = 'The key "%s" was not found.' % (key)
		super(KeyNotFoundError, self).__init__(self.__class__.__name__, message)

class NotSupportedError(CustomError):

	"""
	An error thrown when a function is called or a feature is requested that is not supported.
	For example, a method that cannot be used in a child class that since it inherits the parent's methods, and
	thus throws this error in overriden functions for this unneeded behaviour.
	"""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		message = "The requested behaviour is not supported."
		super(NotSupportedError, self).__init__(self.__class__.__name__, message)

class FileReadError(CustomError):

	"""
	An error thrown when failing to read from a file.
	"""

	def __init__(self, file_path):
		"""
		Constructor for the class.
		"""

		message = 'Cannot read from file "%s".' % (file_path)
		super(FileReadError, self).__init__(self.__class__.__name__, message)

class FileWriteError(CustomError):

	"""
	An error thrown when failing to write to a file.
	"""

	def __init__(self, file_path):
		"""
		Constructor for the class.
		"""

		message = 'Cannot write to file "%s".' % (file_path)
		super(FileWriteError, self).__init__(self.__class__.__name__, message)

class PlatformNotSupportedError(CustomError):

	"""
	An error thrown if the specfiied platform is not supported.
	"""

	def __init__(self, platform):
		"""
		Constructor for the class.
		"""

		message = 'Platform "%s" is not supported.' % (platform)
		super(PlatformNotSupportedError, self).__init__(self.__class__.__name__, message)

class ConfigFileParsingError(CustomError):

	"""
	An error thrown if failed to parse a configuration file.
	"""

	def __init__(self, file_path):
		"""
		Constructor for the class.
		"""

		message = 'Failed to parse the configuration file "%s".' % (file_path)
		super(ConfigFileParsingError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Command in packages.command.abstractcommand

class ExecuteCommandError(CustomError):

	"""
	An error thrown when a Command execution fails.
	"""

	def __init__(self, message):
		"""
		Constructor for the class.

		@param message: The message describing the error.
		"""

		super(ExecuteCommandError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# DepFileNode in thedeployer.packages.depfile.node

class DepFileParsingError(CustomError):

	"""
	An error thrown when parsing a DepFile fails.
	"""

	def __init__(self, message = "", line = None, column = 0):
		"""
		Constructor for the class.
		"""

		_message = "Failed to parse the DepFile."
		if "" != message:
			_message = _message + " " + message

		if None != line:
			_message = _message.rstrip(".") + ": line %s, column %s" % (str(line), str(column))

		_message = _message.rstrip(".") + "."

		super(DepFileParsingError, self).__init__(self.__class__.__name__, _message)

# exceptions used by
# DepFileNode in thedeployer.packages.depfile.node

class ServerNotDefinedError(CustomError):

	"""
	An error thrown when parsing a DepFile fails.
	"""

	def __init__(self, server_id):
		"""
		Constructor for the class.
		"""

		message = 'The referenced server "%s" was not defined.' % (server_id)
		super(ServerNotDefinedError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Stack in thedeployer.packages.depfile.stack

class StackEmptyError(CustomError):

	"""
	An error attempting to pop from an empty stack or retrieving the top of an empty stack.
	"""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		super(StackEmptyError, self).__init__(self.__class__.__name__, "Stack is empty.")

# exceptions used by
# Server in thedeployer.packages.depfile.server
# Server in thedeployer.packages.depfile.fileset
# Server in thedeployer.packages.depfile.target

class IdentifierExistsError(CustomError):

	"""
	Some objects must have a unique identifier string, like Servers or Targets.
	This exception is thrown on attempting to re-use an id.
	"""

	def __init__(self, id):
		"""
		Constructor for the class.
		"""

		message = 'Identifier must be unique. Attempted to use the identifier "%s" more than once.' % (id)
		super(IdentifierExistsError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# package is thedeployer.packages.ftp

class FtpConnectionError(CustomError):
	"""
	raised on ftp connection failure
	"""

	def __init__(self, *args):
		"""
		Constructor for the class.
		"""
		message = 'Can not connect with the Ftp sever'
		message += os.linesep.join(args)
		super(FtpConnectionError, self).__init__(self.__class__.__name__, message)

class FtpCommandError(CustomError):
	"""
	raised on ftp command failure
	"""

	def __init__(self, *args):
		"""
		Constructor for the class.
		"""
		message = os.linesep.join(args)
		super(FtpCommandError, self).__init__(self.__class__.__name__, message)

class FtpDisconnectionError(CustomError):
	"""
	raised on disconnecting ftp server
	"""

	def __init__(self, *args):
		"""
		Constructor for the class.
		"""
		message = 'Can not disconnect with the Ftp sever'
		message += os.linesep.join(args)
		super(FtpDisconnectionError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Server in thedeployer.packages.depfile.default

class DefaultNotSupportedError(CustomError):

	"""
	Only a pre-defined number of default variables are supported.
	"""

	def __init__(self, name):
		"""
		Constructor for the class.
		"""

		message = "The default variable \"" + name + "\" is not supported."
		super(DefaultNotSupportedError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Server in thedeployer.packages.depfile.variable

class ArgumentRequiredError(CustomError):

	"""
	A DepFile can require command line arguments to be passed.
	"""

	def __init__(self, name):
		"""
		Constructor for the class.
		"""

		message = "The command line argument \"" + name + "\" is required but has not been specified."
		super(ArgumentRequiredError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Server in thedeployer.packages.depfile.target

class DependencyCycleError(CustomError):

	"""
	In a list of targets, some target may depend on each other, on condition there is not a cycle.
	"""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		message = "A dependency cycle was detected."
		super(DependencyCycleError, self).__init__(self.__class__.__name__, message)

class PropertiesFileParsingError(CustomError):

	"""
	Raised when an error occurs in parsing a Properties file.
	"""

	def __init__(self, path):
		"""
		Constructor for the class.
		"""

		message = "Failed to parse the properties file \"" + path + "\"."
		super(PropertiesFileParsingError, self).__init__(self.__class__.__name__, message)


class FileNotExistsError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'File or directory does not exist: '
		self.args = args
		message = self.__str__()
		super(FileNotExistsError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileChmodError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in changing file mode: '
		self.args = args
		message = self.__str__()
		super(FileChmodError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileChownError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in changing the ownership of the file: '
		self.args = args
		message = self.__str__()
		super(FileChownError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileRemoveError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in removing a file: '
		self.args = args
		message = self.__str__()
		super(FileRemoveError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileExistsError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'File Exists :'
		self.args = args
		message = self.__str__()
		super(FileExistsError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class MakeDirError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in creating a new directory: '
		self.args = args
		message = self.__str__()
		super(MakeDirError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class ListDirectoryError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in listing directory: '
		self.args = args
		message = self.__str__()
		super(ListDirectoryError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class FilePutError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in put files: '
		self.args = args
		message = self.__str__()
		super(FilePutError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class DirectoryNotEmptyError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Directory not empty: '
		self.args = args
		message = self.__str__()
		super(DirectoryNotEmptyError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileDeleteError(CustomError):
	"""
	Raised if the delete operation failed
	"""
	def __init__(self, *args):

		self.message = 'Error in deleting files: '
		self.args = args
		message = self.__str__()
		super(FileDeleteError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class FileMoveError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in Moving files: '
		self.args = args
		message = self.__str__()
		super(FileMoveError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileRenameError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error in renaming file: '
		self.args = args
		message = self.__str__()
		super(FileRenameError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class CommandExecuteError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'Error Executing command: '
		self.args = args
		message = self.__str__()
		super(CommandExecuteError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class PermissionsInvalidError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(PermissionsInvalidError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class InvalidDate(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(InvalidDate, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ValidationTypeError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(ValidationTypeError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class TemporaryFileError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'error in creating temporary file name: '
		self.args = args
		message = self.__str__()
		super(TemporaryFileError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class FileDownloadError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = 'error in downloading file: '
		self.args = args
		message = self.__str__()
		super(FileDownloadError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class DecompressionNotSupportedError(CustomError):
	'''
	Raised while compressing unknown file type
	'''
	def __init__(self, *args):

		message = 'undefined file type' + str(args)
		super(DecompressionNotSupportedError, self).__init__(self.__class__.__name__, message)

class CompressionNotSupportedError(CustomError):
	'''
	Raised while compressing unknown file type
	'''
	def __init__(self, *args):

		message = 'undefined file type' + str(args)
		super(CompressionNotSupportedError, self).__init__(self.__class__.__name__, message)


class CompressionError(CustomError):
	'''
	Raised if any error occurred while compressing
	'''
	def __init__(self, *args):

		message = 'Error while compressing ' + str(' '.join(args))
		super(CompressionError, self).__init__(self.__class__.__name__, message)

class ClassInitializationError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(ClassInitializationError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ServerValidationError(CustomError):
	"""
	Raised if the targeted file is not exist
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(ServerValidationError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class CheckOutError(CustomError):
	"""
	Raised if Error in check out from subversion
	used in subversion module
	"""
	def __init__(self, *args):

		self.message = 'Error When checking out from VCS: '
		self.args = args
		message = self.__str__()
		super(CheckOutError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class GetFileError(CustomError):
	"""
	raised when any error occurred while downloading file from server
	"""
	def __init__(self, *args):

		self.message = 'Error in getting file: '
		self.args = args
		message = self.__str__()
		super(GetFileError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class GetLastModificationTimeError(CustomError):
	"""
	raised when any error occurred while getting the last modification time of file
	"""
	def __init__(self, *args):

		self.message = 'Error in getting last modification time of the file: '
		self.args = args
		message = self.__str__()
		super(GetLastModificationTimeError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class PermissionDeniedError(CustomError):
	"""
	raised when operation not permitted
	"""
	def __init__(self, *args):

		self.message = 'Not permitted operation: '
		self.args = args
		message = self.__str__()
		super(PermissionDeniedError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ListFileError(CustomError):
	"""
	Raised if Error in check out from subversion
	used in subversion module
	"""
	def __init__(self, *args):

		self.message = 'Error in listing files of VCS: '
		self.args = args
		message = self.__str__()
		super(ListFileError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

# exceptions used by
# Server in thedeployer.packages.filters.*

class FilterProcessingError(CustomError):

	"""An error thrown when failing to apply any filter on a string."""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		message = "Failed to apply the filter."
		super(FilterProcessingError, self).__init__(self.__class__.__name__, message)

class FilterOnFileProcessingError(CustomError):

	"""An error thrown when failing to apply a filter to a file."""

	def __init__(self, path):
		"""
		Constructor for the class.

		@param parameter: The path of the file.
		"""

		message = "Failed to apply the filter to the file \"" + path + "\"."
		super(FilterOnFileProcessingError, self).__init__(self.__class__.__name__, message)

# exceptions used by
# Server in thedeployer.packages.clients.sqlclient

class SqlDumpError(CustomError):

	"""An error thrown when failing to dump a database."""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		message = "Failed to dump the database tables."
		super(SqlDumpError, self).__init__(self.__class__.__name__, message)

class SqlImportError(CustomError):

	"""An error thrown when failing to import to a database."""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		message = "Failed to import the SQL file."
		super(SqlImportError, self).__init__(self.__class__.__name__, message)

class FtpSyncError(CustomError):
	"""
	Raised if Error in check out from subversion
	used in subversion module
	"""
	def __init__(self, *args):

		self.message = ''
		self.args = args
		message = self.__str__()
		super(FtpSyncError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class IncompleteReponseError(CustomError):
	def __init__(self, *args):
		self.message = 'Response Not Completed'
		self.args = args
		message = self.__str__()
		super(IncompleteReponseError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ResponseValidationError(CustomError):
	def __init__(self, *args):
		self.message = 'Response Not Valid'
		self.args = args
		message = self.__str__()
		super(ResponseValidationError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class AcceptedCodeError(ResponseValidationError):
	def __init__(self, *args):
		self.message = 'Status Code is not accepted'
		self.args = args
		message = self.__str__()
		super(AcceptedCodeError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class RejectedCodeError(ResponseValidationError):
	def __init__(self, *args):
		self.message = 'Status Code is rejected'
		self.args = args
		message = self.__str__()
		super(RejectedCodeError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class CookiesValidationError(ResponseValidationError):
	def __init__(self, *args):
		self.message = 'Cookies is not valid'
		self.args = args
		message = self.__str__()
		super(CookiesValidationError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class BodyRegExError(ResponseValidationError):
	def __init__(self, *args):
		self.message = 'Body is not valid'
		self.args = args
		message = self.__str__()
		super(BodyRegExError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class AcceptedBodyRegExError(BodyRegExError):
	def __init__(self, *args):
		self.message = 'Required body value is not matched'
		self.args = args
		message = self.__str__()
		super(AcceptedBodyRegExError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class RejectedBodyRegExError(BodyRegExError):
	def __init__(self, *args):
		self.message = 'Rejected body value is matched'
		self.args = args
		message = self.__str__()
		super(RejectedBodyRegExError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ProxyParamError(CustomError):
	def __init__(self, *args):
		self.message = 'Proxy parameters are no valid'
		self.args = args
		message = self.__str__()
		super(ProxyParamError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class AuthParamError(CustomError):
	def __init__(self, *args):
		self.message = 'Authentication parameters are not valid'
		self.args = args
		message = self.__str__()
		super(AuthParamError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class ExRequestError(CustomError):
	def __init__(self, *args):
		self.message = 'Error during request execution'
		self.args = args
		message = self.__str__()
		super(ExRequestError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class MatchDataError(CustomError):
	def __init__(self, *args):
		self.message = 'Error in matching data'
		self.args = args
		message = self.__str__()
		super(MatchDataError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class LoginError(CustomError):
	def __init__(self, *args):
		self.message = ''
		self.args = args
		message = self.__str__()
		super(LoginError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class ConnectionError(CustomError):
	def __init__(self, *args):
		self.message = ''
		self.args = args
		message = self.__str__()
		super(ConnectionError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')


class TimeoutError(CustomError):
	def __init__(self, *args):
		self.message = ''
		self.args = args
		message = self.__str__()
		super(TimeoutError, self).__init__(self.__class__.__name__, message)

	def __str__(self):
		return self.message + str(self.args).strip('()')

class DbCreateError(CustomError):

	"""An error thrown when failed to create a database."""

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: The name of the database.
		"""

		message = 'Failed to create the database "%s"' % (name)
		super(DbCreateError, self).__init__(self.__class__.__name__, message)

class DbDropError(CustomError):

	"""An error thrown when failed to drop a database."""

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: The name of the database.
		"""

		message = 'Failed to drop database "%s"' % (name)
		super(DbDropError, self).__init__(self.__class__.__name__, message)

class DbStatementError(CustomError):

	"""An error thrown when failed to drop a database."""

	def __init__(self, message):
		"""
		Constructor for the class.

		@param name: The name of the database.
		"""

		super(DbStatementError, self).__init__(self.__class__.__name__, message)
