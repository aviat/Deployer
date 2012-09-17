#!/usr/bin/env python
#
# Copyright (c) 2008 vimov
# 

try:
	# python standard library imports
	from sftpclient import Sftp
	from ftpclient import Ftp
	from unittest import *
	import sys
	import os
	# make life easier
	sys.path.append("../../libs")
	sys.path.append("../../packages")



except Exception, e:

	print 'An exception was thrown: %s: %s' % (e.__class__, e)
	sys.exit(1)


#########################################
# Constants
########################################
HOST = 'localhost'
USERNAME = 'ftp'
PASSWORD = 'ftp'
PORT = 21101
SERVER_PATH = '/home/ftp/' # must ends with /
PATH = '/home/leaf/Documents/'

#######################################
# Static Methods
#######################################

def makeTree():
	path = PATH + 'test/'
	if os.path.exists(path):
		return path
	os.mkdir(path)
	for i in range(1,5):
		for j in range (1,5):
			os.makedirs(path + str(i) + '/' + str(i)+ '-' +str(j) + '/' )
			for k in range (1,5):
				makeFile(path + str(i) + '/' +str(i)+ '-' + str(j) + '/' + str(k) + '.txt')
	return path

def makeEmptyTree():
	path = PATH + 'test/'
	os.mkdir(path)
	for i in range(1,5):
		for j in range (1,5):
			os.makedirs(path + str(i) + '/' + str(i)+ '-' +str(j) + '/' )
	return path


def makeFile(name):
	f = open(name , 'w')
	f.write('This is test file : ' + name)
	f.close()
	return name
	
def makeEmptyDir(name):
	os.makedirs(name)

def remove(path):
	if os.path.isdir(path):
		cont_list = os.listdir(path)
		for item in cont_list:
			if os.path.isdir(path +'/'+ item):
				remove(path +'/'+ item + '/')
			else:
				os.remove( path +'/'+ item )
		os.rmdir(path)
	else:
		os.remove(path)

#######################################
# Test Class
#######################################

class TestFtpClient (TestCase):

	def setUp(self):
