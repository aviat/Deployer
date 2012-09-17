#!/usr/bin/env python
#
# Copyright (c) 2008 vimov
# 

from thedeployer.packages.customexceptions import * 
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.clients.localclient import LocalClient
from thedeployer.packages.clients.ftpclient import FtpClient
from thedeployer.packages.clients.sftpclient import SftpClient
from thedeployer.packages.platform.file import FileObject
	
try:
	# python standard library imports
	from unittest import *
	import sys
	import os
	# make life easier
	#sys.path.append("../../libs")
	#sys.path.append("../../packages")
	
except Exception, e:

	print 'An exception was thrown: %s: %s' % (e.__class__, e)
	sys.exit(1)


#######################################
# Constants
#######################################
HOST = '192.168.0.6'
USERNAME = 'leaf'
PASSWORD = 'rdc123'
PORT = 22
SERVER_PATH = '/home/leaf'
PATH = "/tmp"
TYPE = "sftpclient"
PLATFORM = Platform.get_current()

#######################################
# Static Methods
#######################################

def make_test_directory(path = PATH):
	platform = Platform.get_current()
	if not os.path.exists(path + platform.get_separator() + "test" + platform.get_separator() + "1"):
		os.makedirs(path + platform.get_separator() + "test" + platform.get_separator() + "1", 0777)
	if not os.path.exists(path + platform.get_separator() + "test" + platform.get_separator() + "2"):
		os.makedirs(path + platform.get_separator() + "test" + platform.get_separator() + "2", 0777)
	make_file(path + platform.get_separator() + "test" + platform.get_separator() + "test.txt")
	make_file(path + platform.get_separator() + "test" + platform.get_separator() + "1" + platform.get_separator() + "test.txt")
	make_file(path + platform.get_separator() + "test" + platform.get_separator() + "2" + platform.get_separator() + "test.txt")

def make_file(name):
	f = open(name , 'w')
	f.write('This is test file : ' + name)
	f.close()
	return name

def remove(path):
	platform = Platform.get_current()
	if os.path.isdir(path):
		cont_list = os.listdir(path)
		for item in cont_list:
			if os.path.isdir(path + platform.get_separator() + item):
				remove(path + platform.get_separator() + item + platform.get_separator())
			else:
				os.remove( path + platform.get_separator() + item )
		os.rmdir(path)
	else:
		os.remove(path)

#######################################
# Test Class
#######################################

class TestFileClient (TestCase):

	def setUp(self):
		self.platform = Platform.get_current()
		
		if "ftpclient" == TYPE:
			self.file_client = FtpClient(PLATFORM, HOST, USERNAME, PASSWORD, PORT, SERVER_PATH)
			try:
				self.file_client.connect()
			except Exception, e:
				self.fail('self.failed to connect')
		
		if "sftpclient" == TYPE:
			self.file_client = SftpClient(PLATFORM, HOST, USERNAME, PASSWORD, PORT)
			try:
				self.file_client.connect()
			except Exception, e:
				self.fail('self.failed to connect')
		
		if "localclient" == TYPE:
			self.file_client = LocalClient()

	def tearDown(self):
		if "ftpclient" == TYPE:
			try:
				self.file_client.disconnect()
			except:
				self.fail('failed to close connection')
				
		if "sftpclient" == TYPE:
			try:
				self.file_client.disconnect()
			except:
				self.fail('failed to close connection')
	
