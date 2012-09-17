#
# Copyright (c) 2008 vimov
#

import re
import os

from thedeployer.libs.pexpect.pexpect import *

from thedeployer.packages.customexceptions import *
from thedeployer.packages.application import Application
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.depfile.server import *
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.logger import AppLogger

class Rsync(object):

	#__environment
	#__timeout
	#__pexpect

	def __init__(self):

		self.__timeout = 30
		self.__environment = None
		self.__pexpect = None
		
		platform = Platform.get_current()
		
		if platform.get_platform() == Platform.PLATFORM_WINDOWS:
			self.__environment = self.__get_windows_environment_variables()

	def __get_windows_environment_variables(self):

		rsync_bin_directory = Application.get_application_directory() + "\\" + Application.get_option("paths", "rsync-win")

		environment = {}
		environment["CWRSYNCHOME"] = rsync_bin_directory
		environment["CYGWIN"] = "nontsec"
		environment["HOME"] = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
		environment["CWOLDPATH"] = os.environ["PATH"]
		environment["PATH"] = environment["CWRSYNCHOME"] + ";" + os.environ["PATH"]

		return environment

	def run(self, source, destination, _from, to, rsync_options):
		"""
		run synchronization process
		
		@param source: source server
		@param destination: destination server
		@param _from: path on source server
		@param to: path on destination server
		@param rsync_options: options of rsync operations
		"""
		
		#validating that source or destination are servers and at least one of them is local server
		if not (isinstance(source, LocalServer) or isinstance(source, RsyncServer) or isinstance(source, SshServer)):
			raise InvalidParameterError('source', 'Must be instance of server class')
		if not (isinstance(destination, LocalServer) or isinstance(destination, RsyncServer) or isinstance(destination, SshServer)):
			raise InvalidParameterError('destination', 'Must be instance of server class')
		if not (isinstance(source, LocalServer) or isinstance(destination, LocalServer)):
			raise ServerValidationError, 'one of source or destination should be a LocalServer'
		
		#validatind rest of parameters
		if not Validator.validate_non_empty_string(_from):
			raise InvalidParameterError('_from', 'Must be non-empty string')
		if not Validator.validate_string(to):
			raise InvalidParameterError('to', 'Must be a string value')
		if not isinstance(rsync_options, RsyncOptions):
			raise InvalidParameterError('rsync_options', 'Must be a string value')
		
		options = self.__format_options(rsync_options, source, destination)
		source_path = self.__format_path(source, _from)
		destination_path = self.__format_path(destination, to)

		# fork and execute the command.
		command = "rsync " + options + " --verbose " + source_path + " " + destination_path
		self.__pexpect = spawn(command, env = self.__environment)

		# login if one of source or destination is SshServer
		if isinstance(source, SshServer):
			self.__ssh_login(source._SshServer__password, source._SshServer__passphrase)
		elif isinstance(destination, SshServer):
			self.__ssh_login(destination._SshServer__password, destination._SshServer__passphrase)
		
		# login if one of source or destination is RsyncServer
		if isinstance(source, RsyncServer):
			self.__rsync_login(source.get_password())
		if isinstance(destination, RsyncServer):
			self.__rsync_login(destination.get_password())
		
		#close rsync process	
		self.__pexpect.close()

		# parse the result
		exit_status = self.__pexpect.exitstatus
		output_lines = self.__pexpect.before.strip("\r\n").split("\r\n")[1:]

		if 0 != exit_status:
			matches = None
			if output_lines:
				matches = re.match("rsync error: (.*)", output_lines[-1])
			AppLogger.debug(exit_status)
			
			if matches:
				AppLogger.debug(matches.group(1))
		else:
			AppLogger.debug("Ok!")
			AppLogger.debug(exit_status)
			AppLogger.debug(output_lines)
			
			
	def __ssh_login(self, password, passphrase):
		
		i = self.__pexpect.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password)", "(?i)(?:passphrase for key)", "(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)
		
		# accept the certificate if asked.
		if 0 == i:
			
			# This is what you get if SSH does not have the remote host's
			# public key stored in the 'known_hosts' cache.

			self.__pexpect.sendline("yes")
			i = self.__pexpect.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password)", "(?i)(?:passphrase for key)", "(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)

		# send password or passphrase
		if 1 == i:

			self.__pexpect.sendline(password)
			i = self.__pexpect.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password)", "(?i)(?:passphrase for key)","(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)
		
		if 2 == i:
			self.__pexpect.sendline(passphrase)
			i = self.__pexpect.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password)", "(?i)(?:passphrase for key)","(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)
			
		if 0 == i or 1 == i or 2 == i or 3 == i:
			raise LoginError, "Error in loging to ssh server"
		elif 4 == i:
			raise ConnectionError, "Error in connectimg to ssh server"
		elif 5 == i:
			raise TimeoutError, "Timeout Error"
		elif 6 == i:
			pass
		
		return True
	
	
	def __rsync_login(self, password):
		
		#@TODO: test when rsync server is configured to take password
		
		i = self.__pexpect.expect(["(?i)(?:Password)", "(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)

		# send password 
		if 0 == i:

			self.__pexpect.sendline(password)
			k = self.__pexpect.expect(["(?i)(?:Password)", "(?i)permission denied", "(?i)connection closed by remote host", TIMEOUT, EOF], self.__timeout)

			if 0 == k or 1 == k:
				raise LoginError, "Error in loging to rsync server"
			elif 2 == k:
				raise ConnectionError, "Error in connectimg to rsync server"
			elif 3 == k:
				raise TimeoutError, "Timeout Error"
			elif 4 == k:
				pass

		return True
	
	
	def __format_path(self, server, path):
		"""
		format the rsync source or destination path depending on if source or destination server is LocalServer, SshServer or RsyncServer
		"""
		
		formated_path = ""
		if isinstance(server, SshServer):
			if server._SshServer__username != "":
				formated_path += server._SshServer__username + "@"
			formated_path += server._SshServer__host + ":" + path
			
		elif isinstance(server, RsyncServer):
			formated_path += "rsync://"
			if server.get_username() != "":
				formated_path += server._RsyncServer__username + "@"
			formated_path += server.get_host() + ":" + str(server.get_port()) + "/" + server.get_model_name() + path		
		
		elif isinstance(server, LocalServer):
			formated_path += path
		return formated_path
	
	
	def __format_options(self, rsync_options, source, destination):
		"""
		format the rsync options in form as rsync tack it option arguments
		"""
		
		ssh_server = None
		if isinstance(source, SshServer):
			ssh_server = source
		elif isinstance(destination, SshServer):
			ssh_server = destination
			
		if ssh_server:
			params = rsync_options._RsyncOptions__params
			
			if ssh_server._SshServer__port != 22:

				value = None
				if params.has_key('-e'):
					value = params.pop('-e')
				elif params.has_key('--rsh'):
					value = params.pop('--rsh')
				
				if value:
					value = value.rstrip("'")
					
					if not re.match(r".*(-p)|(--port)", value):
						value += " -p " + str(ssh_server._SshServer__port)+ "'"
				else:
					value = "'ssh -p " + str(ssh_server._SshServer__port) + "'"
				
				params['--rsh'] = value
				
		return str(rsync_options)

class RsyncOptions(object):
	"""
	Represent options of Rsync
	"""

	"""
	@__params:
	"""

	def __init__(self):
		self.__params = {}

	def add_option(self, name, value = ""):
		"""
		Add option of rsunc options
		
		@param name: name of option
		@param value: value of option if exist
		"""
		
		if not Validator.validate_non_empty_string(name):
			raise InvalidParameterError('name', 'Must be non-empty string')
		if not Validator.validate_string(value):
			raise InvalidParameterError('value', 'Must be a string')
		
		self.__params[name] = value
		
	def __str__(self):

		str = ""
		for key in self.__params:
			str += key
			if "" != self.__params[key]:
				str += "="+self.__params[key]
			str += " "
		
		return str