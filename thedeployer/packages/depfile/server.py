#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.platform._platform import Platform

from thedeployer.packages.clients.localclient import LocalClient
from thedeployer.packages.clients.ftpclient import FtpClient
from thedeployer.packages.clients.sftpclient import SftpClient
from thedeployer.packages.clients.sshclient import SshClient
from thedeployer.packages.clients.webclient import WebClient
from thedeployer.packages.clients.mysqlclient import MysqlClient
from thedeployer.packages.clients.versioncontrol.subversionclient import SubversionClient

class Servers(DepFileNode):

	"""
	A collection of servers
	"""

	"""@__servers: An array of Server-descendants."""

	def __init__(self):
		"""
		Constructor for the class
		"""
		self.__servers = []

	def add_child(self, node):
		"""
		Adds a child element to the Servers.

		@param node: An instance of a descendant of the Server class.

		@rtype Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not a descendant of Server.
		"""

		found_parent = False

		for parent in node.__class__.__bases__:
			if Server == parent:
				found_parent = True
				break

		if True == found_parent:

			if Server.LOCAL == node.get_medium() and 0 < len(self.__servers):
				for server in self.__servers:
					if Server.LOCAL == server.get_medium():
						raise DepFileParsingError()

			self.__servers.append(node)
		else:
			raise DepFileParsingError()

		return True

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Servers object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.

		@return: An instance of Servers
		"""

		return Servers()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__servers):
			raise DepFileParsingError("At least one server must be defined.")

		for server in self.__servers:
			if server.__class__ == FtpServer or server.__class__ == SftpServer or server.__class__ == MysqlServer:
				webserver = server.get_webserver()
				if 0 != len(webserver):
					for server in self.__servers:
						if server.__class__ == WebServer and server.get_id() == webserver:
							break
					else:
						raise ServerNotDefinedError(webserver)

		return True

	def has_server(self, id):
		"""
		Looks up whether specified server is defined or not.

		@param id: Identifier of the server to look for.

		@rtype: Boolean
		@return: True if it exists, False if not found.
		"""

		for server in self.__servers:
			if id == server.get_id():
				return True

		return False

	def get_server(self, id):
		"""
		Returns the server with the specified id.

		@param id: Identifier of the server to look for.

		@return: An instance of a descendant of Server.

		@raise ServerNotDefinedError: If no server with the specified identifier exists.
		"""

		for server in self.__servers:
			if id == server.get_id():
				return server
		
		raise ServerNotDefinedError(id)

class Server(DepFileNode):

	"""
	Parent class for all server types.
	"""

	"""@medium: The medium of the server, can be LOCAL or REMOTE."""
	"""@id: The identifier for this instance of LocalServer, can be any non-zero-length string."""

	"""@LOCAL: Denotes the local server, the one running the program."""
	"""@REMOTE: Denotes a remote server."""
	"""@__all_ids: A list of all the defined servers so far."""

	LOCAL = 1001
	REMOTE = 1002
	__all_ids = []

	def __init__(self, id, medium):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param medium: The medium of the server, can be either LOCAL or REMOTE.

		@raise ServerIdentifierExistsError: If the identifier has already been used by another Server.
		@raise InvalidParameterError: If the value of medium is invalid.
		@raise DepFileParsingError: This class cannot be directly instantiated.
		"""

		if Server == self.__class__:
			raise DepFileParsingError()

		if False == Validator.validate_variable_name(id):
			raise InvalidParameterError("id", 'The server ID "%s" is invalid.' % (id))
		else:
			Server.__add_server_id(id)
			self.id = id

		if Server.LOCAL != medium and Server.REMOTE != medium:
			raise InvalidParameterError("medium", "Medium can be either LOCAL or REMOTE")
		else:
			self.medium = medium

	def get_medium(self):
		"""
		Returns the medium of the server.

		@return: The medium of the server.
		"""

		return self.medium

	@classmethod
	def __add_server_id(cls, id):
		"""
		Server IDs are unique, since they are referred to from other nodes. This methods registers a newly
		added server ID to the Server class. Each Server constructor verifies the __all_ids arrays by using
		__has_server_id method to make sure the Server ID was not used before.

		@param id: The identifier of the server to add.

		@raise ServerIdentifierExistsError: If the identifier has already been registered.
		"""

		if False == Server.__has_server_id(id):
			Server.__all_ids.append(id)
		else:
			raise IdentifierExistsError(id)

	@classmethod
	def __has_server_id(cls, id):
		"""
		Looks up the Server ID in the __all_ids array. Used by the constructor to maintain ID uniqueness.

		@param id: The identifier of the server to look for.

		@rtype Boolean
		@return: True if it exists, False if not.
		"""

		try:
			Server.__all_ids.index(id)
			return True

		except Exception, e:
			return False

	def get_id(self):
		"""
		Returns the identifier of the server.

		@return: Server Identifier, a non-empty string.
		"""
		return self.id

