#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.depfile.list import ListEntry

class Dictionary(DepFileNode):

	"""
	A collection of entries, a dictionary that is.
	"""

	"""@__entries: An dictionary of entries."""

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: The name of the Dictionary.
		"""

		self.__name = name
		self.__entries = {}
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Dictionary object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".

		@return: An instance of a Dictionary.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{},
			{"name": "variable_name"}
			)

		return Dictionary(parameters["name"])

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of ListEntry.

		@param node: An instance of a ListEntry class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of ListEntry.
		"""

		if ListEntry == node.__class__:

			if False == Validator.validate_variable_name(node.get_name()):
				raise DepFileParsingError()

			self.__entries[node.get_name()] = node.get_value()
		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__entries):
			raise DepFileParsingError("At least one entry must be defined.")

	def get_name(self):
		return self.__name

	def get_entries(self):
		"""
		Returns a dictionary of the entries.

		@return: A dictionary of the entries.
		"""

		return self.__entries
