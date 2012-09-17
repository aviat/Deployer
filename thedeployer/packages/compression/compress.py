#
# Copyright (c) 2008 vimov
#

from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.validator import *
from thedeployer.packages.platform.file import FileObject
import os, zipfile, tarfile

class Compress(object):

	__TAR = 1000
	__ZIP = 1001

	@classmethod
	def compress(cls, source, destination, excludes = None, replace = True, retry = 1):
		'''
		this method compress file or directory into tar or zip file according to the extension of the destination destination

		@param source: the source file to be compressed
		@param destination: the name of the compressed file
		@param exclusion: list of the excluded files from the compressed file
		@param replace: boolean for replacing existing file with the same name
		@param retry: retry count

		@raise InvalidParameterError: if the parameter is not valid
		@raise CompressionNotSupportedError: if the compression method is not defined
		'''

		if not Validator.validate_non_empty_string(source):
			raise InvalidParameterError("source", "source must be non empty string")

		if not Validator.validate_non_empty_string(destination):
			raise InvalidParameterError("destination", "destination must be non empty string")

		if not Validator.validate_boolean(replace):
			raise InvalidParameterError("replace", "replace must be boolean")

		if not Validator.validate_integer(retry):
			raise InvalidParameterError("retry", "retry must be integer")

		if False == os.path.exists(source):
			raise FileNotExistsError(source)

		if os.path.exists(destination):
			if not replace:
				raise FileExistsError, destination

		if destination.endswith('.zip'):
			Compress.__compress_zip(source, destination, excludes, replace, retry)

		elif destination.endswith('.tar'):
			Compress.__compress_tar(source, destination, 'w', excludes, replace, retry)

		elif destination.endswith('.tar.gz'):
			Compress.__compress_tar(source, destination, 'w:gz', excludes, replace, retry)

		elif destination.endswith('.tar.bz2'):
			Compress.__compress_tar(source, destination, 'w:bz2', excludes, replace, retry)
		else:
			raise CompressionNotSupportedError, destination

	@classmethod
	def __compress_tar(cls, source, destination, mode, excludes, replace, retry):
		"""
		compress tar format according to the mode
		"""

		try:
	 	 	tar_file = tarfile.open(destination, mode)
	 		Compress.__add(Compress.__TAR, source, tar_file, excludes, retry)
	 		tar_file.close()
	 	except Exception, e:
			if os.path.exists(destination):
				os.remove(destination)
			raise CompressionError(source, str(e))

	@classmethod
	def __compress_zip(cls, source, destination, excludes, replace, retry):
		"""
		compress zip format
		"""

		try:
			zip_file = zipfile.ZipFile(destination, 'w')
			Compress.__add(Compress.__ZIP, source, zip_file, excludes, retry)
			zip_file.close()
		except Exception, e:
			if os.path.exists(destination):
				os.remove(destination)
			raise CompressionError(source, str(e))

	@classmethod
	def __add(cls,compresstype, source, archive, excludes, retry):
		"""
		if the source is file the function add file will be called else add directory will be called
		"""

		if os.path.isdir(source):
			return Compress.__add_dir(compresstype, source, archive, os.path.basename(source), excludes, retry)
		else:
			return Compress.__add_file(compresstype, source, archive, '', retry)
		  	

	@classmethod
	def __add_dir(cls,compresstype, source, archive, arcname, excludes, retry):
		"""
		add directory to the archive
		"""

		filenames = os.listdir(source)
		for filename in filenames:

			file_path = source + os.sep + filename
			newarcname = arcname + os.sep + filename

			if os.path.isdir(file_path):
				if not (excludes is not None and excludes.match(file_path, filename, FileObject.DIRECTORY)):
					Compress.__add_dir(compresstype, file_path, archive, newarcname, excludes, retry)
			else:
				if not (excludes is not None and excludes.match(file_path, filename, FileObject.FILE)):				
					Compress.__add_file(compresstype, file_path, archive, newarcname, retry)

	@classmethod
	def __add_file(cls, compresstype, source, archive, arcname, retry):
		"""
		add file to the archive according to the archive type
		"""
		while retry > 0:
			retry = retry - 1
			try:
				if compresstype == Compress.__ZIP:
					archive.write(source, arcname)
				elif compresstype == Compress.__TAR:
					archive.add(source, arcname)
				return 
			except Exception, e:
				if retry == 0:
					raise
