#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.clients.abstractclient import AbstractClient
from thedeployer.packages.clients.sftpclient import SftpClient
from thedeployer.libs import paramiko
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.customexceptions import *

class SshClient(SftpClient):

	"""@__host: The host of the Rsync server."""
	"""@__port: The port of the server."""
	"""@__username: Username."""
	"""@__password: Password."""
	"""@__certificate_file: Path to a local certificate file."""
	"""@__passphrase: The passphrase encrypting the certificate file."""
	"""@__root: Root to use for relative paths."""

	def __init__(self, platform, host, port = 22, username = "", password = "", certificate_file = "", passphrase = "", root = ""):
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

		if not Validator.validate_non_empty_string(host):
			raise InvalidParameterError('host', 'host can not be None or empty string')
		
		if not Validator.validate_integer(port):
			raise InvalidParameterError('port', 'port must be integer')

		if not Validator.validate_non_empty_string(certificate_file) and ( not Validator.validate_non_empty_string(username) or not Validator.validate_non_empty_string(password)):
			raise InvalidParameterError('username', 'A username and password must be specified if not using certificate login')

		self.__certificate_file = certificate_file
		self.__passphrase = passphrase
		
		super(SshClient, self). __init__(platform, host, username, password, port, root)
		self.connect()

	def connect(self):
		"""
		overide the connect method to the sftp client from the ssh client 
		"""
		try:
			self.__sshclient = paramiko.SSHClient()	
			Known_hosts_file = os.path.expanduser('~/.ssh/known_hosts')
			self.__sshclient.load_system_host_keys(Known_hosts_file)
			system_host_keys = self.__sshclient._system_host_keys
			self.__sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			if Validator.validate_non_empty_string(self.__certificate_file):
				"""
				connect with the identity key and without password
				Note:
					the parameter look_for_keys enable searching for the file which contains the private keys
				"""
				self.__sshclient.connect(hostname=self.host, password = self.__passphrase, key_filename = self.__certificate_file, look_for_keys=False)

#				self.__sshclient.connect(hostname=self.host, password=self.__passphrase, look_for_keys=True)

			else:
				"""
				connect with the ssh server with the username and password
				"""	
				self.__sshclient.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, look_for_keys=False)

			server_host_keys = self.__sshclient.get_host_keys()
			
			for hostname, keys in server_host_keys.iteritems():
				for keytype, key in keys.iteritems():
					system_host_keys.add(hostname, keytype, key)
	
			system_host_keys.save(Known_hosts_file)
				
			client = self.__sshclient.open_sftp()
			if client is None:
				raise
			self.set_client(client)
		except Exception, e:
			raise #FtpConnectionError, str(e)
		
		
	def disconnect(self, retry):
		"""
		overiding the disconnect of the sftp client
		"""
		try:
			self.__sshclient.close()
			self.set_client(None)
		except Exception, e:
			raise FtpConnectionError, str(e)
