#
# Copyright (c) 2008 vimov
#

import re

from thedeployer.packages.customexceptions import *
from thedeployer.packages.filters.filter import Filter

class RegexFilter(Filter):

	"""@__pattern: The regex pattern. Should not contain the heading and trailing slashes."""
	"""@__replace_with: The string to replace the matched string with."""
	"""@__ignore_case: If True, matching will be case-insensitive."""
	"""@__multi_line: the pattern character "^" matches at the beginning of the string and at the beginning of each line (immediately following each newline); and the pattern character "$" matches at the end of the string and at the end of each line (immediately preceding each newline). By default, "^" matches only at the beginning of the string, and "$" only at the end of the string and immediately before the newline (if any) at the end of the string."""

	def __init__(self, pattern, replace_with, ignore_case, multi_line):
		"""
		A regular expression replacement pattern.

		@param pattern: The regex pattern. Should not contain the heading and trailing slashes.
		@param replace_with: The string to replace the matched string with.
		@param ignore_case: If True, matching will be case-insensitive.
		@param multi_line: the pattern character "^" matches at the beginning of the string and at the beginning of each line (immediately following each newline); and the pattern character "$" matches at the end of the string and at the end of each line (immediately preceding each newline). By default, "^" matches only at the beginning of the string, and "$" only at the end of the string and immediately before the newline (if any) at the end of the string.
		"""

		if not Validator.validate_non_empty_string(pattern):
			raise InvalidParameterError("pattern", "Must be a non-empty string")
		if not Validator.validate_string(replace_with):
			raise InvalidParameterError("replace_with", "Must be a string")
		if not Validator.validate_boolean(ignore_case):
			raise InvalidParameterError("ignore_case", "Must be a boolean")
		if not Validator.validate_boolean(multi_line):
			raise InvalidParameterError("multi_line", "Must be a boolean")

		self.__pattern = pattern
		self.__replace_with = replace_with
		self.__ignore_case = ignore_case
		self.__multi_line = multi_line

	def apply_filter(self, data):
		"""
		Called to apply the filter on a string data. Must be implemented by the inheritor.

		@param data: The string data to process.

		@rtype: string
		@return: The processed string.

		@raise FilterProcessingError: If it fails to apply the pattern on the data.
		"""

		options = 0
		if True == self.__ignore_case:
			options = options | re.IGNORECASE
		if True == self.__multi_line:
			options = options | re.MULTILINE

		try:
			regex = re.compile(self.__pattern, options)
			return regex.sub(self.__replace_with, data)

		except Exception, e:
			raise FilterProcessingError()
