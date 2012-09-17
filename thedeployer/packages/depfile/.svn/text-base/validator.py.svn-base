#
# Copyright (c) 2008 vimov
#

import re

from thedeployer.packages.customexceptions import *

class Validator(object):

	@classmethod
	def validate(cls, value, type):

		if type == "variable_name":
			return Validator.validate_variable_name(value)
		elif type == "boolean":
			return Validator.validate_boolean(value)
		elif type == "integer":
			return Validator.validate_integer(value)
		elif type == "float":
			return Validator.validate_float(value)
		elif type == "string":
			return Validator.validate_string(value)
		elif type == "non_empty_string":
			return Validator.validate_non_empty_string(value)
		elif type == "email":
			return Validator.validate_email(value)
		elif type == "domain":
			return Validator.validate_domain(value)
		elif type == "port":
			return Validator.validate_port(value)
		elif type == "url":
			return Validator.validate_url(value)
		else:
			raise ValidationTypeError, type

	@classmethod
	def validate_variable_name(cls, value):

		if False == Validator.validate_non_empty_string(value):
			return False
		
		pattern = re.compile("^[A-Za-z0-9\._-]+$")
		if None == pattern.match(value):
			return False

		return True

	@classmethod
	def validate_boolean(cls, value):

		if bool != type(value):
			return False
		return True

	@classmethod
	def validate_integer(cls, value):

		try:
			string = str(value)
			if -1 != string.find("."): # it is a float.
				return False
			
			value = int(value)
			return True

		except Exception, e:
			return False

	@classmethod
	def validate_float(cls, value):

		try:
			float(value)
			return True

		except Exception, e:
			return False

	@classmethod
	def validate_string(cls, value):

		try:
			if str != type(value) and unicode != type(value):
				return False

			return True

		except Exception, e:
			return False

	@classmethod
	def validate_non_empty_string(cls, value):
		if str != type(value) and unicode != type(value):
			
			return False

		if 0 != len(value):
			return True
		else:
			return False

	@classmethod
	def validate_email(cls, value):

		if False == validate_non_empty_string(value):
			return False

		pattern = re.compile("^((?:(?:(?:[a-zA-Z0-9][\.\-\+_]?)*)[a-zA-Z0-9])+)\@((?:(?:(?:[a-zA-Z0-9][\.\-_]?){0,62})[a-zA-Z0-9])+)\.([a-zA-Z0-9]{2,6})$")
		if None == pattern.match(value):
			return False

		return True
	
	@classmethod
	def validate_domain(cls, value):

		if not Validator.validate_non_empty_string(value):
			return False
		if re.match(r'(http(s)?://(.)*)|(.*/.*)|(.*:.*)n', value):
			return False

		return True
	
	@classmethod
	def validate_port(cls, value):
		
		if not Validator.validate_integer(value):
			return False
		
		if not 0<= value <= 65535:
			return False
		
		return True
	
	@classmethod
	def validate_url(self, value):
		
		if not Validator.validate_non_empty_string(value):
			return False
		
		if not re.match(r'http(s)?://(.)+', value):
			return False
		
		return True
