#
# Copyright (c) 2008 vimov
#
import zipfile, tarfile, os

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.validator import *

class Decompress(object):
	
	@classmethod
	def decompress(cls, file_path, destination, replace = True, retry = 1):
		'''
		decompress file or directory
		
		@param file_path: the path of the file to be compressed
		@param destination: the destination of the compressed file
		@param replce: boolean for replace the file or the directory if exist
		
		@raise InvalidParameterError: If the required argument(s) are not specified. 
		@raise CompressionNotSupportedError: if the type of the file to be compressed is not defined
		'''
		
		if not Validator.validate_non_empty_string(file_path):
			raise InvalidParameterError("file_path", "file_path can not be None or empty string")
		
		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination can not be None or empty string")

		if not Validator.validate_integer(replace):
			raise InvalidParameterError("retry", "retry must be integer")
		
		if not Validator.validate_boolean(replace):
			raise InvalidParameterError("replace", "replace must be boolean")

		if False == os.path.exists(destination):
			raise FileNotExistsError(destination)

		if zipfile.is_zipfile(file_path):
			Decompress.__decompress_zip(file_path, destination, replace, retry)
		elif tarfile.is_tarfile(file_path):
			Decompress.__decompress_tar(file_path, destination, replace, retry)
		else:
			raise DecompressionNotSupportedError, file_path

	
	@classmethod
	def __decompress_zip(cls, file_path, destination, replace = True, retry = 1):
		'''
		decompress zip archive
		'''

		while retry > 0:
			retry = retry - 1
			try:
				end = False
				zip_file = zipfile.ZipFile(file_path, 'r')
				infolist = zip_file.infolist()
	
				for fileinfo in infolist:
					
					filename = fileinfo.filename
					fullfilepath =  destination + os.sep + filename
					fileparent = os.path.dirname(fullfilepath)
		
					if not os.path.exists(fileparent):
						os.makedirs(fileparent, 0755)
	
					if not os.path.exists(fullfilepath):
						f = open(fullfilepath, 'wb')
						f.write(zip_file.read(filename))
						f.close()
					elif False == replace:
						raise FileExistsError(fullfilepath)

			except Exception, e:
				if retry == 0:
					raise
	
	@classmethod
	def __decompress_tar(cls, file_path, destination, replace = True, retry = 1):
		'''
		decompress tar archive
		note: always replaces
		'''

		while retry > 0:
			retry = retry - 1
			try:
				mode = "r"
				if file_path.endswith('.tar'):
					mode = "r"
				elif file_path.endswith('.tar.gz'):
					mode = "r:gz"
				elif file_path.endswith('.tar.bz2'):
					mode = "r:bz2"
				else:
					raise DecompressionNotSupportedError, file_path
				
				tar_file = tarfile.open(file_path, mode)
				tar_file.extractall(destination)
				tar_file.close()
	
			except Exception, e:
				if retry == 0:
					raise
		
