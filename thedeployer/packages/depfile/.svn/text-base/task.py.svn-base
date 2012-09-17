#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.commands.command import Command
from thedeployer.packages.algorithms.graph import GraphNode
from thedeployer.packages.algorithms.graph import solve_graph

class Task(DepFileNode, GraphNode):

	"""
	A task is a collection of executable commands.
	"""

	"""@__name: The name of the task."""
	"""@__depends: The name of another task that this task depends on."""
	"""@__commands: An array of instances of a descendant of Command."""

	def __init__(self, name, depends = ""):
		"""
		Constructor for the class.

		@param name: The name of the target.
		@param depends: The name of another target that this target depends on (optional).

		@raise InvalidParameterError: If the name is a 0-length string.
		"""

		if "" == name:
			raise InvalidParameterError("name", "Name cannot be empty")

		self.__name = name
		self.__depends = depends
		self.__commands = []

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Task object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".
			Optional keys are "depends".

		@return: An instance of a Task.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{"depends": ""},
			{"name": "variable_name", "depends": "variable_name"}
			)

		return Task(parameters["name"], parameters["depends"])

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of a descendant of Command.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of a descendant of Command.
		"""

		for parent in node.__class__.__bases__:
			if Command == parent:
				self.__commands.append(node)
				return True

		raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__commands):
			raise DepFileParsingError("At least one command must be defined.")

	def get_commands(self):
		"""
		@return: An array of commands.
		"""
		
		return self.__commands

	def get_name(self):
		"""
		@return: The name of the task, a non-empty string.
		"""

		return self.__name

	def get_depends(self):
		"""
		@return: The name of the task this one depends on, can be an empty string if no such dependency.
		"""

		return self.__depends