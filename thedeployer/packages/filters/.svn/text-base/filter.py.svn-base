#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *

class Filter(object):

	"""
	Interface all Filters must implement.
	"""

	def __init__(self):
		"""
		Constructor for the class.
		"""
		pass

	def apply_filter(self, data):
		"""
		Called to apply the filter on a string data. Must be implemented by the inheritor.

		@param data: The string data to process.

		@rtype: string
		@return: The processed string.

		@raise FilterProcessingError: If it fails to apply the filter.
		"""

		raise NotImplementedError()