class LocalServer(Server, LocalClient):
	
	"""
	Represents the local server running the program.
	"""

	def __init__(self, id, root = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param root: The root directory to assume for all relative paths.
		"""

		Server.__init__(self, id, Server.LOCAL)
		LocalClient.__init__(self, root)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a LocalServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id".
			Optional keys are "root". Defaults to platform's root (/ on Linux and Mac, C:\ on Windows).

		@return: An instance of a child of LocalServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id"],
			{"root": None},
			{"id": "variable_name", "root": "string"}
			)

		return LocalServer(parameters["id"], parameters["root"])

class WebServer(Server, WebClient):
	
	"""
	Represents a remote web server.
	"""

	"""@__address: The web address (excluding the protocol, for the web server."""
	"""@__port: The port of the server."""
	"""@__document_root: The document root of the server."""
	"""@__language: A language this server supports, like PHP5."""

	def __init__(self, id, address, port, document_root, language):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param address: The web address (excluding the protocol, for the web server.
		@param port: The port of the server.
		@param document_root: The document root of the server.
		@param language: A language this server supports, like PHP5.
		"""

		if not Validator.validate(address, 'domain'):
			raise InvalidParameterError('address', 'Must be a valid domain name, excluding the protocol or path.')
		if not Validator.validate(port, 'port'):
			raise InvalidParameterError('port', 'Must be an integer value between 0 and 65535')
		if not Validator.validate(document_root, 'non_empty_string'):
			raise InvalidParameterError('document_root', 'Must be a non-empty string')
		if not Validator.validate(language, 'non_empty_string'):
			raise InvalidParameterError('language', 'Must be a non-empty string')

		self.__address = address
		self.__port = port
		self.__document_root = document_root
		self.__language = language

		Server.__init__(self, id, Server.REMOTE)
		WebClient.__init__(self)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a WebServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id", "address", "language" and "document_root".
			Optional keys are "port".

		@return: An instance of a child of WebServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "address", "language", "document_root"],
			{"port": 80},
			{"id": "variable_name", "address": "non_empty_string", "port": "integer", "language": "non_empty_string", "document_root": "non_empty_string"}
			)

		return WebServer(parameters["id"], parameters["address"], parameters["port"], parameters["document_root"], parameters["language"])