#	def test_chmod(self):
#		
#		#Test uploading Nonexisting Directory
#		path = SERVER_PATH + PLATFORM.get_separator() + 'nonexist'
#		self.assertRaises(CustomError, self.file_client.chmod, path, "777", None, False, True)
#		
#		Destination = SERVER_PATH
#		source = PATH + self.platform.get_separator() + "test"
#		make_test_directory()
#		self.file_client.put(source, Destination, None, False, True, True, True)
#		remove(source)
#		
#		#chmod the directory recursively to "777"
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		self.file_client.chmod(path, "777", None, False, True)
#		result = self.file_client.list(path, None, True)
#		
#		if result[0].get_type() == FileObject.DIRECTORY:
#			child = result[0].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[0].get_permissions() , 0777)
#		
#		if result[1].get_type() == FileObject.DIRECTORY:
#			child = result[1].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[1].get_permissions() , 0777)
#		
#		if result[2].get_type() == FileObject.DIRECTORY:
#			child = result[2].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[2].get_permissions() , 0777)
#		
#		
#		#chmod the directory non-recursively to "755"
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		self.file_client.chmod(path, "755", None, False, False)
#		result = self.file_client.list(path, None, True)
#		
#		if result[0].get_type() == FileObject.DIRECTORY:
#			child = result[0].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[0].get_permissions() , 0777)
#		
#		if result[1].get_type() == FileObject.DIRECTORY:
#			child = result[1].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[1].get_permissions() , 0777)
#		
#		if result[2].get_type() == FileObject.DIRECTORY:
#			child = result[2].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[2].get_permissions() , 0777)
#		
#		
#		#chmod contents only non-recursivle to "755"
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		self.file_client.chmod(path, "755", None, True, False)
#		result = self.file_client.list(path, None, True)
#		
#		if result[0].get_type() == FileObject.DIRECTORY:
#			child = result[0].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[0].get_permissions() , 0755)
#		
#		if result[1].get_type() == FileObject.DIRECTORY:
#			child = result[1].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[1].get_permissions() , 0755)
#		
#		if result[2].get_type() == FileObject.DIRECTORY:
#			child = result[2].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0777)
#		self.assertEqual(result[2].get_permissions() , 0755)
#		
#		
#		#chmod contents only recursivly to "755"
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		self.file_client.chmod(path, "555", None, True, True)
#		result = self.file_client.list(path, None, True)
#		
#		if result[0].get_type() == FileObject.DIRECTORY:
#			child = result[0].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0555)
#		self.assertEqual(result[0].get_permissions() , 0555)
#		
#		if result[1].get_type() == FileObject.DIRECTORY:
#			child = result[1].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0555)
#		self.assertEqual(result[1].get_permissions() , 0555)
#		
#		if result[2].get_type() == FileObject.DIRECTORY:
#			child = result[2].get_childs()
#			self.assertEqual(child[0].get_permissions() , 0555)
#		self.assertEqual(result[2].get_permissions() , 0555)
#		
#		self.file_client.chmod(path, "777", None, False, True)
#		
#		self.file_client.delete(SERVER_PATH + PLATFORM.get_separator() + "test", recursive = True)
#		result = self.file_client.is_exists(SERVER_PATH + PLATFORM.get_separator() + "test")
#		self.assertEqual(result, False)
#	
#	def test_mkdir(self):
#		
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		
#		#test one level mkdir non-recursivley 
#		self.file_client.mkdir(path)
#		result = self.file_client.is_exists(path)
#		self.assertEqual(result, True)
#		
#		#change the path
#		path =  SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test"
#		
#		#test multilevel mkdir non-recursivle
#		self.assertRaises(CustomError, self.file_client.mkdir, path)
#		
#		#test multilevel mkdir non-recursivle
#		self.file_client.mkdir(path, recursive = True)
#		result = self.file_client.is_exists(path)
#		self.assertEqual(result, True)
#		
#		path = SERVER_PATH + PLATFORM.get_separator() + "test"
#		self.file_client.delete(path, recursive = True)
#		result = self.file_client.is_exists(path)
#		self.assertEqual(result, False)
#		
#	
#	def test_list(self):
#		
#		#Test listing non-existing Directory
#		path = SERVER_PATH + PLATFORM.get_separator() + 'nonexist'
#		self.assertRaises(CustomError, self.file_client.list, path, None, True)
#		
#		Destination = SERVER_PATH
#		source = PATH + self.platform.get_separator() + "test"
#		make_test_directory()
#		self.file_client.put(source, Destination, None, False, True, True, True)
#		remove(source)
#		
#		#test list non-recursivly
#		path = SERVER_PATH + PLATFORM.get_separator() + 'test'
#		
#		result = self.file_client.list(path)
#		self.assertEqual(len(result), 3)
#		self.assertEqual(len(result[0].get_childs()), 0)
#		self.assertEqual(len(result[1].get_childs()), 0)
#		self.assertEqual(len(result[2].get_childs()), 0)
#		
#		#test list recursivly
#		result = self.file_client.list(path, recursive = True)
#		self.assertEqual(len(result), 3)
#		self.assertEqual(len(result[0].get_childs()), 1)
#		self.assertEqual((result[0].get_childs())[0].get_name(), "test.txt")
#		self.assertEqual(len(result[1].get_childs()), 1)
#		self.assertEqual((result[1].get_childs())[0].get_name(), "test.txt")
#		self.assertEqual(len(result[2].get_childs()), 0)
#		self.assertEqual(result[2].get_name(), "test.txt")
#		
#		self.file_client.delete(path, recursive = True)
#		result = self.file_client.is_exists(path)
#		self.assertEqual(result, False)
#		
		
