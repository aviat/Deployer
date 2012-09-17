#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *

class DepFileFactory(object):

	"""
	Factory for creating instances of objects that correspond to nodes in the DepFile tree.
	"""

	__commands_map = {}

	def __init__(self):
		"""
		This is an abstract class and cannot be constructed.
		"""

		raise NotSupportedError()

	@classmethod
	def initialize(cls, commands_map_file_path):
		"""
		Initializes the __commands_map object by processing the commands_map_file_path.

		The format of each line in the commands map file is as follows:
		[#][<empty>|<spaces>|<tabs>][tag_name;module_path;class_name]

		The following four lines represent an example part of a commands map file:

		project;thedeployer.packages.depfile.project;Project
		  filesets;thedeployer.packages.depfile.fileset;FileSets
		# some comment
		# filesets;thedeployer.packages.depfile.fileset;FileSets

		This will be loaded into a dictionary as follows:
			{
				"project": ["thedeployer.packages.depfile.project", "Project"],
				"filesets": ["thedeployer.packages.depfile.fileset", "FileSets"]
			}

		@param commands_map_file_path: The path of the commands map file.

		@raise ConfigFileParsingError: If it failed to parse the commands map file.
		"""

		try:
			filehandle = open(commands_map_file_path, "r")
			filelines = filehandle.readlines()
		except Exception:
			raise FileReadError(commands_map_file_path)

		i = 0
		for line in filelines:

			i = i + 1
			line = line.strip(" \t\r\n")

			if 0 < len(line) and not line.find("#") == 0:

				tokens = line.split(";")

				if len(tokens) != 3:
					raise ConfigFileParsingError("Error in parsing line number " + str(i) + " " + line)
				else:
					DepFileFactory.__commands_map[tokens[0].strip()] = [tokens[1].strip(), tokens[2].strip()]

		

	@classmethod
	def get_object(cls, tag_name, tag_attributes, project, cl_arguments):
		"""
		Creates an instance of the object associated with the tag name "tag_name".
		
		@param tag_name: The name of the newly opened tag.
		@param tag_attributes: The attributes associated with the tag.
		@param project: An instance of a Project, sent as None the first time get_object is called when supposedly it is asked to create an instance of Project.
		@param cl_arguments: A dictionary of the command line arguments sent, excluding application options (like -v)

		@raise DepFileParsingError if the specified tag name was not found, cannot be in this place, or the
		attributes are invalid/missing.
		"""

		tag_name = tag_name.lower()
		
		if DepFileFactory.__commands_map.has_key(tag_name):

			classname = DepFileFactory.__commands_map[tag_name][1]
			pathname = DepFileFactory.__commands_map[tag_name][0]

			exec "from %s import %s" %(pathname, classname)

			if tag_name == 'project':
				exec "created_object = %s.get_instance(None, tag_attributes)" % classname
			else:
				exec "created_object = %s.get_instance(project, tag_attributes)" % classname

			return created_object
		else:
			raise DepFileParsingError('The declared tag "%s" is not supported.' % (tag_name))

