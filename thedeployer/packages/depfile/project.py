#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.default import *
from thedeployer.packages.depfile.variable import *
from thedeployer.packages.depfile.server import *
from thedeployer.packages.depfile.target import *
from thedeployer.packages.depfile.validator import *
from thedeployer.packages.depfile.fileset import *

class Project(DepFileNode):

	LAST_SCHEMA_VERSION = "1.0"

	"""@__name: The name of the project."""
	"""@_schema_version: The version of the schema."""

	"""@__defaults: An instance of Defaults that has default parameters referred to if a node's optional attributes were not specified."""
	"""@__variables: An instance of Variables that has variables which were specified either through passed arguments or through a property file."""
	"""@__servers: An instance of Servers which has a list of servers."""
	"""2__filesets: An instance of FileSets which has a list of FileSet objects."""
	"""@__targets: An instance of Targets which has a list of build targets."""

	def __init__(self, name, schema_version = "1.0"):
		"""
		Constructor for the class

		@param name: The name of the project.

		@raise InvalidParameterError: If the name is a 0-length string.
		"""

		if "" == name:
			raise InvalidParameterError("name", "The project's name cannot be empty")

		self.__name = name
		self.__schema_version = schema_version

		self.__defaults = None
		self.__variables = None
		self.__servers = None
		self.__filesets = None
		self.__targets = None

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of this object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".
			Optional keys are "schema".

		@return: An instance of a Project
		"""

		if False == parameters.has_key("name") or "" == parameters["name"]:
			raise DepFileParsingError()

		schema_version = Project.LAST_SCHEMA_VERSION
		if parameters.has_key("schema") and "" != parameters["schema"]:
			schema_version = parameters["schema"]

		return Project(parameters["name"], schema_version)

	def add_child(self, node):
		"""
		Adds a child element to the project.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node does not support a child node of this type.
		"""

		if Defaults == node.__class__:
			self.__defaults = node
		elif Variables == node.__class__:
			self.__variables = node
		elif Servers == node.__class__:
			self.__servers = node
		elif FileSets == node.__class__:
			self.__filesets = node
		elif Targets == node.__class__:
			self.__targets = node
		else:
			raise DepFileParsingError()

		return True

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if None == self.__servers:
			raise DepFileParsingError("At least one server must be defined.")

		if None == self.__targets:
			raise DepFileParsingError("At least one target must be defined.")

		targets = self.__targets.get_targets(False)
		for target in targets:
			if "" != target.get_depends():
				for dependant in targets:
					if target.get_depends() == dependant.get_name():
						break
				else:
					raise DepFileParsingError(
						"Target \"%s\" depends on a non-defined target \"%s\"" % (target.get_name(), target.get_depends())
					)

		return True

	def get_name(self):
		"""
		Returns the name of the Project.
		"""
		return self.__name

	def get_servers(self):
		"""
		Returns an instance of Servers.
		"""
		return self.__servers

	def get_server(self, id):
		"""
		Returns an instance of the server with the specified identifier.

		@param id: The string identifier of the server.
		"""
		return self.__servers.get_server(id)

	def get_filesets(self):
		"""
		Returns an array of FileSet objects.
		"""

		if None != self.__filesets:
			return self.__filesets.get_filesets()
		else:
			return None

	def get_targets(self, sort_by_dependency = False):
		"""
		Returns an array of Target instances.

		@param sort_by_dependency: Sort the resulting array by the dependency of targets on each other, with the
			first target being the one being depended on, and the last being the depending on others.
		"""
		return self.__targets.get_targets(sort_by_dependency)

	def get_defaults(self):
		"""
		Returns a dictionary of the defaults.
		"""
		return self.__defaults

	def process_node_parameters(self, parameters, required_parameters, implicit_defaults, types):
		"""
		"""

		# subistitute the variable delcaration in the values of the parameters.
		parameters = self.__subistitute_variables_in_parameter_values(parameters)

		# applying the defaults is equivalent to adding the default keys/values for the node's supported defaults.
		parameters = self.__apply_defaults(parameters, implicit_defaults)

		# normlize the value of the variables, like always use True for booleans (and not "true" or 1 or "1")
		parameters = self.__normalize_parameter_values(parameters, types)

		# validate the value of the parameters conform to the specified types.
		self.__validate_parameter_values(parameters, required_parameters, types)

		# verify all the required parameters have been specified.
		self.__verify_required_parameters(parameters, required_parameters)

		return parameters

	def __subistitute_variables_in_parameter_values(self, parameters):
		"""
		"""

		if None == self.__variables:
			return parameters

		variables = self.__variables.get_variables()
		if 0 == len(variables):
			return parameters

		for name, value in parameters.iteritems():
			for variable_name, variable_value in variables.iteritems():
				value = value.replace("${" + variable_name + "}", variable_value)

			parameters[name] = value

		return parameters

	def __apply_defaults(self, parameters, implicit_defaults):
		"""
		"""

		for implicit_default_name, implicit_default_value in implicit_defaults.iteritems():

			if parameters.has_key(implicit_default_name):
				pass
			elif None != self.__defaults and self.__defaults.has_default(implicit_default_name):
				parameters[implicit_default_name] = self.__defaults.get_default_value(implicit_default_name)
			else:
				parameters[implicit_default_name] = implicit_default_value

		return parameters

	def __validate_parameter_values(self, parameters, required_parameters, types):
		"""
		Note: do not validate if it is not specified and it is optional.
		"""

		for name, value in parameters.iteritems():

			try:
				if None != value or required_parameters.index(name):
					if types.has_key(name) and False == Validator.validate(value, types[name]):
						raise InvalidParameterError(name, "Must be of type '" + type + "'")
			except Exception, e:
				pass

		return True

	def __verify_required_parameters(self, parameters, required_parameters):
		"""
		Verifies that all the required keys are set in the parameters dictionary.

		@param parameters: Dictionary of keys and their values.
		@param required_parameters: An array of the required keys.

		@rtype: Boolean
		@return: True on success.

		@raise MissingParameterError: If a required key is not specified in the dictionary.
		"""

		for parameter in required_parameters:
			if False == parameters.has_key(parameter):
				raise MissingParameterError(parameter)

		return True

	def __normalize_parameter_values(self, parameters, types):
		"""
		"""

		for name, value in parameters.iteritems():

			if types.has_key(name):
				if bool != type(value) and "boolean" == types[name].lower():
					if "true" == parameters[name].lower() or "1" == parameters[name]:
						parameters[name] = True
					elif "false" == parameters[name].lower() or "0" == parameters[name]:
						parameters[name] = False
					else:
						raise InvalidParameterError(name, "Must be 'true', '1', 'false' or '0'")
				elif "integer" == types[name].lower():
					try:
						parameters[name] = int(value)
					except Exception:
						raise InvalidParameterError(name, "Must be an integer")
				elif "float" == types[name].lower():
					try:
						parameters[name] = float(value)
					except Exception:
						raise InvalidParameterError(name, "Must be an float")

		return parameters
