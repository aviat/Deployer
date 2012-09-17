#
# Copyright (c) 2008 vimov
#

import os
import xml.parsers.expat

from thedeployer.packages.depfile.factory import DepFileFactory
from thedeployer.packages.depfile.project import Project
from thedeployer.packages.depfile.stack import *

class DepFileParser:

	"""
	Parser for Deployment Files.
	"""

	"""@__parser: An instance of an Expat parser."""

	"""@__root_element: The root element of the parsed tree. Should always be an instance of project"""
	"""@__top_element: The current top element in the stack."""
	"""@__stack: A stack used while creating the DepFile tree."""
	"""@__cl_arguments: A dictionary of the command line arguments sent, excluding application options (like -v)"""

	def __init__(self, cl_arguments):
		"""
		Constructor for the class.
		"""

		self.__parser = xml.parsers.expat.ParserCreate()
		self.__parser.StartElementHandler = self.start_element_handler
		self.__parser.EndElementHandler = self.end_element_handler
		self.__parser.CharacterDataHandler = self.character_data_handler

		self.__stack = Stack()

		self.__root_element = None
		self.__top_element = None

		self.__cl_arguments = cl_arguments

	def parse(self, file_path):
		"""
		Parse an XML file and returns an object for the top element.

		@param file_path: The path to the XML file.

		@rtype: DepFileNode
		@return: An instance that is inherited from at least DepFileNode
		"""

		try:
			handle = file(file_path, "r")
			xml_data = handle.read()
			handle.close()

		except Exception, e:
			raise FileReadError(file_path)

		try:
			self.__parser.Parse(xml_data)
			return self.__top_element[1]

		except xml.parsers.expat.ExpatError, e:
			raise DepFileParsingError(
				str(e).capitalize()
			)

	def start_element_handler(self, name, attributes):
		"""
		A callback for when an XML tag starts.

		@param name: The name of the newly opened tag.
		@param attributes: The attributes associated with the tag.

		@raise DepFileParsingError if the specified tag name was not found, cannot be in this place, or the
		attributes are invalid/missing.
		"""

		try:
			name = str(name)
			element = DepFileFactory.get_object(name, attributes, self.__root_element, self.__cl_arguments)

		except Exception, e:
			raise DepFileParsingError(
				e.get_message(),
				self.__parser.CurrentLineNumber,
				self.__parser.CurrentColumnNumber
			)

		if None == self.__root_element:
			if Project == element.__class__:
				self.__root_element = element
			else:
				raise DepFileParsingError("Root node must be a Project.")

		if self.__top_element:
			self.__top_element[1].add_child(element)

		self.__top_element = (name, element)
		self.__stack.push(self.__top_element)

	def end_element_handler(self, name):
		"""
		A callback for when an XML tag ends.

		@param name: The name of the just closed tag.

		@raise DepFileParsingError if the specified tag name was not opened in this scope before.
		"""

		try:
			name, node = self.__stack.pop()
			node.close_node()

		except Exception, e:
			raise DepFileParsingError(
				e.get_message(),
				self.__parser.CurrentLineNumber,
				self.__parser.CurrentColumnNumber
			)

		if not self.__stack.is_empty():
			self.__top_element = self.__stack.get_top()

	def character_data_handler(self, cdata):
		"""
		A callback for when the parser encounters a CDATA block.

		@param cdata: The contents of the CDATA block.

		@raise DepFileParsingError if the currently open tag does not accept cdata in it.
		"""

		try:
			self.__top_element[1].add_text_data(cdata)

		except Exception, e:
			raise DepFileParsingError(
				e.get_message(),
				self.__parser.CurrentLineNumber,
				self.__parser.CurrentColumnNumber
			)