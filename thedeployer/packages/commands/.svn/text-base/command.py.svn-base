#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.node import DepFileNode
from thedeployer.packages.depfile.server import *
from thedeployer.packages.depfile.fileset import FileSets, FileSet
from thedeployer.packages.depfile.list import List
from thedeployer.packages.depfile.dictionary import Dictionary

#@TODO: currnetly, no validation is performed on creation of the XML tree that referenced filesets actually exist!

class Command(DepFileNode):

	"""
	Abstract class that represents an executable command.

	On FileSet children:

	Some Commands may allow for children of a FileSet type, like the CompressCommand that can use a locally defined
	FileSet for excluding files while compressing. In general, all Commands do not allow for children, so to make a
	Command allow for FileSet children, call the function self.accept_fileset() in the constructor. Make sure you
	call this function after calling the super to Command. With this function, you specify what the minimum number
	of FileSet objects should be, and what the maximum should be, and what are the variable names of referenced
	FileSets this instance of the Command is. For example, for the following command:

		<compress source="local" destination="local" from="/var/www" to="/tmp/test.tar.gz" excludes="set1">
			<fileset name="set1">
				<file directory="log" pattern="(.*)" />
			</fileset>
		</compress>

	the call to accept_fileset() function in the constructor of CompressCommand would evaluate to:
		self.accept_fileset(0, 0, ["set1"])

	The accept_fileset function will verify that the minimum has been declared, that the maximum has not been reached,
	and that the referenced FileSet actually has been declared either locally first, or globally second.

	On List and Dictionary items:

	Each command can contain child List and Dictionary items, that are referenced to with their name from the
	command's attributes. They work similar to FileSets, with the exception that their is no global counter-part to
	the locally defied List and Dictionary types. An example:

		<mysqldump source="mysql" destination="local" to="dump.sql" databases="dbs" options="opts">
			<list name="dbs">
				<entry value="blog"/>
			</list>
			<dictionary name="opts">
				<entry name="--xml" value="" />
			</list>
		</mysqldump>

	Each entry for a list item has a "value" parameter, while entry tags for dictionary items must contain a "name"
	and a "value".

	To accept list and dictionary children, call in the constructor accept_list and accept_dictionary functions,
	similar to accept_fileset. Review MysqlDumpCommand for an example.

	On path parameters:

	All FileClient-descendant function properly handle the internal conversion of relative-to-root paths to
	absolute paths. However, for other Commands that take paths as arguments, they must manually handle the
	conversion of possibly-relative to absolute paths. Review MysqlDumpCommand for example, but in general, all you
	need to do is to add the following code to the constructor if "to" was a path parameter.

		local_server = project.get_server(destination)
		to = local_server.to_absolute(to)
	"""

	"""@project: An instance of the project of this command."""
	"""@source: The source server the command is executing on."""
	"""@destination: The destination server the command is executing on."""

	"""@__filesets_supported: Whether or not this Command accepts FileSet children."""
	"""@__filesets_minimum_count: The minimum number of FileSet instances this Command needs."""
	"""@__filesets_maximum_count: The maximum number of FielSet instances this Command can support. 0 for unlimited."""
	"""@__filesets_referencing_variables: The name of the FileSet variable names this Command references."""
	"""@__filesets: An array of instances of FileSet objects."""

	"""@__lists_supported: Whether or not this Command accepts List children."""
	"""@__lists_minimum_count: The minimum number of List instances this Command needs."""
	"""@__lists_maximum_count: The maximum number of List instances this Command can support. 0 for unlimited."""
	"""@__lists_referencing_variables: The name of the List variable names this Command references."""
	"""@__lists: An array of instances of List objects."""

	"""@__dictionaries_supported: Whether or not this Command accepts Dictionary children."""
	"""@__dictionaries_minimum_count: The minimum number of Dictionary instances this Command needs."""
	"""@__dictionaries_maximum_count: The maximum number of Dictionary instances this Command can support. 0 for unlimited."""
	"""@__dictionaries_referencing_variables: The name of the Dictionary variable names this Command references."""
	"""@__dictionaries: An array of instances of Dictionary objects."""

	def __init__(self, project, source, destination):
		"""
		Constructor for a Command. Must be overriden by the inheritor.

		@param source: The source server that the command will execute on.
		@param destination: The destination server that the command will execute on.
		"""

		self.project = project
		self.source = source
		self.destination = destination

		if None != source:
			project.get_server(source)
		if None != destination:
			project.get_server(destination)

		self.__filesets_supported = False
		self.__filesets_minimum_count = 0
		self.__filesets_maximum_count = 0
		self.__filesets_referencing_variables = 0
		self.__filesets = []

		self.__lists_supported = False
		self.__lists_minimum_count = 0
		self.__lists_maximum_count = 0
		self.__lists_referencing_variables = 0
		self.__lists = []

		self.__dictionaries_supported = False
		self.__dictionaries_minimum_count = 0
		self.__dictionaries_maximum_count = 0
		self.__dictionaries_referencing_variables = 0
		self.__dictionaries = []

	def add_child(self, node):
		"""
		Adds a child element to the node. It must be overriden by the inheritor. The inheritor then has to
		decide in which member it should add the child (or not add it at all if its type is invalid to it).
		If not inherited by the child, it is assumed the child does not support children of its own, and thus
		all calls to this method will yield a DepFileParsingError exception.

		@param node: An instance of a DepFileNode class.

		@rtype: Boolean
		@return: True on success.

		@raise IdentifierExistsError: If the identifier name of the new FileSet object is already used.
		@raise DepFileParsingError: If the node does not support child nodes.
		"""

		if True == self.__filesets_supported and FileSet == node.__class__:

			if 0 != self.__filesets_maximum_count and 0 != len(self.__filesets) and self.__filesets_maximum_count == len(self.__filesets):
				raise DepFileParsingError()

			if FileSet == node.__class__:

				for fileset in self.__filesets:
					if node.get_name() == fileset.get_name():
						raise IdentifierExistsError(node.get_name())

				self.__filesets.append(node)
			else:
				raise DepFileParsingError()

		elif True == self.__lists_supported and List == node.__class__:

			if 0 != self.__lists_maximum_count and 0 != len(self.__lists) and self.__lists_maximum_count == len(self.__lists):
				raise DepFileParsingError()

			if List == node.__class__:

				for _list in self.__lists:
					if node.get_name() == _list.get_name():
						raise IdentifierExistsError(node.get_name())

				self.__lists.append(node)
			else:
				raise DepFileParsingError()

		elif True == self.__dictionaries_supported and Dictionary == node.__class__:

			if 0 != self.__dictionaries_maximum_count and 0 != len(self.__dictionaries) and self.__dictionaries_maximum_count == len(self.__dictionaries):
				raise DepFileParsingError()

			if Dictionary == node.__class__:

				for dictionary in self.__dictionaries:
					if node.get_name() == dictionary.get_name():
						raise IdentifierExistsError(node.get_name())

				self.__dictionaries.append(node)
			else:
				raise DepFileParsingError()

		else:
			raise DepFileParsingError()

	def close_node(self):
		"""
		Called when the closing tag is called. It verifies all the required children are valid.

		@rtype: Boolean
		@return: True if the node meets all the require creation conditions.

		@raise KeyNotFoundError: If a referenced FileSet is not defined locally or globaly.
		@raise DepFileParsingError: If the node was not fully created as it should have been.
		"""

		if True == self.__filesets_supported:

			# check the minimum count has been met.
			if 0 != self.__filesets_minimum_count and self.__filesets_minimum_count > len(self.__filesets):
				raise DepFileParsingError()

			# check that all references identifies have been defined.
			for reference in self.__filesets_referencing_variables:

				if "" == reference or None == reference:
					continue

				for fileset in self.__filesets:
					if reference == fileset.get_name():
						break
				else:
					if None == self.project.get_filesets():
						raise KeyNotFoundError(reference)

					for fileset in self.project.get_filesets():
						if reference == fileset.get_name():
							break
					else:
						raise KeyNotFoundError(reference)

		elif True == self.__lists_supported:

			# check the minimum count has been met.
			if 0 != self.__lists_minimum_count and self.__lists_minimum_count > len(self.__lists):
				raise DepFileParsingError()

			# check that all references identifies have been defined.
			for reference in self.__lists_referencing_variables:

				if "" == reference or None == reference:
					continue

				for _list in self.__lists:
					if reference == _list.get_name():
						break
				else:
					raise KeyNotFoundError(reference)

		elif True == self.__dictionaries_supported:

			# check the minimum count has been met.
			if 0 != self.__dictionaries_minimum_count and self.__dictionaries_minimum_count > len(self.__dictionaries):
				raise DepFileParsingError()

			# check that all references identifies have been defined.
			for reference in self.__dictionaries_referencing_variables:

				if "" == reference or None == reference:
					continue

				for dictionary in self.__dictionaries:
					if reference == dictionary.get_name():
						break
				else:
					raise KeyNotFoundError(reference)

		return True

	def accept_fileset(self, minimum_count, maximum_count = 0, referencing_variables = []):
		"""
		Declares that this command support FileSet children. This function must be called in the constructor
		if the Command is to accept FileSet children.

		@param minimum_count: Minimum number of FileSet instances that must be defined by this command.
		@param maximum_count: Maximum number of FileSet instances this command may have. 0 for unlimited.
		@param referencing_variables: An array of the identifiers that this command instances declares it wants
			FileSet instances of. For example, if the Command had < ... excludes="fileset1" ... > then
			referencing_variables would be ["fileset1"].

		@raise IdentifierExistsError: If the identifier name of the new FileSet object is already used.
		"""

		self.__filesets_supported = True
		self.__filesets_minimum_count = minimum_count
		self.__filesets_maximum_count = maximum_count
		self.__filesets_referencing_variables = referencing_variables
		self.__filesets = []

	def accept_list(self, minimum_count, maximum_count = 0, referencing_variables = []):
		"""
		Declares that this command support List children. This function must be called in the constructor
		if the Command is to accept List children.

		@param minimum_count: Minimum number of List instances that must be defined by this command.
		@param maximum_count: Maximum number of List instances this command may have. 0 for unlimited.
		@param referencing_variables: An array of the identifiers that this command instances declares it wants
			List instances of. For example, if the Command had < ... excludes="list1" ... > then
			referencing_variables would be ["list1"].

		@raise IdentifierExistsError: If the identifier name of the new List object is already used.
		"""

		self.__lists_supported = True
		self.__lists_minimum_count = minimum_count
		self.__lists_maximum_count = maximum_count
		self.__lists_referencing_variables = referencing_variables
		self.__lists = []

	def accept_dictionary(self, minimum_count, maximum_count = 0, referencing_variables = []):
		"""
		Declares that this command support Dictionary children. This function must be called in the constructor
		if the Command is to accept Dictionary children.

		@param minimum_count: Minimum number of Dictionary instances that must be defined by this command.
		@param maximum_count: Maximum number of Dictionary instances this command may have. 0 for unlimited.
		@param referencing_variables: An array of the identifiers that this command instances declares it wants
			Dictionary instances of. For example, if the Command had < ... options="dict1" ... > then
			referencing_variables would be ["dict1"].

		@raise IdentifierExistsError: If the identifier name of the new Dictionary object is already used.
		"""

		self.__dictionaries_supported = True
		self.__dictionaries_minimum_count = minimum_count
		self.__dictionaries_maximum_count = maximum_count
		self.__dictionaries_referencing_variables = referencing_variables
		self.__dictionaries = []

	def get_fileset(self, name = None):
		"""
		Returns a FileSet object with the specified name.

		@param name: The name of the FileSet.

		@rtype: FileSet
		@return: An instance of a FileSet object.

		@raise InvalidParameterError: If the name is not a non-empty string.
		@raise KeyNotFoundError: If no FileSet of the specified name is defined, not locally and not globally.
		"""

		if None == name:
			return None

		if "" == name:
			raise InvalidParameterError("name", "Must not be empty")

		for fileset in self.__filesets:
			if name == fileset.get_name():
				return fileset

		raise KeyNotFoundError(name)

	def get_list(self, name = None):
		"""
		Returns a list type of entries specified in a List object.

		@param name: The name of the List.

		@return: A list.

		@raise InvalidParameterError: If the name is not a non-empty string.
		@raise KeyNotFoundError: If no List of the specified name is defined locally to the command.
		"""

		if None == name:
			return []

		if "" == name:
			raise InvalidParameterError("name", "Must not be empty")

		for _list in self.__lists:
			if name == _list.get_name():
				return _list.get_entries()

		raise KeyNotFoundError(name)

	def get_dictionary(self, name = None):
		"""
		Returns a dictionary type of entries specified in a Dictionary object.

		@param name: The name of the Dictionary.

		@return: A dict.

		@raise InvalidParameterError: If the name is not a non-empty string.
		@raise KeyNotFoundError: If no List of the specified name is defined locally to the command.
		"""

		if None == name:
			return {}

		if "" == name:
			raise InvalidParameterError("name", "Must not be empty")

		for dictionary in self.__dictionaries:
			if name == dictionary.get_name():
				return dictionary.get_entries()

		raise KeyNotFoundError(name)

	def execute(self, project):
		"""
		Selects the appropriate execute method based on the type of the source and destination servers.

		@param project: An instance of a project which has defined in it the available servers.

		@rtype: Boolean
		@return: True on success.

		@raise ExecuteCommandError: When execution throws an exception, with the error message as sent from the thrown exception.
		"""

		servers = project.get_servers()

		if None != self.source:
			if True == servers.has_server(self.source):
				source_type = servers.get_server(self.source).get_medium()
			else:
				raise ServerNotDefinedError(self.source)
		else:
			source_type = None

		if None != self.destination:
			if True == servers.has_server(self.destination):
				destination_type = servers.get_server(self.destination).get_medium()
			else:
				raise ServerNotDefinedError(self.destination)
		else:
			destination_type = None

		try:
			if Server.LOCAL == source_type and Server.LOCAL == destination_type:
				self.execute_local_to_local(project)
			elif Server.LOCAL == source_type and Server.REMOTE == destination_type:
				self.execute_local_to_remote(project)
			elif Server.REMOTE == source_type and Server.LOCAL == destination_type:
				self.execute_remote_to_local(project)
			elif Server.REMOTE == source_type and Server.REMOTE == destination_type:
				self.execute_remote_to_remote(project)
			elif Server.LOCAL == source_type or Server.LOCAL == destination_type:
				self.execute_local(project)
			elif Server.REMOTE == source_type or Server.REMOTE == destination_type:
				self.execute_remote(project)
			elif None == self.source and None == self.destination:
				self.execute_virtual(project)

		except Exception, e:

			raise #ExecuteCommandError(e.message)

	def execute_local(self, project):
		"""
		Used for executing commands that are only specific to the local server, like "system".

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_local_to_local(self, project):
		"""
		Used for executing commands that have a local source and destination, like copying a file between
		two folders on the same local server.

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_local_to_remote(self, project):
		"""
		Used for executing commands that have a local source and a remote destination, like copying a file
		between a folder on the local server and a folder on a remote server.

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_remote(self, project):
		"""
		Used for executing commands that are only specific to a remote server, like "system".

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_remote_to_local(self, project):
		"""
		Used for executing commands that have a remote source and a local destination, like copying a file
		between a folder on a remote server and a folder on the local server.

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_remote_to_remote(self, project):
		"""
		Used for executing commands that have a remote source and destination, like copying a file between
		folders on two different remote servers.

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()

	def execute_virtual(self, project):
		"""
		Can be used for virtual commands like printing on the screen.

		Optionally overridden by the inheritor.
		"""
		raise NotSupportedError()
