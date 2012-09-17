#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.task import Task
from thedeployer.packages.algorithms.graph import GraphNode
from thedeployer.packages.algorithms.graph import solve_graph

class Targets(DepFileNode):

	"""
	A collection of targets.
	"""

	"""@__targets: An array of instances of Target."""

	def __init__(self):
		"""
		Constructor for the class.
		"""
		self.__targets = []
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Targets object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.

		@return: An instance of a Targets.
		"""

		return Targets()

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of Target.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of Target.
		"""

		if Target == node.__class__:

			for target in self.__targets:
				if node.get_name() == target.get_name():
					raise IdentifierExistsError(node.get_name())

			self.__targets.append(node)
		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__targets):
			raise DepFileParsingError("At least one target must be defined.")

	def get_targets(self, sort_by_dependency = True):
		"""
		Returns an array of Target instances.

		@param sort_by_dependency: Sort the resulting array by the dependency of targets on each other, with the
			first target being the one being depended on, and the last being the depending on others.

		@return: An array of instances of Target.

		@raise: DependencyCycleError: If the dependency could not be solved, i.e., a cycle.
		"""

		if True == sort_by_dependency:
			return solve_graph(self.__targets)
		else:
			return self.__targets

class Target(DepFileNode, GraphNode):

	"""
	A target is a collection of related tasks to be executed in part of the deployment process.
	"""

	"""@__name: The name of the target."""
	"""@__depends: The name of another target that this target depends on."""
	"""@__tasks: An array of tasks, each an instance of Task."""
	
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
		self.__tasks = []

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Target object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".
			Optional keys are "depends".

		@return: An instance of a Target.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{"depends": ""},
			{"name": "variable_name", "depends": "variable_name"}
			)

		return Target(parameters["name"], parameters["depends"])

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of Task.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of Task.
		"""

		if Task == node.__class__:

			for task in self.__tasks:
				if node.get_name() == task.get_name():
					raise IdentifierExistsError(node.get_name())

			self.__tasks.append(node)
		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__tasks):
			raise DepFileParsingError("At least one task must be defined.")

		tasks = self.get_tasks(False)
		for task in tasks:
			if "" != task.get_depends():
				for dependant in tasks:
					if task.get_depends() == dependant.get_name():
						break
				else:
					raise DepFileParsingError(
						"Task \"%s\" depends on a non-defined task \"%s\"" % (task.get_name(), task.get_depends())
					)

	def get_tasks(self, sort_by_dependency = True):
		"""
		Returns an array of Task instances.

		@param sort_by_dependency: Sort the tasks by the dependency of tasks on each other, with the
			first target being the one being depended on, and the last being the depending on others.

		@return: An array of instances of Task.

		@raise: DependencyCycleError: If the dependency could not be solved, i.e., a cycle.
		"""

		if True == sort_by_dependency:
			return solve_graph(self.__tasks)
		else:
			return self.__tasks

	def get_name(self):
		"""
		@return: The name of the target, a non-empty string.
		"""

		return self.__name

	def get_depends(self):
		"""
		@return: The name of the target this one depends on, can be an empty string if no such dependency.
		"""

		return self.__depends
