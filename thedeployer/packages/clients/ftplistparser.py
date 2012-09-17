#
# Copyright (c) 2008 vimov
#

import re
import datetime

from thedeployer.packages.platform._platform import Platform
from thedeployer.packages.depfile.validator import Validator

class FtpListParser(object):
	
	def __init__(self, platform, list):
		
		"""
		constructor for the class 
		this class used for parsing the long file list format and get the file properties from it
		i.e. drwxr-xr-x   2 ftp      nogroup      4096 Aug 20 13:46 New directory
		
		Note:
			this format is not standard and varies according to the server type(Linux or Windows)
			and the used ftp library 
		"""
		
		if not Validator.validate_non_empty_string(list):
			raise InvalidParameterError("list", "list can not be None or empty string")
		
		if platform is None:
			raise InvalidParameterError("platform", "platform can not be None")		
		
		self.__platform = platform 
		self.__list = list
		
		self.__type = '-'
		self.__mode = '---------'
		
		self.__links = '0'
		
		self.__owner = ''
		self.__group = ''
		
		self.__size = '0'

		self.__date = ''
		now = datetime.datetime.now()
		self.__year = str(now.year)
		self.__month = ''
		self.__day = ''
		self.__hour = '00'
		self.__minute = '00'
		self.__second = '00'
		self.__month_dic = { 'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11' , 'Dec':'12'}
		self.__name = ''
		
		self.__parse(self.__list)
	
	def __parse(self, list):
		'''
		parse the list string
		string1 = "drwxr-xr-x   2 ftp      nogroup      4096 Aug 20 13:46 New directory" #pattern 1
		string6 = "d---------   1 owner    group               0 May  9 19:45 Softlib-d" #equal to pattern 1
		string4 = "lrwxrwxrwx   1 root     other          7 Jan 25 00:17 bin -> usr/bin" #pattern 1
		string5 = "----------   1 owner    group         1803128 Jul 10 10:18 ls-lR.Z" #pattern 1
		
		string2 = "dr-xr-xr-x   2 root     other        512 Apr  8  1994 etc-etc" #pattern 2
		string7 = "-rwxrwxrwx   1 noone    nogroup      322 Aug 19  1996 message.ftp" #pattern 2
		
		string3 = "dr-xr-xr-x   2 root     512 Apr  8  1994 etc" #pattern 3
		
		string8 = "d [R----F---] supervisor            512       Jan 16 18:53    login" #pattern 4

		"""Windos fromat"""		
		string9 = '04-27-00  09:09PM       <DIR>          licensed' #pattern 5
		string10 = '04-14-00  03:47PM                  589 readme.htm' #pattern 6
		
		"""paramiko fromat"""
		string10 = "drwxr-xr-x   1 1000     1000         4096 21 Jul 11:34 aptana.workspace" #pattern7
		string11 = "drwxr-xr-x   1 1000     1000         4096 21 Jul 2004 aptana.workspace" #pattern8
		
		pattern1 = "^(d|l|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern2 = "^(d|l|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{4})\s+.+"
		pattern3 = "^(d|l|-)\S{9}\s+(\d+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{4})\s+.+"
		pattern4 = "^(d|l|-)\s+\[(\S{9})\]\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern5 = '\d{1,2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}\w{2}\s+<\w+>\s+.+'
		pattern6 = '\d{1,2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}\w{2}\s+\d+\s+.+'
		pattern7 = "^(d|l|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d{1,2})\s+(\w{3})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern8 = "^(d|l|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d{1,2})\s+(\w{3})\s+(\d{4})\s+.+"
		'''
		
		str, pattern_number = self.__get_pattern_number(list)
		
		if 1 == pattern_number:
			'''
			string1 = "drwxr-xr-x   2 ftp      nogroup      4096 Aug 20 13:46 New directory" #pattern 1
			string6 = "d---------   1 owner    group               0 May  9 19:45 Softlib-d" #equal to pattern 1
			string4 = "lrwxrwxrwx   1 root     other          7 Jan 25 00:17 bin -> usr/bin" #pattern 1
			string5 = "----------   1 owner    group         1803128 Jul 10 10:18 ls-lR.Z" #pattern 1
			'''
			list = str.split(None, 8)
			self.__type = list[0][0]
			self.__mode = list[0][1:10]
			self.__links = list[1]
			self.__owner = list[2]
			self.__group = list[3]
			self.__size = list[4]
			self.__month = list[5]
			self.__day =  list[6]
			time = list[7]
			time_list = time.split(':')
			self.__hour = time_list[0]
			self.__minute = time_list[1]
			self.__second = '00'
			temp = list[8]
			i = temp.find('->')
			if i >= 0:
				temp = temp[0:i]
			self.__name =  temp.rstrip()
		elif 2 == pattern_number :
			'''
			string2 = "dr-xr-xr-x   2 root     other        512 Apr  8  1994 etc-etc" #pattern 2
			string7 = "-rwxrwxrwx   1 noone    nogroup      322 Aug 19  1996 message.ftp" #pattern 2
			'''
			list = str.split(None, 8)
			self.__type = list[0][0]
			self.__mode = list[0][1:10]
			self.__links = list[1]
			self.__owner = list[2]
			self.__group = list[3]
			self.__size = list[4]
			self.__month = list[5]
			self.__day =  list[6]
			self.__year = list[7]
			temp = list[8]
			i = temp.find('->')
			if i >= 0:
				temp = temp[0:i]
			self.__name =  temp.rstrip()

		elif 7 == pattern_number :
			'''
			string10 = "drwxr-xr-x   1 1000     1000         4096 21 Jul 11:34 aptana.workspace" #pattern7
			'''
			list = str.split(None, 8)
			self.__type = list[0][0]
			self.__mode = list[0][1:10]
			self.__links = list[1]
			self.__owner = list[2]
			self.__group = list[3]
			self.__size = list[4]
			self.__day =  list[5]
			self.__month = list[6]
			time = list[7]
			time_list = time.split(':')
			self.__hour = time_list[0]
			self.__minute = time_list[1]
			temp = list[8]
			i = temp.find('->')
			if i >= 0:
				temp = temp[0:i]
			self.__name =  temp.rstrip()

		elif 8 == pattern_number :
			'''
			string11 = "drwxr-xr-x   1 1000     1000         4096 21 Jul 2004 aptana.workspace" #pattern8
			'''
			list = str.split(None, 8)
			self.__type = list[0][0]
			self.__mode = list[0][1:10]
			self.__links = list[1]
			self.__owner = list[2]
			self.__group = list[3]
			self.__size = list[4]
			self.__day =  list[5]
			self.__month = list[6]
			self.__year = list[7]
			temp = list[8]
			i = temp.find('->')
			if i >= 0:
				temp = temp[0:i]
			self.__name =  temp.rstrip()

		elif 3 == pattern_number :
			pass

		elif 4 == pattern_number :
			pass

		elif 5 == pattern_number :
			pass

		elif 6 == pattern_number :
			pass

	
	def __get_pattern_number(self, list):
		
		pattern1 = "^(d|l|s|c|p|b|D|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern2 = "^(d|l|s|c|p|b|D|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{4})\s+.+"
		pattern3 = "^(d|l|s|c|p|b|D|-)\S{9}\s+(\d+)\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{4})\s+.+"
		pattern4 = "^(d|l|s|c|p|b|D|-)\s+\[(\S{9})\]\s+(\w+)\s+(\d+)\s+(\w{3})\s+(\d{1,2})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern5 = '\d{1,2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}\w{2}\s+<\w+>\s+.+'
		pattern6 = '\d{1,2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}\w{2}\s+\d+\s+.+'
		pattern7 = "^(d|l|s|c|p|b|D|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d{1,2})\s+(\w{3})\s+(\d{1,2}):(\d{1,2})\s+.+"
		pattern8 = "^(d|l|s|c|p|b|D|-)\S{9}\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d{1,2})\s+(\w{3})\s+(\d{4})\s+.+"
		
		m = re.match(pattern1, list, re.IGNORECASE)
		if m:
			return str(m.group()), 1
		
		m = re.match(pattern2, list, re.IGNORECASE)
		if m:
			return str(m.group()), 2

		m = re.match(pattern7, list, re.IGNORECASE)
		if m:
			return str(m.group()), 7

		m = re.match(pattern8, list, re.IGNORECASE)
		if m:
			return str(m.group()), 8
		
		m = re.match(pattern3, list, re.IGNORECASE)
		if m:
			return str(m.group()), 3
		
		m = re.match(pattern4, list, re.IGNORECASE)
		if m:
			return str(m.group()), 4
		
		m = re.match(pattern5, list, re.IGNORECASE)
		if m:
			return str(m.group()), 5
		
		m = re.match(pattern6, list, re.IGNORECASE)
		if m:
			return str(m.group()), 6
	
	def get_name(self):
		return self.__name 
	
	def get_size(self):
		return self.__size
	
	def get_mode(self):
		return self.__mode
	
	def get_type(self):
		return self.__type
	
	def get_owner(self):
		return self.__owner
	
	def get_group(self):
		return self.__group
	
	def links(self):
		return self.__links
	
	def get_date(self):
		if Platform.PLATFORM_WINDOWS == self.__platform.get_platform():
			self.__date = self.__second + ' ' + self.__minute + ' ' + self.__hour + ' ' + self.__day + ' ' + self.__month + ' ' + self.__year
		else:
			self.__date = self.__second + ' ' + self.__minute + ' ' + self.__hour + ' ' + self.__day + ' ' + self.__month_dic.get(self.__month) + ' ' + self.__year
		return self.__date
	
	def get_time(self):
		return self.__time
