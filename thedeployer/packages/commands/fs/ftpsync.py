#
# Copyright (c) 2008 vimov
#

from os import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.commands.command import Command
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.project import Project
from thedeployer.packages.sync.ftpsync import FtpSync
from thedeployer.packages.depfile.server import *

class FtpSyncCommand(Command):

	"""
	Syncs a local directory to an FTP/SFTP server based on the timestamp.
	"""

	"""@__retry: The number of times to retry execution on error."""

	def __init__(self, project, source, destination, _from, to, excludes = None, chmod = None, delete = False, retry = 1):
		"""
		Constructor for the class.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		@param _from: path of the local directory on source server.
		@param to: path on destination FTP/FTPS server.
		@param exclude: The name of a referenced FileSet of excludes.
		@param chmod: value for destination files to be chmoded to
		@param delete: if true any files in destination that do not exist in source will be deleted
		@param retry: The number of times to retry execution on error.

		@raise Others: All other exceptions raised by the parent class'es constructor.
		"""

		local_server = project.get_server(source)
		_from = local_server.to_absolute(_from)

		remote_server = project.get_server(destination)
		to = remote_server.to_absolute(to)

		self.__from = _from
		self.__to = to
		self.__excludes = excludes
		self.__chmod = chmod
		self.__delete = delete
		self.__retry = retry

		super(FtpSyncCommand, self).__init__(project, source, destination)
		self.accept_fileset(0, 0, [excludes])

	@classmethod
	def get_instance(self, project, parameters):
		"""
		Creates an instance of a FtpSyncCommand object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "source", "destination", "from" and "to".
			Optional keys are "excludes", "chmod", "delete" and "retry".

		@return: An instance of FtpSyncCommand

		@raise InvalidParameterError: If the required parameter(s) are not specified.
		@raise Others: All other exceptions raised by the constructor.
		"""
		
		parameters = project.process_node_parameters(
			parameters,
			["source", "destination", "from", "to"],
			{"excludes": None, "chmod": None, "delete": False, "retry": 1},
			{"source": "variable_name", "destination": "variable_name", "from": "non_empty_string", "to": "non_empty_string", "excludes": "variable_name", "chmod":"string", "delete": "boolean", "retry": "integer"}
			)

		if FtpServer != project.get_server(parameters["destination"]).__class__ and SftpServer != project.get_server(parameters["destination"]).__class__:
			raise DepFileParsingError('Cannot sync to server "%s". Must be an FTP or SFTP server.' % (parameters["destination"]))

		return FtpSyncCommand(project, parameters["source"], parameters["destination"], parameters["from"], parameters["to"], parameters["excludes"], parameters["chmod"], parameters["delete"], parameters["retry"])

	def execute_local_to_remote(self, project):
		"""
		Syncs the local directory to a remote ftp directory.

		@param project: An instance of a Project.

		@rtype: bool
		@return: True on success
		"""

		AppLogger.info('Syncing local directory "%s" to directory "%s" at FTP server "%s".' % (self.__from, self.__to, self.destination))

		local_server = project.get_server(self.source)
		remote_server = project.get_server(self.destination)
		excludes_fileset = self.get_fileset(self.__excludes)

		ftpsync = FtpSync()
		ftpsync.run(local_server, remote_server, self.__from, self.__to, excludes_fileset, self.__chmod, self.__delete, self.__retry, True)
