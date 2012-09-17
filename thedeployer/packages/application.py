#
# Copyright (c) 2008 vimov
#

import ConfigParser
import os
import sys

from thedeployer.packages.customexceptions import *

class Application:

	__configuration_parser = None

	@classmethod
	def get_application_directory(cls):
		return dirname(os.path.join(sys.path[0], sys.argv[0]))

	@classmethod
	def load_configuration_file(cls, path):

		try:
			parser = ConfigParser.ConfigParser()
			parser.readfp(open(path))

			Application.__configuration_parser = parser

		except Exception, e:
			raise FileReadError(path)

	@classmethod
	def get_option(cls, section, name):
		try:
			return Application.__configuration_parser.get(section, name)
		except Exception:
			raise MissingConfigurationParameterError(section, name)