class FtpServer(Server, FtpClient):

	"""
	Represents a remote FTP server.
	"""

	"""@__webserver: An instance of WebServer for this FTP server."""

	def __init__(self, id, platform, host, port, username, password, root = "", webserver = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param host: The host of the ftp server.
		@param port: The port of the server.
		@param username: Username.
		@param password: Password.
		@param root: The root to assume for all relative paths.
		@param webserver: Identifier of the webserver this FTP server stores files for.
		"""

		if 0 != len(webserver) and False == Validator.validate_variable_name(webserver):
			raise InvalidParameterError("webserver", 'The webserver ID "%s" is invalid.' % (webserver))
		else:
			self.__webserver = webserver

		Server.__init__(self, id, Server.REMOTE)
		FtpClient.__init__(self, platform, host, username, password, port, root)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a FtpServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id", "os", "host", "username" and "password".
			Optional keys are "port", "root" and "webserver".

		@return: An instance of FtpServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "host", "username", "password", "os"],
			{"port": 21, "root": "", "webserver": ""},
			{"id": "variable_name", "os": "non_empty_string", "host": "non_empty_string", "port": "integer", "username": "non_empty_string", "password": "non_empty_string", "root": "string", "webserver": "variable_name"}
			)

		platform_instance = Platform.get_instance(parameters["os"])

		return FtpServer(parameters["id"], platform_instance, parameters["host"], parameters["port"], parameters["username"], parameters["password"], parameters["root"], parameters["webserver"])

	def get_webserver(self):
		"""
		Returns the identifier of the webserver running on this server.

		@return: The identifier of the webserver.
		"""

		return self.__webserver

class SftpServer(Server, SftpClient):

	"""
	Represents a remote SFTP server.
	"""

	"""@__webserver: An instance of WebServer for this SFTP server."""

	def __init__(self, id, platform, host, port, username, password, root = "", webserver = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param host: The host of the ftp server.
		@param port: The port of the server.
		@param username: Username.
		@param password: Password.
		@param root: The root to assume for all relative paths.
		@param webserver: Identifier of the webserver this FTP server stores files for.
		"""

		if 0 != len(webserver) and False == Validator.validate_variable_name(webserver):
			raise InvalidParameterError("webserver", 'The webserver ID "%s" is invalid.' % (webserver))
		else:
			self.__webserver = webserver

		Server.__init__(self, id, Server.REMOTE)
		SftpClient.__init__(self, platform, host, username, password, port, root)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a SftpServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id", "os", "host", "username" and "password".
			Optional keys are "port", "root" and "webserver".

		@return: An instance of SftpServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "host", "username", "password", "os"],
			{"port": 21, "root": "", "webserver": ""},
			{"id": "variable_name", "os": "non_empty_string", "host": "non_empty_string", "port": "integer", "username": "non_empty_string", "password": "non_empty_string", "root": "string", "webserver": "variable_name"}
			)

		platform_instance = Platform.get_instance(parameters["os"])

		return FtpServer(parameters["id"], platform_instance, parameters["host"], parameters["port"], parameters["username"], parameters["password"], parameters["root"], parameters["webserver"])

	def get_webserver(self):
		"""
		Returns the identifier of the webserver running on this server.

		@return: The identifier of the webserver.
		"""

		return self.__webserver

