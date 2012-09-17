#
# Copyright (c) 2008 vimov
#

import logging
import sys
import traceback

class AppLogger(logging.getLoggerClass()):

	"""
	Custom logging class for use application-wide.
	"""

	"""@NOTSET: NOTSET error level."""
	"""@DEBUG: DEBUG error level."""
	"""@INFO: INFO error level."""
	"""@WARNING: WARNING error level."""
	"""@ERROR: ERROR error level."""
	"""@CRITICAL: CRITICAL error level."""

	NOTSET = logging.NOTSET
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL

	"""@line_format: The line format of each log entry."""
	"""@date_format: The date format used in each log entry line."""
	"""@file_mode: The mode to use in openning the log file."""

	line_format = "%(asctime)s %(levelname)s %(message)s"
	date_format = "%a, %d %b %Y %H:%M:%S"
	file_mode = "a+"
	name = ''

	"""@__is_verbose: If True, prints the backtrace to stdout."""
	"""@__logging_level: Logged messages also have levels of importance associated with them. The default levels provided are DEBUG, INFO, WARNING, ERROR and CRITICAL."""
	__is_verbose = False
	__logging_level = None

	def __init__(self, name):
		"""
		Constructor for the class.

		@param name: The logger's name. The name is typically a dot-separated hierarchical name like "a",
		"a.b" or "a.b.c.d".
		"""
		super(logging, self).__init__(name)

	@classmethod
	def initialize(cls, log_file_path, logging_level, is_verbose = False):
		"""
		Initializes the logging class.

		@param log_file_path: The path of the log file.
		@param logging_level: Logged messages also have levels of importance associated with them. The default levels provided are DEBUG, INFO, WARNING, ERROR and CRITICAL.
		@param is_verbose: If True, prints the backtrace to stdout.

		@rtype: String
		@return: A 0-length string on success, an error message on failure.
		"""

		# check log level
		if AppLogger.DEBUG != logging_level and AppLogger.INFO != logging_level \
		and AppLogger.WARNING != logging_level and AppLogger.ERROR != logging_level \
		and AppLogger.CRITICAL != logging_level:
			return "Error level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL."

		# set the configuration
		try:
			logging.basicConfig(format = AppLogger.line_format,
				datefmt = AppLogger.date_format,
				filemode = AppLogger.file_mode,
				filename = log_file_path,
				level = logging_level)
		except Exception, e:
			return 'Cannot open the log file "%s" for writing.' % (log_file_path)

		# set the verbosity level and logging level
		AppLogger.__is_verbose = is_verbose
		AppLogger.__logging_level = logging_level

		# success
		return ""

	@classmethod
	def debug(cls, message):
		"""
		Add a debug message to the log file.

		@param message: The message to add to the log file.
		"""

		logging.debug(message)

		#if True == AppLogger.__is_verbose and AppLogger.DEBUG == AppLogger.__logging_level:
		#	print message

	@classmethod
	def info(cls, message):
		"""
		Add an information message to the log file.

		@param message: The message to add to the log file.
		"""

		logging.info(message)

		#if True == AppLogger.__is_verbose and AppLogger.INFO >= AppLogger.__logging_level:
		#	print message

	@classmethod
	def warning(cls, message):
		"""
		Add a warning message to the log file.

		@param message: The message to add to the log file.
		"""

		logging.warning(message)

		#if True == AppLogger.__is_verbose and AppLogger.WARNING >= AppLogger.__logging_level:
		#	print message

	@classmethod
	def error(cls, message):
		"""
		Add an error message to the log file.

		@param message: The message to add to the log file.
		"""

		logging.error(message)

		#if True == AppLogger.__is_verbose and AppLogger.ERROR >= AppLogger.__logging_level:
		#	print message

	@classmethod
	def critical(cls, message):
		"""
		Add a critical message to the log file.

		@param message: The message to add to the log file.
		"""

		logging.critical(message)

		#if True == AppLogger.__is_verbose and AppLogger.CRITICAL >= AppLogger.__logging_level:
		#	print message

class AppBacktrace:

	"""Provides the ability to write the backtrace to a file. Not for use by modules, but rather, only by the
	CustomError exception class.
	"""

	"""@backtrace_file_path: The path of the backtrace file."""
	__backtrace_file_path = ""

	"""@is_verbose: If True, prints the backtrace to stdout."""
	__is_verbose = False

	def __init__(self):
		"""Not allowed."""
		raise NotSupportedError()

	@classmethod
	def initialize(cls, backtrace_file_path, is_verbose = False):
		"""
		Initializes the backtrace class.

		@param backtrace_file_path: The path of the backtrace file to write to.
		@param is_verbose: If True, prints the backtrace to stdout.

		@rtype: String
		@return: A 0-length string on success, an error message on failure.
		"""

		try:
			handle = open(backtrace_file_path, "a")
			handle.close()
		except Exception, e:
			return 'Cannot open the backtrace file "%s" for writing.' % (backtrace_file_path)

		AppBacktrace.__backtrace_file_path = backtrace_file_path
		AppBacktrace.__is_verbose = is_verbose

		# success
		return ""

	@classmethod
	def write(cls):
		"""
		Adds the backtrace to the backtrace log file. This function is only used by the CustomError exception
		class, and is not intended to be called by other modules.
		"""

		if "" != AppBacktrace.__backtrace_file_path:

			try:
				file_handle = open(AppBacktrace.__backtrace_file_path, "w")
				traceback.print_tb(sys.exc_info()[2], None, file_handle)
				file_handle.close()

			except Exception, e:
				raise

		#if True == AppBacktrace.__is_verbose:
			#print traceback.print_tb(sys.exc_info()[2])
