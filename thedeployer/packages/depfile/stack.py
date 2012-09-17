#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *

class Stack(object):
	
	def __init__(self):
		self.stack = []
		
	def push(self, object):
		self.stack.append(object)

	def pop(self):
		if len(self.stack) == 0:
			raise StackEmptyError()
		obj = self.stack[-1]
		del self.stack[-1]
		return obj
	
	def get_top(self):
		if len(self.stack) == 0:
			raise StackEmptyError()
		return self.stack[-1]
	
	def is_empty(self):
		if len(self.stack) == 0:
			return True
		return False

	def __len__(self):
		return len(self.stack)
	
	def length(self):
		return self.__len__()
	
	def __str__(self):
		return str(self.stack)