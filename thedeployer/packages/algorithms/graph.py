#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *

class GraphNode(object):
	
	def __init__(self):
		if self.__class__ == DepFileNode:
			raise NotSupportedError()
	
	def get_name(self):
		raise NotImplementedError()
	
	def get_depends(self):
		raise NotImplementedError()

def solve_graph(nodes):

	ret_dict = []
	roots = []
	count = 0

	for node in nodes:
		if node.get_depends() == "":
			roots.append(node)
			
	if len(roots) == 0:
		raise DependencyCycleError
	
	for root in roots:

		alist = []
		alist.append(root)
		count += 1

		for item in alist:

			for node in nodes:
				if item.get_name() == node.get_depends():
					alist.append(node)
					count += 1

		ret_dict.append(alist)

	if count < len(nodes):
		raise DependencyCycleError

	return ret_dict
