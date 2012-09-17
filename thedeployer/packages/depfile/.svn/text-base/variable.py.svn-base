#
# Copyright (c) 2008 vimov
#

import re
import ConfigParser

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import *
from thedeployer.packages.depfile.validator import *

class Variables(DepFileNode):

	"""
	Variables are all name/value pairs that can be referenced in the script by using ${name}. The variables can be
	either command line arguments, whose name is defined with an argument tag and whose value is retrieved from
	the command line interface, or they can be retrieved from a property file (an INI-like file).
	
	Arguments have higher precedence than variables, and variable precedence is bound by the order of their
	definition. For example, if a property file defined a variable X.Y to 1, and then a property file defined X.Y
	as 2, then it will be stored as 2. Whatever the order is, arguments have higher precedence.
	
	During processing the DepFile, the arguemnts and properties are collected in the members vars, the arguments are
	proessed from the command line and if all the required arguments were specified, the entered variables are
	stored in __variables, possibly replacing ones read from a property file.

	Note that a variable's name may contain letters, numbers, underscores, dashes and dots, only.
	"""

	"""@__arguments: An array used to store instances of Argument during the parsing of the DepFile."""
	"""@__properties: An array used to store instances of Properties during the parsing of the DepFile."""
	"""@__cl_arguments: A dictionary used to store the name/value pairs of the passed command line arguments."""

	"""@__variables: A dictionary of name/value pairs. This dictionary is filled from one or more property files. It
		is only initialized when the Variables node is closed (close_node)."""

	def __init__(self):
		"""
		Constructor for the class.
		"""

		self.__arguments = []
		self.__properties = []
		self.__cl_arguments = {}
		
		self.__variables = {}

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Variables object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.

		@return: An instance of a child of Variables
		"""

		return Variables()

	def add_child(self, node):
		"""
		Adds a child element to the node. The child can either be an "argument" or a "properties".
		A property file defined after another will replace all the properties with the same name in that earlier
		property file.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node does not support the type of node passed.
		"""

		if Argument == node.__class__:

			if True == node.is_required() and False == self.__cl_arguments.has_key(node.get_name()):
				raise ArgumentRequiredError(node.get_name())
			elif False == node.is_required() and False == self.__cl_arguments.has_key(node.get_name()):
				AppLogger.info("The optional argument \"" + node.get_name() + "\" was not specified.")
			elif True == self.__cl_arguments.has_key(node.get_name()):
				node.set_value(self.__cl_arguments[node.get_name()])
				self.__arguments.append(node)

		elif Properties == node.__class__:
			self.__properties.append(node)
		else:
			raise NotSupportedError()

	def close_node(self):
		"""
		Called when the closing tag of "variables" is encountered. On closing, the command line arguments are
		passed and evaluated, and are then added to the __variables dictionary.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__arguments) and 1 > len(self.__properties):
			raise DepFileParsingError("At least one argument or one property file must be specified.")

		# add the properties to the Variables.__variables dictionary.
		for properties in self.__properties:
			self.__variables.update(properties.get_properties())

		# add the arguments to the Variables.__variables dictionary.
		for argument in self.__arguments:		
			self.__variables[argument.get_name()] = argument.get_value(self.__cl_arguments)

		self.__arguments = None
		self.__properties = None
		self.__cl_arguments = None

		return True

	@classmethod
	def filter(cls, attributes):
		"""
		Filters a dictionary of key/value pairs, by replacing all references to variables in the values by the
		respective variable's value as defined by an argument or a property file. For example, if the dictionary
		sent was {"retry":"${retry}","description":"it is '${description}'"}

		@param attributes: A dictionary of attributes associated with a DepFile tag.

		@return: The same dictionary after replacing the variables with the values using defined variables.
		"""

		#for attribute_name, attribute_value in attributes:
		#	pass

		return attributes

	@classmethod
	def validate_name(cls, name):
		"""
		Validates the variable name. Variable name must be a non-empty string. Allowed characters are letters, numbers, dots, underscores and dashes.

		@param name: The name to validate.

		@rtype: Boolean
		@return: True on success, False on failure.
		"""
		
		return Validator.validate_variable_name(name)

	def set_cl_arguments(self, cl_arguments):
		"""
		Sets a dictionary of the command line arguments passed to the deployment session.
		
		@param cl_arguments: A dictionary of the command line arguments sent, excluding application options (like -v)
		"""
		self.__cl_arguments = cl_arguments

	def get_variables(self):
		"""
		Returns the dictionary of variables. 
		"""

		return self.__variables

