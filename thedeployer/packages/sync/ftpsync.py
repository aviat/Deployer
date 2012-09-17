#
# Copyright (c) 2008 vimov
#
import time
import re
from datetime import datetime

from thedeployer.packages.clients.localclient import LocalClient
from thedeployer.packages.clients.ftpclient import FtpClient
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.depfile.fileset import FileSet
from thedeployer.packages.platform.file import FileObject
from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.server import *
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.logger import AppLogger

def compare(x, y):
	if x.__class__ == FileObject and y.__class__ == FileObject:
		return cmp(x.get_name(), y.get_name())
	
	if x.__class__ == str or y.__class__ == str:
		if x == None:
			return 1
		elif y == None:
			return -1
		else:
			return cmp(x, y)
	
	return cmp(x, y)

class FtpSync(object):
	
	def __init__(self):
		pass
	
	def run(self, source, destination, _from, to, excludes = None, chmod = None, delete = False, retry = 1, test_mode = False):
		"""
		run synchronization process
		
		@param source: source server
		@param destination: destination server
		@param _from: path on source server
		@param to: path on destination server
		@param exclude: instance of FileSet
		@param chmod: value for destination files to be chmoded to
		@param delete: if true any files in destination that is non-exist in source will be deleted
		@param test_mode: if true run in test mode
		
		@rtype: bool
		@return: True on success
		
		@raise InvalidParameterError: If one of the arguments is invalid.
		@raise Other: from localclient methods
		"""

		#validating that source or destination are servers and at least one of them is local server
		if source.__class__ != LocalServer:
			raise InvalidParameterError('source', 'Must be instance of LocalServer class')
		if destination.__class__ != FtpServer:
			raise InvalidParameterError('destination', 'Must be instance of FtpSerevr class')
		if not Validator.validate_non_empty_string(_from):
			raise InvalidParameterError('_from', 'Must be non-empty string')
		if not Validator.validate_non_empty_string(to):
			raise InvalidParameterError('to', 'Must be non-empty string')
		if excludes.__class__ != FileSet and excludes != None:
			raise InvalidParameterError('excludes', 'should be instance of FileSet')
		if not Validator.validate_non_empty_string(chmod) and chmod != None:
			raise InvalidParameterError('chmod', 'should be a string value in form like "0777"')
		if not Validator.validate_boolean(delete):
			raise InvalidParameterError('delete', 'should be boolean value')
		if not Validator.validate_boolean(test_mode):
			raise InvalidParameterError('test_mode', 'should be boolean value')
		
		local_platform = source.get_platform()
		ftp_platform = destination.get_platform()

		if not destination.is_exists(to):

				try:
					destination.mkdir(to)
				except Exception, e:
					raise

		while True:

			try:

				try:	
					local_list = source.list(_from, excludes, False)
					ftp_list = destination.list(to, excludes, False)

				except Exception, e:
					raise #FtSyncError("Error in synchronization over ftp: ", str(e))

				local_list.sort(compare)
				ftp_list.sort(compare)

				#get time difference between local and ftp server
				try:
					tmp_name = "rfXq11fc.ftpservertimetest"
					
					tmp_file = open(_from + local_platform.get_separator() + tmp_name, "w")
					tmp_file.write("test")
					tmp_file.close()

					destination.put(_from + local_platform.get_separator() + tmp_name, to, None, False, True, False, True)
					local_time = time.mktime(datetime.timetuple(datetime.now()))
					ftp_time = time.mktime(datetime.timetuple(destination.get_last_modified_time(to + ftp_platform.get_separator() + tmp_name)))

					if chmod != None:
						destination.chmod(to + ftp_platform.get_separator() + tmp_name, chmod, None, False, True)
							
					
					source.delete(_from + local_platform.get_separator() + tmp_name)
					destination.delete(to + ftp_platform.get_separator() + tmp_name)

					time_diff = local_time - ftp_time

				except Exception, e:

					if source.is_exists(_from + local_platform.get_separator() + tmp_name):
						source.delete(_from + local_platform.get_separator() + tmp_name)
					if destination.is_exists(to + ftp_platform.get_separator() + tmp_name):
						destination.delete(to + ftp_platform.get_separator() + tmp_name)
					raise

				i= 0
				j = 0

				while True:

					local_item = None
					ftp_item = None
					local_item_name = None
					ftp_item_name = None

					if i <= (len(local_list) - 1):
						local_item = local_list[i]
						local_item_name = local_item.get_name()

					if j <= (len(ftp_list) - 1):
						ftp_item = ftp_list[j]
						ftp_item_name = ftp_item.get_name()

					if local_item_name != None or ftp_item_name != None:
						comparison = compare(local_item_name, ftp_item_name)

						if comparison < 0:
							if not test_mode:
								destination.put(local_item.get_path(), to, None, False, True, False, False)
							AppLogger.info("Copying :'" + local_item.get_path() + "', to '" + to + "'")
							if chmod != None:
								if not test_mode:
									destination.chmod(to + ftp_platform.get_separator() + local_item_name, chmod, None, False, True)
								AppLogger.info("Chmoding :'" + to + ftp_platform.get_separator() + local_item_name + "', with value '" + chmod + "'")

							i += 1

						elif comparison > 0 :
							if delete:
								if not test_mode:
									destination.delete(ftp_item.get_path(), None, False, True)
								AppLogger.info("Deleting :'" + ftp_item.get_path())
								
							j += 1

						else:
							if local_item.get_type() == ftp_item.get_type():

								if local_item.get_type() == FileObject.DIRECTORY:
									self.run(source, destination, local_item.get_path(), ftp_item.get_path(), excludes, chmod, delete, test_mode)

								elif local_item.get_type() == FileObject.FILE:
									local_item_time = time.mktime(datetime.timetuple(source.get_last_modified_time(local_item.get_path())))
									ftp_item_time = time.mktime(datetime.timetuple(destination.get_last_modified_time(ftp_item.get_path())))
									ftp_item_time += time_diff + 10

									if local_item_time > ftp_item_time:
										if not test_mode:
											destination.put(local_item.get_path(), to, None, False, True, False, True)
										AppLogger.info("Copying :'" + local_item.get_path() + "', to '" + to + "'")
										
										if chmod != None:
											if not test_mode:
												destination.chmod(to + ftp_platform.get_separator() + local_item_name, chmod, None, False, True)
											AppLogger.info("Chmoding :'" + to + ftp_platform.get_separator() + local_item_name + "', with value '" + chmod + "'")

							else:
								if not test_mode:
									destination.delete(ftp_item.get_path(), None, False, True)
									destination.put(local_item.get_path(), to, None, False, True, False, False)
								AppLogger.info("Deleting :'" + ftp_item.get_path())
								AppLogger.info("Copying :'" + local_item.get_path() + "', to '" + to + "'")

								if chmod != None:
									if not test_mode:
										destination.chmod(to + ftp_platform.get_separator() + local_item_name, chmod, None, False, True)
									AppLogger.info("Chmoding :'" + to + ftp_platform.get_separator() + local_item_name + "', with value '" + chmod + "'")

							i += 1
							j += 1

					else:
						break

				return True

			except Exception:

				retry -= 1

				if 0 == retry:
					raise