#		self.ftp_client = Sftp(HOST, USERNAME, PASSWORD, PORT)
		self.ftp_client = Ftp(HOST, USERNAME, PASSWORD, PORT)
		if not self.ftp_client.connect():
			self.fail('self.failed to connect')

	def tearDown(self):
		if not self.ftp_client.close():
			self.fail('self.failed to close connection')
	
	def test_upload(self):
		
		#Test uploading Directory tree non-recusively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = False)
		self.assertEqual(result , True, 'Error in uploding non-recursively')
		result = self.ftp_client.delete('test', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: False)')
		remove(local_path)
		
		
		#Test uploading Directory tree recusively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		
		#Test uploading Empty directory tree recusively
		local_path = makeEmptyTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding empty tree recursively')
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded empty tree (recurse: True)')
		
		#Test uploading a file
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file')
		result = self.ftp_client.delete('test.txt')
		self.assertEqual(result, True, 'Error in Deleting uploaded file')
		
		#Test uploading a file with setting upoading recusive
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file (2)')
		result = self.ftp_client.delete('test.txt')
		self.assertEqual(result, True, 'Error in Deleting uploaded file (2)')
		
		#Test uploading Nonexisting Directory
		local_path = PATH + 'nonexist/'
		result = self.ftp_client.upload(local_path, '', recursive = True)
		self.assertEqual(result , False, 'Error in uploding non-existing files')
		
		#Test uploading Directory tree that is already exist on servers
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding Directory that exists on the server')
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		

	def test_delete(self):
		#Test Deleting non-existant directory
		result = self.ftp_client.delete('nonexist/', recursive = True)
		self.assertEqual(result, False, 'Error in Deleting Non-existing directory')
		#Test Deleting Directory Tree recursively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting Directory Tree recursively')
		#Test Deleting Non-empty Directory non-recursively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, SERVER_PATH, recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.delete(SERVER_PATH + 'test/', recursive = False)
		self.assertEqual(result, True, 'Error in Deleting Non-empty Directory Tree non-recursively')
		result = self.ftp_client.delete(SERVER_PATH + 'test/', recursive = True)
		#Test Deleting file
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file')
		result = self.ftp_client.delete('test.txt')
		self.assertEqual(result, True, 'Error in Deleting file')
	
	def test_get(self):
		#Test Downloading non existing directory
		result = self.ftp_client.get(PATH, 'nonexist/', recursive = True)
		self.assertEqual(result , None, 'Error in Downloading non-existing directory')
		
		
		#Test Downloading Directory tree recusively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.get(PATH, 'test/', recursive = True)
		self.assertEqual(result.get_path(), PATH + 'test', 'Error in Getting Directory Tree (recurse: True)')
		remove(result.get_path())
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Getting Directory Tree (recurse: True)')
		
		
		#Test Bownloading Directory non-recursively
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.get(PATH, 'test/', recursive = False)
		self.assertEqual(result.get_path(), PATH + 'test', 'Error in Getting Directory Tree (recurse: False)')
		cont = os.listdir(result.get_path() )
		if cont:
			remove(result.get_path())
			self.fail('Error in Getting Directory Tree non-recursively')
		remove(result.get_path())
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		
		
		#Test Downloading file
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file')
		result = self.ftp_client.get(PATH, 'test.txt', recursive = True)
		self.assertEqual(result.get_path(), PATH + 'test.txt', 'Error in Downloading file')
		remove(result.get_path())
		result = self.ftp_client.delete('test.txt')
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		
		
		#Test Downloading Directory Tree in non-existing local path (should be created automaticly)
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding recursively')
		result = self.ftp_client.get(PATH + 'downtest/downtest2/', 'test/', recursive = True)
		self.assertEqual(result.get_path(), PATH + 'downtest/downtest2/test', 'Error in Getting Directory Tree (recurse: True)')
		remove(result.get_path() )
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		
		
		#Test Downloading file in path have no permisions to write
		os.mkdir(PATH + 'permtest/')
		os.chmod(PATH + 'permtest/', 0444)
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file')
		result = self.ftp_client.get(PATH + 'permtest/', 'test.txt', recursive = True)
		self.assertEqual(result, None, 'Error in Downloading file in a path have no permisions to write')
		result = self.ftp_client.delete('test.txt', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		os.chmod(PATH + 'permtest/', 0777)
		remove(PATH + 'permtest/')
		
	def test_chmod(self):
		
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		self.assertEqual(result , True, 'Error in uploading recursively')
		remove(local_path)
		
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploading file')
		
		#Test chmod non-existing file
		result = self.ftp_client.chmod('non-exist/', 777)
		self.assertEqual(result, False, 'Error in chmod non-existing directory')
		
		#Test chmod Directory
		result = self.ftp_client.chmod('test/', 777)
		self.assertEqual(result, True, 'Error in chmod a directory')
		
		#Test chmod file
		result = self.ftp_client.chmod('test.txt', 666)
		self.assertEqual(result, True, 'Error in a file')
		
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		result = self.ftp_client.delete('test.txt', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
	
	def test_list_dir(self):
		
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding non-recursively')
		
		local_path = makeFile(PATH + 'test.txt')
		result = self.ftp_client.upload(local_path, '')
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding file')
		
		#Test list dir
		result = self.ftp_client.list_dir()
#		self.assertEqual(len(result) , 2, 'Error in listing directory')
		
		self.ftp_client.chdir(SERVER_PATH + 'test/')
		result = self.ftp_client.list_dir()
#		self.assertEqual(len(result) , 4, 'Error in listing directory')
		
		
		result = self.ftp_client.delete(SERVER_PATH + 'test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
		result = self.ftp_client.delete(SERVER_PATH + 'test.txt', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
	
	def test_cdup(self):
		local_path = makeTree()
		result = self.ftp_client.upload(local_path, '', recursive = True)
		remove(local_path)
		self.assertEqual(result , True, 'Error in uploding non-recursively')
		
		#Test Parent when on root
		result = self.ftp_client.cdup() #go to home
		self.assertEqual(result , True, 'Error in getting parent directory when on root')
		self.assertEqual(self.ftp_client.get_cwd().rstrip(os.sep), os.path.dirname(SERVER_PATH.rstrip(os.sep)), 'Error in getting parent directory when on root')
		
		#Test Parent when in a dir
		self.ftp_client.chdir(SERVER_PATH + 'test/')
		self.assertEqual(self.ftp_client.get_cwd(), SERVER_PATH +'test', 'Error in getting parent directory')
		result = self.ftp_client.cdup()
		self.assertEqual(result , True, 'Error in getting parent directory')
		self.assertEqual(self.ftp_client.get_cwd().rstrip(os.sep), SERVER_PATH.rstrip(os.sep), 'Error in getting parent directory')
		
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting uploaded files (recurse: True)')
	
	def test_create_path(self):
		#Test creating non-existing path
		result = self.ftp_client.create_path('test/test1/test2')
		self.assertEqual( result, 'test/test1/test2', 'Error in creating server path')
		
		#Test creating existing path
		result = self.ftp_client.create_path('test/test1/test2')
		self.assertEqual( result, 'test/test1/test2', 'Error in creating non-exsiting server path')
		
		result = self.ftp_client.delete('test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting created server path (recurse: True)')
	
	def test_mkdir(self):
		#Test create dir with absolute path
		result = self.ftp_client.mkdir('test/')
		self.assertEqual(result, True, 'Error in making directory with absolute path')
		result = self.ftp_client.mkdir('test/test1')
		self.assertEqual(result, True, 'Error in making directory with absolute path')
		result = self.ftp_client.mkdir('test/test1/test2')
		self.assertEqual(result, True, 'Error in making directory with absolute path')
		
		#Test create dir with relative path
		result = self.ftp_client.chdir('test/test1/test2/')
		result = self.ftp_client.mkdir('test3/')
		self.assertEqual(result, True, 'Error in making directory with relative path')
		
		#Test create an existing dir
		result = self.ftp_client.mkdir('test3/')
		self.assertEqual(result, False, 'Error in making existing directory with relative path')
		
		#Test create a dir in non-existing path
		result = self.ftp_client.mkdir(SERVER_PATH + 'nonexist/test3/')
		self.assertEqual(result, False, 'Error in making a dir in non-existing path')
		
		result = self.ftp_client.delete(SERVER_PATH + 'test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting created server path (recurse: True)')
		
	
	def test_rename(self):
		
		result = self.ftp_client.create_path('test/test1/test2')
		self.assertEqual( result, 'test/test1/test2', 'Error in creating server path')
		
		#Test rename a dir with absolute path
		result = self.ftp_client.rename('test/test1/', 'test/modtest')
		self.assertEqual(result, True, 'Error in renaming directory with absolute path')
		
		#Test rename with relative path
		result = self.ftp_client.chdir('test/')
		result = self.ftp_client.rename('modtest/', 'test1')
		self.assertEqual(result, True, 'Error in renaming directory with relative path')
		
		#Test rename non-Existing file
		result = self.ftp_client.rename('modtest/', 'test1')
		self.assertEqual(result, False, 'Error in renaming non-Existing dir')
		
		#Test passing inconsistant absolute path (oldpath, newpath) to rename methos
		result = self.ftp_client.rename(SERVER_PATH + 'test/test1/', SERVER_PATH + 'tester/modtest')
		self.assertEqual(result, False, 'Error in renaming with inconsistant absolute path')
		
		result = self.ftp_client.delete(SERVER_PATH + '/test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting created server path (recurse: True)')
		
	def test_chdir(self):
		result = self.ftp_client.create_path('test/test1/test2')
		self.assertEqual( result, 'test/test1/test2', 'Error in creating server path')
		
		result = self.ftp_client.create_path('antest/test1/test2')
		self.assertEqual( result, 'antest/test1/test2', 'Error in creating server path')
		
		#Test chdir with raltive path
		result = self.ftp_client.chdir('test/')
		result = self.ftp_client.chdir('test1/test2')
		self.assertEqual(result, True, 'Error in chdire with relative path')
		self.assertEqual(self.ftp_client.get_cwd(), SERVER_PATH + 'test/test1/test2', 'Error in chdire with relative path')
		
		#Test chdir with absolute path
		self.ftp_client.cdup()
		self.ftp_client.cdup()
		self.ftp_client.cdup()
		result = self.ftp_client.chdir('test/test1/test2')
		self.assertEqual(result, True, 'Error in chdire with absolute path')
		
		#Test chdir for non-existing child
		result = self.ftp_client.chdir('test/test1/test2/test3/test4/')
		self.assertEqual(result, False, 'Error in chdire with absolute path')
		
		#Test chdir for non-child
		self.ftp_client.cdup()
		result = self.ftp_client.get_cwd()
		self.assertEqual(result, SERVER_PATH + 'test/test1', 'Error (not expected working directory)')
		result = self.ftp_client.chdir(SERVER_PATH + 'antest/test1/test2')
		self.assertEqual(result, True, 'Error in chdire for non-child')
		
		result = self.ftp_client.delete(SERVER_PATH + 'test/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting created server path (recurse: True)')
		result = self.ftp_client.delete(SERVER_PATH + 'antest/', recursive = True)
		self.assertEqual(result, True, 'Error in Deleting created server path (recurse: True)')
	

##########################################################################
# main method
##########################################################################
def main():

	suite = TestSuite()
	suite.addTest(makeSuite(TestFtpClient))

	runner = TextTestRunner(verbosity = 2)
	runner.run(suite)

if __name__ == '__main__':
	main()
