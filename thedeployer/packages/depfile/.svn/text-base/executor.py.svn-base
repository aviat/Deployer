#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.logger import *

from thedeployer.packages.depfile.project import *

class DepFileExecutor:

	@classmethod
	def execute(cls, project):
		"""
		Execute all the targets in a project.

		@param project: An instance of Project, represents a DepFile.

		@rtype: Booean.
		@return: True on success.

		@raise CustomException: Raises a descendant of CustomException on error which can vary depending on
			the nature of the error.
		"""

		if Project != project.__class__:
			raise InvalidParameterError("project", "Must be an instance of Project.")

		AppLogger.info("Deploying project \"" + project.get_name() + "\".")
		
		for target_list in project.get_targets(True):

			for target in target_list:

				for task_list in target.get_tasks(True):

					for task in task_list:
	
						AppLogger.info("Processing task \"%s\" in target \"%s\"." % (task.get_name() , target.get_name()))
						
						for command in task.get_commands():
							command.execute(project)
