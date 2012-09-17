#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.filters.filter import Filter

class FilterChain(object):

	"""
	A FilterChain is an ordered list of Filters that is used to apply it on a stream of data.

	An example FilterChain:

		<filterchain name="filter1">
			<regexfilter pattern="DB_USER" replace="${database.user}" ignoreCase="false" />
			<regexfilter pattern="DB_PASSWORD" replace="${database.password}" />
		</filterchain>
	"""

	"""@__filters: An array of objects each a descendant of Filter."""

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: Identifier name for this FilterChain.
		"""

		if not Validator.validate_non_empty_string(name):
			raise InvalidParameterError("name", "Must be a non-empty string")

		self.__name = name
		self.__filters = []

	def add_filter(self, _filter):
		"""
		Adds a filter to this chain.

		@param _filter: A Filter-descendant object.

		@raise InvalidParameterError: _filter be a class desendant from Filter
		"""

		for parent in _filter.__class__.__bases__:
			if Filter == parent:
				self.__filters.append(_filter)
				return True

		raise InvalidParameterError("_filter", "Must be a class desendant from Filter.")

	def get_name(self):
		"""
		Returns the identifier name of this FilterChain.
		"""
		return self.__name

	def apply_filters_to_file(self, path):
		"""
		Applies the hain of Filters to all the contents of a file.

		@param path: The path of the file to process.

		@raise FileReadError: If an error occurs while reading the file.
		@raise FileWriteError: If an error occurs while writing to the file.
		@raise FilterOnFileProcessingError: If an execution of a filter fails.
		"""

		try:
			handle = open(path, "rw")
			data = handle.read()
		except Exception, e:
			raise FileReadError(path)

		# raise their own exceptions
		try:
			for current_filter in self.__filters:
				data = current_filter.apply_filter(data)
		except Exception:
			raise FilterOnFileProcessingError(path)

		try:
			handle.write(data)
			handle.close()
		except Exception, e:
			raise FileWriteError(path)

		return True

	def apply_filters(self, data):
		"""
		Apply this FilterChain's filters to the passed data.

		@param data: The string data to process.

		@rtype: string
		@return: The processed string.
		"""

		if "" == data or None == data:
			return data

		for _filter in self.__filters:
			data = _filter.apply_filter(data)

		return data