#	def test_put(self):
#		
#		#Test uploading Nonexisting Directory
#		source = PATH + self.platform.get_separator() + 'nonexist'
#		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, True, True, True )
#		
#		#Source is File, destination is Directory, All flags False
#		source = PATH + self.platform.get_separator() + 'tmp'
#		make_file(source)
#		Destination = SERVER_PATH
#		
#		self.file_client.put(source, Destination, None, False, False, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "tmp")
#		self.assertEqual(result , True)
#		
#		#Source is File, destination is Directory, All False and file is already exist
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, False)
#		
#		#Source is File, destination is Directory, Replace is True
#		result = self.file_client.put(source, Destination, None, False, False, False, True)
#		
#		#Source is File, Destination is File, All False
#		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, False)
#		
#		#Source is File, Destination is File, Replace True
#		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, True)
#		
#		self.file_client.delete(Destination, None)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result, False, "Erorr in Deleting")
#		
#		#Source is File, Destination is non-exist directory, All False
#		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmpdir"
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, False)
#		 
#		#Source is File, Destination is non-exist directory, make_dirs True
#		result = self.file_client.put(source, Destination, None, False, False, True, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "tmp")
#		self.assertEqual(result , True)
#		remove(source)
#		
#		#Source is Diectory and destination is file, All False
#		Destination = Destination + PLATFORM.get_separator() + "tmp"
#		source = PATH + self.platform.get_separator() + "test"
#		make_test_directory()
#		
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, False)
#		
#		#Source is directory and destination is file, Replace is True
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, True, True, True)
#		
#		Destination = PLATFORM.dirname(Destination)
#		result = self.file_client.delete(Destination, None, False, True)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result, False, "Error in deleting")
#		
#		#Source is directory, Destination is directory, All False
#		Destination = SERVER_PATH
#		
#		result = self.file_client.put(source, Destination, None, False, False, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		
#		#Source is directory, Destination is directory, recursive True, rest is Fasle		
#		result = self.file_client.put(source, Destination, None, False, True, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		#source is File, destination is directory has child directory with the same name of file, replace is True
#		remove(source)
#		make_file(source)
#		
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, True, False, True)
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test" , None, recursive = True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		remove(source)
#		make_test_directory()
#		
#		#Source is Directory, destination is directory, contents_only True, rest False
#		result = self.file_client.put(source, Destination, None, True, False, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test.txt" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "1" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "2" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		#Source is Directory, destination is directory, contents_only and recusive is True, rest is False
#		result = self.file_client.put(source, Destination, None, True, True, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		
#		#Source is Directory, destination is directory, contents_only and recusive is True, rest is False, source is already exist under destination
#		remove(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "test.txt")
#		remove(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "1"  +  self.platform.get_separator() + "test.txt")
#		remove(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "2"  +  self.platform.get_separator() + "test.txt")
#
#		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "test2.txt")
#		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "1"  +  self.platform.get_separator() + "test2.txt")
#		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "2"  +  self.platform.get_separator() + "test2.txt")
#		
#		result = self.file_client.put(source, Destination, None, True, True, False, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test2.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test2.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test2.txt")
#		self.assertEqual(result , True)
#		
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test.txt" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test2.txt" , None)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "1" , None, recursive = True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "2" , None, recursive = True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2")
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		remove(source)
#		
#		
#		#Source is directory, Destination is non-exist directory, All False
#		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmpdir"
#		source = PATH + self.platform.get_separator() + "test"
#		make_test_directory()
#		
#		self.assertRaises(CustomError, self.file_client.put, source, Destination, None, False, False, False, False)
#		
#		#Source is directory, Destination is non-exist directory, make_dirs True , rest False
#		result = self.file_client.put(source, Destination, None, False, False, True, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination, recursive = True)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		
#		#Source is directory, destination is non-exist directory, makedirs and recursive True, rest is Fasle		
#		result = self.file_client.put(source, Destination, None, False, True, True, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination, recursive = True)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		#Source is Directory, destination is directory, make_dirs and contents_only True, rest False
#		result = self.file_client.put(source, Destination, None, True, False, True, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination, recursive = True)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		
#		#Source is Directory, destination is non-exist directory, make_dirs, contents_only and recusive are True, rest is False
#		result = self.file_client.put(source, Destination, None, True, True, True, False)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination, recursive = True)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		#Source is empty directory, destination is non-exist directory, make_dirs, contents_only are True, rest is False
#		remove(source)
#		os.makedirs(source, 0777)
#		
#		result = self.file_client.put(source, Destination, None, True, False, True, False)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , True)
#		
#		result = self.file_client.delete(Destination)
#		result = self.file_client.is_exists(Destination)
#		self.assertEqual(result , False, 'Error in Deleting')
#		
#		remove(source)
#	
#	
#	def test_get(self):
#		
#		if "localclient" != TYPE:
#			local_client = LocalClient()
#			
#			#Test uploading Nonexisting Directory
#			Destination = PATH
#			source = SERVER_PATH + PLATFORM.get_separator() + "nonexist"
#			self.assertRaises(FileNotExistsError, self.file_client.get, source, Destination, None, False, True, True, True )
#			
#			#uploading on server
#			os.mkdir(PATH + self.platform.get_separator() + "tmptest")
#			source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + 'tmp'
#			Destination = SERVER_PATH
#			make_file(source)
#			self.file_client.put(source, Destination, recursive = True)
#			remove(source)
#			source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + "test"
#			make_test_directory(PATH + self.platform.get_separator() + "tmptest")
#			self.file_client.put(source, Destination, None, False, True, True, True)
#			remove(source)
#			
#			#Source is File, destination is Directory, All flags False
#			source = SERVER_PATH + PLATFORM.get_separator() + "tmp"
#			Destination = PATH
#			
#			result = self.file_client.get(source, Destination, None, False, False, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "tmp")
#			self.assertEqual(result , True)
#			
#			#Source is File, destination is Directory, All False and file is already exist
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, False)
#			
#			#Source is File, destination is Directory, Replace is True
#			result = self.file_client.get(source, Destination, None, False, False, False, True)
#			
#			#Source is File, Destination is File, All False
#			Destination = PATH + self.platform.get_separator() + "tmp"
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, False)
#			
#			#Source is File, Destination is File, Replace True
#			Destination = PATH + self.platform.get_separator() + "tmp"
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, True)
#			
#			local_client.delete(Destination, None)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result, False, "Erorr in Deleting")
#			
#			#Source is File, Destination is non-exist directory, All False
#			Destination = PATH + self.platform.get_separator() + "tmpdir"
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, False)
#			 
#			#Source is File, Destination is non-exist directory, make_dirs True
#			result = self.file_client.get(source, Destination, None, False, False, True, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "tmp")
#			self.assertEqual(result , True)
#			
#			self.file_client.delete(source)
#			
#
#			#Source is Diectory and destination is file, All False
#			Destination = Destination + self.platform.get_separator() + "tmp"
#			source = SERVER_PATH + PLATFORM.get_separator() + "test"
#			
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, False)
#			
#			#Source is directory and destination is file, Replace is True
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, True, True, True)
#			
#			Destination = self.platform.dirname(Destination)
#			result = local_client.delete(Destination, None, False, True)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result, False, "Error in deleting")
#			
#			#Source is directory, Destination is directory, All False
#			Destination = PATH
#			
#			result = self.file_client.get(source, Destination, None, False, False, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "test" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			
#			#Source is directory, Destination is directory, recursive True, rest is Fasle		
#			result = self.file_client.get(source, Destination, None, False, True, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "1" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "2" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			#source is File, destination is directory has child directory with the same name of file, replace is True
#			self.file_client.delete(source, None, False, True)
#			tmp_source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + "test"
#			tmp_dest = SERVER_PATH
#			make_file(tmp_source)
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			remove(tmp_source)
#			
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, True, False, True)
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "test" , None, recursive = True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			self.file_client.delete(source, None, False, True)
#			tmp_source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + "test"
#			tmp_dest = SERVER_PATH
#			make_test_directory(PATH + self.platform.get_separator() + "tmptest")
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			remove(tmp_source)
#			
#			#Source is Directory, destination is directory, contents_only True, rest False
#			result = self.file_client.get(source, Destination, None, True, False, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "test.txt" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "1" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "2" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			#Source is Directory, destination is directory, contents_only and recusive is True, rest is False
#			result = self.file_client.get(source, Destination, None, True, True, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			
#			#Source is Directory, destination is directory, contents_only and recusive is True, rest is False, source is already exist under destination
#			self.file_client.delete(SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test.txt")
#			self.file_client.delete(SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1"  +  PLATFORM.get_separator() + "test.txt")
#			self.file_client.delete(SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2"  +  PLATFORM.get_separator() + "test.txt")
#			
#			tmp_source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + "test2.txt"
#			make_file(tmp_source)
#			tmp_dest = SERVER_PATH + PLATFORM.get_separator() + "test"
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			tmp_dest = SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1"
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			tmp_dest = SERVER_PATH + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2"
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			
#			result = self.file_client.get(source, Destination, None, True, True, False, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1" + self.platform.get_separator() + "test2.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2" + self.platform.get_separator() + "test2.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test2.txt")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "test.txt" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "test2.txt" , None)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "1" , None, recursive = True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			result = local_client.delete(Destination + self.platform.get_separator() + "2" , None, recursive = True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2")
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			self.file_client.delete(source, recursive = True)
#			
#			
#			#Source is directory, Destination is non-exist directory, All False
#			Destination = PATH + self.platform.get_separator() + "tmpdir"
#			source = SERVER_PATH + PLATFORM.get_separator() + "test"
#			
#			tmp_source = PATH + self.platform.get_separator() + "tmptest" + self.platform.get_separator() + "test"
#			tmp_dest = SERVER_PATH
#			make_test_directory(PATH + self.platform.get_separator() + "tmptest")
#			self.file_client.put(tmp_source, tmp_dest, recursive = True)
#			remove(tmp_source)
#			
#			
#			self.assertRaises(CustomError, self.file_client.get, source, Destination, None, False, False, False, False)
#			
#			#Source is directory, Destination is non-exist directory, make_dirs True , rest False
#			result = self.file_client.get(source, Destination, None, False, False, True, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination, recursive = True)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			
#			#Source is directory, destination is non-exist directory, makedirs and recursive True, rest is Fasle		
#			result = self.file_client.get(source, Destination, None, False, True, True, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "1" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "2" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination, recursive = True)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			#Source is Directory, destination is directory, make_dirs and contents_only True, rest False
#			result = self.file_client.get(source, Destination, None, True, False, True, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination, recursive = True)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			
#			#Source is Directory, destination is non-exist directory, make_dirs, contents_only and recusive are True, rest is False
#			result = self.file_client.get(source, Destination, None, True, True, True, False)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "1" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "2" + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			result = local_client.is_exists(Destination + self.platform.get_separator() + "test.txt")
#			self.assertEqual(result , True)
#			
#			result = local_client.delete(Destination, recursive = True)
#			result = local_client.is_exists(Destination)
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			
#			result = local_client.delete(source, recursive = True)
#			result = local_client.is_exists(source)
#			self.assertEqual(result , False, 'Error in Deleting')
#			
#			remove(PATH + self.platform.get_separator() + "tmptest")
#	
	def test_move(self):
		
		#Test uploading Nonexisting Directory
		source = SERVER_PATH + PLATFORM.get_separator() + 'nonexist'
		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
		self.assertRaises(FileNotExistsError, self.file_client.move, source, Destination, None, False, True, True )
		
		source = PATH + self.platform.get_separator() + 'tmp'
		Destination = SERVER_PATH
		make_file(source)
		self.file_client.put(source, Destination, recursive = True)
		remove(source)
		source = PATH + self.platform.get_separator() + "test"
		make_test_directory()
		self.file_client.put(source, Destination, None, False, True, True, True)
		remove(source)
		
		#Source is File, destination is Directory, All flags False
		source = SERVER_PATH + PLATFORM.get_separator() + 'tmp'
		Destination = SERVER_PATH + PLATFORM.get_separator() + 'tmpdir'
		self.file_client.mkdir(Destination, "0777", True)
		
		result = self.file_client.move(source, Destination, None, False, False, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "tmp")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , False)
		
		self.file_client.delete(Destination, None, False, True)
		result = self.file_client.is_exists(Destination)
		self.assertEqual(result, False)
		
		tmp_source = PATH + self.platform.get_separator() + 'tmp'
		tmp_dest = SERVER_PATH
		make_file(tmp_source)
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		
		#Source is File, destination is Directory, All False and file is already exist
		Destination = SERVER_PATH
		
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, False)
		
		
		#Source is File, destination is Directory, Replace is True
		result = self.file_client.move(source, Destination, None, False, False, True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "tmp")
		self.assertEqual(result , True)
		
		
		#Source is File, Destination is File, All False
		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, False)
		
		#Source is File, Destination is File, Replace True
		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmp"
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, True)
		

		#Source is File, Destination is non-exist directory, All False
		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmpdir"
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, False)
		 
		#Source is File, Destination is non-exist directory, make_dirs True
		result = self.file_client.move(source, Destination, None, False, True, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "tmp")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result, False)
		
		
		#Source is Diectory and destination is file, All False
		Destination = Destination + PLATFORM.get_separator() + "tmp"
		source = SERVER_PATH + PLATFORM.get_separator() + "test"
		
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, False)
		
		#Source is directory and destination is file, Replace is True
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, True, True)
		
		Destination = PLATFORM.dirname(Destination)
		result = self.file_client.delete(Destination, None, False, True)
		result = self.file_client.is_exists(Destination)
		self.assertEqual(result, False, "Error in deleting")
		

		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmpdir"
		self.file_client.mkdir(Destination, "0777", True)
		
		#Source is directory, Destination is directory, recursive True, rest is Fasle		
		result = self.file_client.move(source, Destination, None, False, False, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
				
		
		#source is File, destination is directory has child directory with the same name of file, replace is True
		
		tmp_source = PATH + self.platform.get_separator() + 'test'
		tmp_dest = SERVER_PATH
		make_file(tmp_source)
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, True, False, True)
		
		self.assertRaises(CustomError, self.file_client.delete, Destination + PLATFORM.get_separator() + "test")
		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test" , None, False, True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test")
		self.assertEqual(result , False, 'Error in Deleting')
		
		self.file_client.delete(source, recursive = True)
		
		tmp_source = PATH + self.platform.get_separator() + 'test'
		tmp_dest = SERVER_PATH
		make_test_directory()
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		
		#Source is Directory, destination is directory, contents_only is True, rest is False
		result = self.file_client.move(source, Destination, None, True, False, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , True)
		
		self.file_client.delete(source, None, False, True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , False)
		
		
		#Source is Directory, destination is directory, contents_only and recusive is True, rest is False, source is already exist under destination
		
		os.makedirs(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "1", 0777)
		os.makedirs(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "2", 0777)
		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "test2.txt")
		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "1" + self.platform.get_separator() + "test2.txt")
		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "2" + self.platform.get_separator() + "test2.txt")

		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "test2.txt")
		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "1"  +  self.platform.get_separator() + "test2.txt")
		make_file(PATH + self.platform.get_separator() + "test" + self.platform.get_separator() + "2"  +  self.platform.get_separator() + "test2.txt")
		
		
		tmp_source = PATH + self.platform.get_separator() + 'test'
		tmp_dest = SERVER_PATH
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		
		result = self.file_client.move(source, Destination, None, True, False, True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test2.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test2.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test2.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , True)
		
		self.file_client.delete(source, None, False, True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , False)
		
		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test.txt" , None)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , False, 'Error in Deleting')
		
		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "test2.txt" , None)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , False, 'Error in Deleting')
		
		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "1" , None, recursive = True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1")
		self.assertEqual(result , False, 'Error in Deleting')
		
		result = self.file_client.delete(Destination + PLATFORM.get_separator() + "2" , None, recursive = True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2")
		self.assertEqual(result , False, 'Error in Deleting')
		
		
		self.file_client.delete(Destination)
		result = self.file_client.is_exists(Destination)
		self.assertEqual(result , False, 'Error in Deleting')
		
		
		#Source is directory, Destination is non-exist directory, All False
		tmp_source = PATH + self.platform.get_separator() + 'test'
		tmp_dest = SERVER_PATH
		make_test_directory()
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		Destination = SERVER_PATH + PLATFORM.get_separator() + "tmpdir"
		source = SERVER_PATH + PLATFORM.get_separator() + "test"
		
		self.assertRaises(CustomError, self.file_client.move, source, Destination, None, False, False, False)
		
		
		#Source is directory, destination is non-exist directory, makedirs True, rest is Fasle	
		result = self.file_client.move(source, Destination, None, False, True, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , False)
		
		
		result = self.file_client.delete(Destination, recursive = True)
		result = self.file_client.is_exists(Destination)
		self.assertEqual(result , False, 'Error in Deleting')
		
		
		#Source is Directory, destination is non-exist directory, make_dirs, contents_only and replace is False
		tmp_source = PATH + self.platform.get_separator() + 'test'
		tmp_dest = SERVER_PATH
		make_test_directory()
		self.file_client.put(tmp_source, tmp_dest, recursive = True)
		remove(tmp_source)
		
		result = self.file_client.move(source, Destination, None, True, True, False)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "1" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "2" + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(Destination + PLATFORM.get_separator() + "test.txt")
		self.assertEqual(result , True)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , True)
		
		self.file_client.delete(source)
		result = self.file_client.is_exists(source)
		self.assertEqual(result , False)
		
		result = self.file_client.delete(Destination, recursive = True)
		result = self.file_client.is_exists(Destination)
		self.assertEqual(result , False, 'Error in Deleting')


		
###########################################################################
## main method
###########################################################################

def main():

	suite = TestSuite()
	suite.addTest(makeSuite(TestFileClient))

	runner = TextTestRunner(verbosity = 2)
	runner.run(suite)

if __name__ == '__main__':
	main()
