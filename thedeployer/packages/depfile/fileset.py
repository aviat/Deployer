#
# Copyright (c) 2008 vimov
#

import re

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.platform.file import FileObject

class FileSets(DepFileNode):

	"""
	A collection of filesets.
	
	A FileSet is a definition of a number of rules that declare match patterns against files or directories. These
	patterns can be used by some functions to filter their operation. For example, a Copy command may exclude a
	number of files or directories who are matched by the definition in a FileSet. An example declaration of a
	FileSet in XML is:

		<fileset name="set1">
			<match directory="" pattern="^config.php$" type="file" />
			<match pattern="^install.php$" />
			<match directory="files/backup" pattern="(.*)\.php" />
		</fileset>

		<fileset name="set2">
			<match directory="/var/www/" pattern="(.*)\.pyc" />
			<match directory="/var/www/" pattern="log" type="directory" />
		</fileset>

		<fileset name="set3">
			<match type="directory" />
		</fileset>

	A directory can be empty, in this case the pattern is applied to all directories under the working directory.
	It can be absolute, or relative. If it is relative, then it is relative to the working directory. For example,
	for a copy operation from /var/www to /var/backup, the directory can be specified as /var/www/logs or logs (of
	course, there could be trailing slashes.

	If a type is specified, then neither the directory or pattern have to be specified. But if it was not specified,
	then at least pattern must be specified.

	FileSets can be either globally defined or locally defined. For globally defined FileSets, they are declares in
	the <filesets> tag right inside the <project> tag. An example of a globally defined FileSet:

		<project>
		...
		<filesets>
			<fileset name="set1">
			...
			</fileset>
		</filesets>
		...
		<targets>
		...

	A locally defined FileSet is declared as a child to a Command. Not all commands support FileSet children. When a
	command references a fileset, it is looked up in locally defined FileSet instances first, then, in globally
	defined ones. That's, local has higher precedence than global. An example for a Command that declares a local
	FileSet:

		<compress source="local" destination="local" from="/var/www" to="/tmp/test.tar.gz" excludes="set1">
			<fileset name="set1">
				<match directory="log" pattern="(.*)" />
			</fileset>
		</compress>

	Refer to the documentation of the Command class for information on how to programmatically make use of FileSet
	objects in a Command.
	"""

	"""@__filesets: An array of instances of FileSet."""

	def __init__(self):
		"""
		Constructor for the class.
		"""
		self.__filesets = []
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a FileSets object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.

		@return: An instance of a FileSets.
		"""

		return FileSets()

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of FileSet.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise IdentifierExistsError: If the identifier name of the new FileSet object is already used.
		@raise DepFileParsingError: If the node is not an instance of FileSet.
		"""

		if FileSet == node.__class__:

			for fileset in self.__filesets:
				if node.get_name() == fileset.get_name():
					raise IdentifierExistsError(node.get_name())

			self.__filesets.append(node)
		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__filesets):
			raise DepFileParsingError("At least one fileset must be defined.")

	def get_filesets(self):
		"""
		Returns an array of FileSet instances.

		@return: An array of instances of FileSet.
		"""

		return self.__filesets

class FileSet(DepFileNode):

	"""
	A collection of "file" tags (FileSetEntry).
	"""

	"""@__name: The unique name of the FileSet."""
	"""@__filesetentries: An array of instances of FileSetEntry."""

	def __init__(self, name):
		"""
		Constructor for the class.
		"""

		self.__name = name
		self.__filesetentries = []
	
	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a FileSet object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Expected keys are "name".

		@return: An instance of a FileSet.
		"""

		parameters = project.process_node_parameters(
			parameters,
			["name"],
			{},
			{"name": "variable_name"}
			)

		return FileSet(parameters["name"])

	def add_child(self, node):
		"""
		Adds a child element to the node, which must be an instance of FileSetEntry.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise DepFileParsingError: If the node is not an instance of FileSetEntry.
		"""

		if FileSetEntry == node.__class__:
			self.__filesetentries.append(node)
		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if 1 > len(self.__filesetentries):
			raise DepFileParsingError("At least one file entry must be defined.")

	def get_name(self):
		"""
		Return the name identifier of this FileSet.
		"""

		return self.__name

	def match(self, path, name, _type):
		"""
		Matches the name in the specified path against the current rules.

		@param path: The path of the parent of name, can be relative or absolute.
		@param name: The name of the child under the parent specified by path.
		@param _type: The type of the file, can be FileSet.FILE or FileSet.DIRECTORY.

		@rtype: Boolean
		@return: True if it matches a rule, False if it does not.
		"""
		return False
		for fileset_entry in self.__filesetentries:
			
			if re.match(re.escape(fileset_entry.get_directory()) + "(/|\\\\)?(.)*", path):
				
				pattern = fileset_entry.get_pattern()
				match_type = fileset_entry.get_type()
				
				flag = True
				
				if pattern:
					if not re.match(pattern, name):
						flag = False
				
				if flag and match_type:
					if _type != match_type:
						flag = False
				
				return flag

		return False

class FileSetEntry(DepFileNode):

	"""
	Reprents a rule as specified by the "file" tag.
	"""

	"""@__directory: The parent directory to apply the "file" regular expression against. Can be an empty string."""
	"""@__pattern: The regular expression to use against matching the file name or directory name."""
	"""@__type: The type of the file to match against. Can be FileObject.FILE, FileObject.DIRECTORY, FileObject.LINK or None."""

	def __init__(self, directory = "", pattern = "", _type = None):
		"""
		Constructor for the class.
		"""

		self.__directory = directory
		self.__pattern = pattern
		self.__type = _type

	@classmethod
	def get_instance(cls, project, parameters):
		"""
		Creates an instance of a FileSetEntry object and returns it.

		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param parameters: A dictionary of parameters that are sent to the constructor.
			Optional keys are "directory", "pattern" and "type".

		@return: An instance of a FileSetEntry.
		"""

		parameters = project.process_node_parameters(
			parameters,
			[],
			{"directory": "", "pattern": "", "type": None},
			{"name": "string", "pattern": "string", "type": "string"}
			)

		if "" == parameters["pattern"] and None == parameters["type"]:
			
			raise DepFileParsingError()

		elif None != parameters["type"]:

			if "file" == parameters["type"].lower():
				parameters["type"] = FileObject.FILE
			elif "directory" == parameters["type"].lower():
				parameters["type"] = FileObject.DIRECTORY
			elif "link" == parameters["type"].lower():
				parameters["type"] = FileObject.LINK
			else:
				raise DepFileParsingError()

		return FileSetEntry(parameters["directory"], parameters["pattern"], parameters["type"])

	def get_directory(self):
		"""
		Returns the parent directory to apply the pattern against.
		"""

		return self.__directory


	def get_pattern(self):
		"""
		Returns the pattern to match with.
		"""

		return self.__pattern
	
	def get_type(self):
		"""
		Returns type of match
		"""
		
		return self.__type
