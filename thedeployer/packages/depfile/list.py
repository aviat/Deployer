#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode

class List(DepFileNode):

	"""
	A collection of entries, a list that is.
	"""

	"""@__entries: An array of entries."""

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: The name of the List.
		"""

		self.__name = name
		self.__entries = []
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a List object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".

		@return: An instance of a List.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{},
			{"name": "variable_name"}
			)

		return List(parameters["name"])

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of ListEntry.

		@param node: An instance of a ListEntry class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of ListEntry.
		"""

		if ListEntry == node.__class__:

			if 0 == len(node.get_value()):
				raise DepFileParsingError()

			self.__entries.append(node.get_value())
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
			raise DepFileParsingError("At least one list entry must be defined.")

	def get_name(self):
		return self.__name

	def get_entries(self):
		"""
		Returns an array of list entries.

		@return: An array of list entries.
		"""

		return self.__entries

class ListEntry(DepFileNode):

	"""
	Represents a single entry in a list or dictionary.
	"""

	"""@__name: The name of the entry."""
	"""@__value: The value of the entry."""

	def __init__(self, name = "", value = ""):
		"""
		Constructor for the class.

		@param name: The name of the entry.
		@param value: The value of the entry.
		"""

		self.__name = name
		self.__value = value

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a ListEntry object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Required key is "value".
			Optional key is "name".

		@return: An instance of a ListEntry.
		"""

		parameters = project.process_node_parameters(
			parameters,
			[],
			{"name": "", "value": ""},
			{"name": "string", "value": "string"}
			)

		return ListEntry(parameters["name"], parameters["value"])

	def get_name(self):
		return self.__name

	def get_value(self):
		return self.__value
