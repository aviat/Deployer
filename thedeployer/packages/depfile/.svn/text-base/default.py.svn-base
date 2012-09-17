#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.variable import *

#@TODO: Refactor so Defaults is not static.

class Defaults(DepFileNode):

	#__all_defaults = []

	def __init__(self):
		self.__all_defaults = []

	@classmethod
	def get_instance(cls, project, parameters):

		return Defaults()

	def add_child(self, node):

		if Default == node.__class__:
			self.__all_defaults.append(node)
		else:
			raise DepFileParsingError()

		return True

	def has_default(self, name):

		for default in self.__all_defaults:
			if name == default.get_name():
				return True

		return False

	def get_default_value(self, name):

		for default in self.__all_defaults:
			if name == default.get_name():
				return default.get_value()

		# should raise an error
		return None

	@classmethod
	def is_default_supported(cls, name):

		if "retry" == name or "create_dirs" == name:
			return True
		else:
			return False

class Default(DepFileNode):

	"""@__name: The name of the default."""
	"""@__value: The value of this default variable."""

	def __init__(self, name, value):

		if False == Defaults.is_default_supported(name):
			raise DefaultNotSupportedError(name)
		elif False == Variables.validate_name(name):
			raise DepFileParsingError("Default name must be a non-empty string. Allowed characters are letters, numbers, dots, underscores and dashes.")
		elif "" == value:
			raise InvalidParameterError("value", "Value for \"" + name + "\" cannot be empty")

		self.__name = name
		self.__value = value
	
	@classmethod
	def get_instance(cls, project, parameters):

		parameters = project.process_node_parameters(
			parameters,
			["name", "value"],
			{},
			{"name": "variable_name", "value": "string"}
			)

		return Default(parameters["name"], parameters["value"])

	def get_name(self):
		return self.__name

	def get_value(self):
		return self.__value

	def set_name(self, name):
		self.__name = name

	def set_value(self, value):
		self.__value = value
