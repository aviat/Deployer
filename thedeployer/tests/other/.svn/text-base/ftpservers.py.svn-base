#!/usr/bin/env python
#
# Copyright (c) 2008 vimov
# 

try:
	# python standard library imports
	import unittest

	# make life easier
	sys.path.append("../../libs")
	sys.path.append("../../packages")

	# program specific packages
	#import ftpclient

	# libs
	import paramiko

except Exception, e:

	print 'An exception was thrown: %s: %s' % (e.__class__, e)
	sys.exit(1)


class TestFtpServers(unittest.TestCase):

	def setUp(self):
		return

	def tearDown(self):
		return

	def test_chdir_with_relative_path(self):
		return

	def test_chdir_with_absolute_path(self):
		return


def main():

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestFtpServers))

	runner = unittest.TextTestRunner(verbosity = 2)
	runner.run(suite)

if __name__ == '__main__':
	main()
