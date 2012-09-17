#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.clients.abstractclient import *

class SqlClient(AbstractClient):

	def __init__(self):
		"""
		This is an abstract class and cannot be instantiated directly.
		"""

		if self.__class__ == SqlClient:
			raise NotSupportedError()

	def create_db(self):
		pass

	def drop_db(self):
		pass

	def select(self):
		pass

	def execute_sql(self):
		pass

	def dump(self):
		pass

	def _import(self):
		pass