#
# Copyright (c) 2008 vimov
#

import httplib
import urllib2
import os
import re

from thedeployer.packages.customexceptions import *
from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.clients.abstractclient import AbstractClient
from thedeployer.packages.depfile.validator import Validator
from thedeployer.packages.clients.localclient import LocalClient

class WebClient(AbstractClient):

	def __init__(self):
		pass

	@classmethod
	def download(cls, url, destination, replace = False, retry = 1):
		"""
		downloads a file from the web
		
		@param url: the url of the file to be downloaded
		@param destination: the destination where the file will be downloaded to
		@param replace: if set True then the downloaded file will replae any existinf file
		@param retry: number of retries
		
		@rtype: bool
		@return: True on success
		
		@raise FileDownloadError: if error during downloading
		"""
		if not Validator.validate(url, "url"):
			raise InvalidParameterError("url", "should be a non-empty string starts with 'http://'")
		if not Validator.validate(destination, "non_empty_string"):
			raise InvalidParameterError('destination', 'should be non-empty string')
		if not Validator.validate(replace, 'boolean'):
			raise InvalidParameterError('replace', 'should be a boolean value')
		if not Validator.validate(retry, 'integer'):
			raise InvalidParameterError('getting', 'should be an integer value')
		
		separator = Platform.get_current().get_separator()
		
		if not (re.match(r'/', destination) or re.match(r'[a-zA-Z]:\\', destination)):
			destination = destination.rstrip(separator)
		
		while retry:
			retry -= 1
			try:
				result = urllib2.urlopen(url, "")
				
				if os.path.exists(destination):
					if os.path.isdir(destination):
						if result.headers.has_key('content-disposition'):
							tmp = result.headers.dict['content-disposition']
							index = tmp.find('filename=')
							if index == -1:
								name = 'attachment'
							else:
								name = tmp[index+9: ]
								name = name.split(' ')[0]
						else:
							name = result.geturl()
							name = name.split('?')[0]
							name = name.rstrip('/')
							index = name.rfind('/')
							name = name[index+1:]
						
						destination = destination + separator + name
					
					else:
						if os.path.isfile(destination):
							if replace:
								os.remove(destination)
							else:
								raise FileExistsError, 'the destination file already exists'
						else:
							raise FileExistsError, 'destination is non-file, system cannot replace a non file'
					
				file = open(destination, "wb")
				
				buffer = result.read(4096)
				
				while len(buffer) != 0:
					file.write(buffer)
					buffer = result.read(4096)
				
				file.close()	
				
			except Exception, e:
				if retry == 0:
					raise FileDownloadError, str(e)
			
			else:
				break
			