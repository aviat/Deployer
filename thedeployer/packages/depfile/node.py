#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *

class DepFileNode(object):

	"""
	Represents a node in the tree created by parsing a Deployment File (depfile).
	The node has an element, which can be a CopyCommand for example, possibly list of children, and possibly text
	data.
	"""

	def __init__(self):
		"""
		This is an abstract class and cannot be instantiated directly.
		"""

		if self.__class__ == DepFileNode:
			raise NotSupportedError()

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a Command object and returns it. It must be overriden by the inheritor.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.

		@return: An instance of a child of Command
		"""

		raise NotImplementedError()

	def add_child(self, node):
		"""
		Adds a child element to the node. It must be overriden by the inheritor. The inheritor then has to
		decide in which member it should add the child (or not add it at all if its type is invalid to it).
		If not inherited by the child, it is assumed the child does not support children of its own, and thus
		all calls to this method will yield a DepFileParsingError exception.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node does not support child nodes.
		"""

		raise DepFileParsingError()

	def add_text_data(self, text_data):
		"""
		Adds text data to this object, read as a CDATA from the XML file.
		If not inherited by the child, it is assumed the child does not allow CDATA inside of it, and thus
		all calls to this method will yield a DepFileParsingError exception.

		@param text_data: The CDATA read from the XML file.

		@rtype: Boolean
		@return: True on success. False if the node does not expect cdata.
		"""

		return False

	def close_node(self):
		"""
		Called when the closing tag of an element is encountered. A class should implement this method if it
		needs post-validation processing. For example, to verify that at least one child has been added.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		return True