class RsyncServer(Server):
	
	"""
	Represents a remote Rsync server.
	"""

	"""@__id: The identifier of this server, must be a non-empty string."""
	"""@__host: The host of the Rsync server."""
	"""@__model_name: The model name of the rsync daemon."""
	"""@__port: The port of the server."""
	"""@__username: Username."""
	"""@__password: Password."""

	def __init__(self, id, host, model_name , port = 873, username = "", password = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param host: The host of the Rsync server.
		@param model_name: The model name of the rsync daemon.
		@param port: The port of the server.
		@param username: Username.
		@param password: Password.
		"""
		
		self.__id = id
		self.__host = host
		self.__model_name = model_name
		self.__port = port
		self.__username = username
		self.__password = password

		Server.__init__(self, id, Server.REMOTE)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a RsyncServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id", "host" and "model_name".
			Optional keys are "port", "username", "password".

		@return: An instance of RsyncServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "host", "model_name"],
			{"port": 873, "username": "", "password": ""},
			{"id": "variable_name", "host": "non_empty_string", "model_name" : "non_empty_string", "port": "integer", "username": "string", "password": "string"}
			)

		return RsyncServer(parameters["id"], parameters["host"], parameters["model_name"], parameters["port"], parameters["username"], parameters["password"])
	
	def det_id(self):
		return self.__id
	
	def get_host(self):
		return self.__host
	
	def get_model_name(self):
		return self.__model_name
	
	def get_port(self):
		return self.__port
	
	def get_username(self):
		return self.__username
	
	def get_password(self):
		return self.__password
	
class SshServer(Server, SshClient):
	
	"""
	Represents a remote SSH server.
	"""

	def __init__(self, id, platform, host, port = 22, username = "", password = "", certificate_file = "", passphrase = "", root = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param host: The host of the Rsync server.
		@param port: The port of the server.
		@param username: Username.
		@param password: Password.
		@param certificate_file: Path to a local certificate file.
		@param passphrase: The passphrase encrypting the certificate file.
		"""

		Server.__init__(self, id, Server.REMOTE)
		SshClient.__init__(self, platform, host, port, username, password, certificate_file, passphrase, root)
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a SshServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id", "os" and "host".
			Optional keys are "port", "username", "password", "certificate_file", "passphrase" and "root".

		@return: An instance of SshServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "host", "os"],
			{"port": 22, "username": "", "password": "", "certificate_file" : "", "passphrase" : "", "root" : ""},
			{"id": "variable_name", "host": "non_empty_string", "os" : "non_empty_string", "port": "integer", "username": "string", "password": "string", "certificate_file" : "string", "passphrase" : "string", "root" : "string"}
			)

		platform_instance = Platform.get_instance(parameters["os"])

		return SshServer(parameters["id"], platform_instance, parameters["host"], parameters["port"], parameters["username"], parameters["password"], parameters["certificate_file"], parameters["passphrase"], parameters["root"])


class SubversionServer(Server, SubversionClient):
	
	"""
	Represents a remote subversion server.
	"""

	def __init__(self, id, repository_path, username = "", password = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param repository_path: repository path on subversion server
		@param username: username on subversion server
		@param password: password on the subversion server
		"""
		
		Server.__init__(self, id, Server.REMOTE)
		SubversionClient.__init__(self, repository_path, username, password)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a SubversionServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id" and "repository_path"
			Optional keys are "username" and "password".

		@return: An instance of a SubversionServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "repository_path"],
			{"username": "", "password": ""},
			{"id": "variable_name", "repository_path": "non_empty_string", "username": "string", "password": "string"}
			)

		return SubversionServer(parameters["id"], parameters["repository_path"], parameters["username"], parameters["password"])

class MysqlServer(Server, MysqlClient):
	
	"""
	Represents a Mysql server.
	"""

	"""@__webserver: An instance of WebServer for this SFTP server."""

	def __init__(self, id, host, port = 3306, username = "", password = "", webserver = ""):
		"""
		Constructor for the class.

		@param id: The identifier of this server, must be a non-empty string.
		@param host: host of the MySQL server.
		@param port: port of the MySQL server.
		@param username: user on the MySQL server.
		@param password: user's password.
		@param webserver: Identifier of the webserver this FTP server stores files for.
		"""

		if 0 != len(webserver) and False == Validator.validate_variable_name(webserver):
			raise InvalidParameterError("webserver", 'The webserver ID "%s" is invalid.' % (webserver))
		else:
			self.__webserver = webserver

		Server.__init__(self, id, Server.REMOTE)
		MysqlClient.__init__(self, host, port, username, password)

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a MysqlServer object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "id" and "host".
			Optional keys are "port", "webserver", "username" and "password".

		@return: An instance of a MysqlServer
		"""

		parameters = project.process_node_parameters(
			parameters,
			["id", "host"],
			{"port": 3306, "username": "", "password": "", "webserver": ""},
			{"id": "variable_name", "host": "non_empty_string", "port": "integer", "username": "string", "password": "string", "webserver": "variable_name"}
			)

		return MysqlServer(parameters["id"], parameters["host"], parameters["port"], parameters["username"], parameters["password"])

	def get_webserver(self):
		"""
		Returns the identifier of the webserver running on this server.

		@return: The identifier of the webserver.
		"""

		return self.__webserver