class Argument(DepFileNode):

	"""@__name: The name of the argument."""
	"""@__value: The value of the argument."""
	"""@__required: Whether or not this argument must be specified."""

	def __init__(self, name, required = True):
		"""
		Constructor for the class.

		@param name: The name of the argument which is used in referencing it as a variable.
		@param required: Whether this is a required argument and must be specified at the command line or not.
			Default is True.

		@raise DepFileParsingError: If the name is empty or does not follow the pattern letters, numbers, dots,
			underscores and dashes.
		"""

		if False == Variables.validate_name(name):
			raise DepFileParsingError("Argument name must be a non-empty string. Allowed characters are letters, numbers, dots, underscores and dashes.")

		self.__name = name
		self.__value = ""
		self.__required = required

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of an Argument object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param arguments: A dictionary of arguments that are sent to the constructor.
			Expected keys are "name".
			Optional keys are "required". Defaults to True.

		@return: An instance of a child of Argument
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{"required": True},
			{"name": "variable_name", "required": "boolean"}
			)
		
		return Argument(parameters["name"], parameters["required"])

	def get_name(self):
		"""
		Returns the name of the argument.
		"""
		return self.__name

	def get_value(self, cl_arguments):
		"""
		Returns the value of the argument as sent to the command line interface.
		"""
		return self.__value
	
	def set_value(self, value):
		"""
		Sets the value of the Argument.
		"""
		self.__value = value

	def is_required(self):
		"""
		Returns True if the argument is required and must be specified at the command line interface, False
		otherwise.
		"""
		return self.__required

class Properties(DepFileNode):
	"""
	Represents a Properties file.
	
	A properties file is divided into sections, and each section consists of a number of variables. A section's
	name or variable's name may contain letters, numbers, underscores, dashes and dots, only.
	
	When read using get_properties, variables are stored in the dictionary in the form section_name.variable_name.
	Note that since the dot is allowed, there may be multiple dots in this fully qualified name.

	Example properties file:

	[section1]
	foodir: %(dir)s/whatever
	dir.name=frob
	[section.2]
	file.name=file.txt
	"""

	"""@__path: The path of the properties file."""

	def __init__(self, path):
		"""
		Constructor for the class.
		"""

		self.__path = path

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Properties object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param arguments: A dictionary of arguments that are sent to the constructor.
			Expected keys are "file".

		@return: An instance of a child of Properties
		"""

		parameters = project.process_node_parameters(
			parameters,
			["file"],
			{},
			{"file": "non_empty_string"}
			)

		return Properties(parameters["file"])

	def get_properties(self):
		"""
		Returns a dictionary of arguments as read from the properties file.

		When read using get_properties, variables are stored in the dictionary in the form section_name.variable_name.
		Note that since the dot is allowed, there may be multiple dots in this fully qualified name.

		Example properties file:

		[section1]
		foodir: %(dir)s/whatever
		dir.name=frob
		[section.2]
		file.name=file.txt

		Returned as:
		{"section1.foodir": "frob/whatever", "section1.dir.name": "frob", "section.2.file.name": "file.txt"}

		Lines starting with # or ; are considered comments and are ignored.
		"""

		try:
			parser = ConfigParser.ConfigParser()
			parser.readfp(open(self.__path))
			
			properties = {}

			# then, read the section variables
			for section in parser.sections():
				for name, value in parser.items(section):
					properties[section + "." + name] = value

			return properties

		except Exception, e:
			raise PropertiesFileParsingError(self.__path)
