import httplib
import urllib
import urllib2
import Cookie
import cookielib
import exceptions
import socket
import re


from thedeployer.packages.customexceptions import *
from thedeployer.packages.depfile.validator import Validator

class BrowserSession(object):
	'''
	This class creates a browser session that takes list of requests, execute them sequentially when calling 'run' method and return list
	of responses if all requests executed successfully, if an error occured during any request execution or responses validation execution
	will stop and an exception will be raised.
	
	You give the constructor list of requests of Request class.
	
	You can pass cookies to the session using 'set_cookies' method. You should pass a CookieJar object to it (see python documention for
	CookieJar class at http://docs.python.org/lib/cookie-jar-objects.html).
	
	After requests execution you can add more requests executes them within the same session (using the same CookieJar).
	'''
	
	def __init__(self, requests):
		'''
		@param requests: is a list of instances of Request class, contain all requests that should be automated sequentially
		'''
		if requests.__class__ != list:
			raise InvalidParameterError("requests", "Must be instance of string")
		
		self.requests = requests
		self.cookies = cookielib.CookieJar()
		self.responses = []
		self.last_response = None
	
	def run(self):
		'''
		handle requests dependency, executes requests of the session, validate responses returned and empty the requests list
		
		@raise MatchDataError: 
		'''
		
		for request in self.requests:
			request.set_cookies(self.cookies)
			for req_data in request.get_requested_data():
				if not self.last_response:
					raise MatchDataError
				key , value = req_data.match(self.last_response.get_body())
				request.add_data(key, value)
			response = request.execute()
			response.validate()
			self.last_response = response
			self.responses.append(response)
		
		self.requests = []
		responses = self.responses
		self.responses = []
		
		return responses
	
	
	def set_last_response(self, last_response):
		'''
		set response that the first request in the list depends on.
		
		@param last_response: instance of Response class
		'''
		
		if isinstance(last_response, Response):
			self.last_response = last_response
			return True
		return False
	
	def set_cookies(self, cookies):
		'''
		sets cookie jar to the session which that requests use to handle cookies and responses use to extract returned cookies in
		
		@param cookies: object of CookieJar class
		'''

		if isinstance(cookies, cookielib.CookieJar):
			self.cookies = cookies
			return True
		return False
	
	
	def get_cookies(self):
		return self.cookies
	
	def set_requests(self, requests):
		'''
		this method replaces requests list with the given list
		
		@param requests: list of requests of Request class
		'''
		
		if isinstance(requests, list):
			self.requests = requests
			return True
		return False
	
	def add_request(self, request):
		'''
		add single request
		
		@param request: instance of 'Request' class
		'''
		
		if isinstance(request, Request):
			self.requests.append(request)
			return True
		return False
	
	def add_requests(self, requests):
		'''
		this method append requests list by the given list
		add multiple requests at once by supplying list of requests
		
		@param requests: list of requests of Request class
		'''
		
		if isinstance(requests, list):
			self.requests.extend(requests)
			return True
		return False


class DataMatcher(object):
	'''
	this class used to match post data needed for requests from the imidiately preceding responses
	
	it takes aregular expression of match patern in the contructor
	
	the matching string (response body) is passed to match method that returns a tuple of key and value
	
	note: match pattern may be in form like '<input type="hidden" name="anything" value=".*">'
	note: match pattern (reqular expretion) should  contain ' name="anything" ' and ' value="anything" 'in the regular expretion string
	'''
	
	def __init__(self, match_pattern):
		'''
		@param match_pattern: regular expretion string 
		'''
		
		if not Validator.validate_string(match_pattern):
			raise InvalidParameterError("match_pattern", "Must be a string value")
		
		self.match_pattern = match_pattern
		
	def match(self, match_string):
		'''
		matches pattern in body of response
		
		@param match_string: string to be matched (body of response)
		'''
		
		if not Validator.validate_string(match_string):
			raise InvalidParameterError("match_string", "Must be a string value")
		
		matchs = re.findall(self.match_pattern, match_string)
		if not matchs:
			raise MatchDataError
		data = matchs[0]
		data_key = (re.findall('name[ ]*=[ ]*".*"',data))[0]
		data_value = (re.findall('value[ ]*=[ ]*".*"',data))[0]
		if not (data_key and data_value):
			raise MatchDataError
		return (data_key.split('"'))[1], (data_value.split('"'))[1]


class Request(object):
	'''
	To instantiate an object of Request class you pass the url of request. Other constructor parameters are optional
	
	You can add validators to the response resulted from that request. Validation is for status code, body, cookies (see ResponsValidation
	child classes for more details)
	
	If the request depends on the the immediately preceding response, you should create an objects of DataMatcher, pass it a regular
	expression of post data you want to match and pass this object to 'add_requested_data' method
	'''
	
	HTTP_METHOD_GET = 'GET'
	HTTP_METHOD_POST= 'POST'
	HTTP_METHOD_POST_XWWW_DATA = 'application/x-www-form-urlencoded'
	HTTP_METHOD_POST_FORM_DATA = ''
	USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9) Gecko/2008061015 Firefox/3.0'
	
	def __init__(self, url, proxy = None, auth = None, post_encoding = HTTP_METHOD_POST_XWWW_DATA):
		'''
		@param url: the url of the request
		@param proxy: dictionary with two entries have keys ('type' and 'host')
		@param auth: dictionary with four entries have keys ('realm', 'uri', 'user', 'passwd')
		@param ost_encoding : one of types 'Request.HTTP_METHOD_POST_XWWW_DATA' or 'Request.HTTP_METHOD_POST_FORM_DATA'
		'''
		
		if not Validator.validate_non_empty_string(url):
			raise InvalidParameterError("url", "Must be non-empty string")
		if proxy.__class__ != dict and proxy != None:
			raise InvalidParameterError("proxy", "Must be a dictionary")
		if auth.__class__ != dict and auth != None:
			raise InvalidParameterError("auth", "Must be a dictionary")
		
		
		self.method = Request.HTTP_METHOD_GET
		self.url = url
		self.referrer = url
		self.proxy = proxy
		self.auth = auth
		self.post_encoding = post_encoding
		self.data = {}
		self.params = {}
		self.headers = {}
		self.response_validator = []
		self.requested_data = []
		self.cookies = cookielib.CookieJar()
	
	@classmethod
	def set_default_timeout(cls, timeout):
		'''
		sets default timeout for all requests
		'''
		
		if not Validator.validate_integer(timeout):
			raise InvalidParameterError("timeout", "Must be an integer value")
		
		socket.setdefaulttimeout(timeout)
	
	@classmethod
	def set_default_user_agent(cls, user_agent):
		'''
		sets default User Agent for all requests
		
		@param user_agent:
		'''
		
		if not Validator.validate_non_empty_string(user_agent):
			raise InvalidParameterError("user_agent", "Must be non-empty string")
		
		Request.USER_AGENT = user_agent
	
	@classmethod
	def get_default_user_agent(cls):
		'''
		return default User Agent
		'''
		
		return Request.USER_AGENT
	
	
	def add_requested_data(self, req_data):
		'''
		@param req_data: instance of DataMatcher class
		
		add post data that depends on the immediately preceding 
		'''
		
		if isinstance(req_data, DataMatcher):
			self.requested_data.append(req_data)
			return True
		return False
	
	def get_requested_data(self):
		
		return self.requested_data
	
	def add_response_validator(self, response_validator):
		'''
		@param response_validator: instance of children of ResponseValidation class
		
		add a validator to the response of that request
		
		response validation is one of four types that is used to validate status coe, body and return cokies of the reponse (see
		ResponseValidation child classes for more details)
		'''
		
		if isinstance (response_validator, ResponseValidator):
			self.response_validator.append(response_validator)
			return True
		return False

	def add_header(self, key, value):
		'''
		add header to the request in form of key and value
		
		@param key: 
		@param value: 
		'''
		
		self.headers[key] = value
	
	def set_cookies(self, cookies):
		'''
		sets a cookie jar for the request to be used by CookieProcessor
		note: this methos is called by the browser session class by default. the is no need to be called again
		
		@param cookies: instance of CookieJar
		'''

		if isinstance(cookies, cookielib.CookieJar):
			self.cookies = cookies
			return True
		return False
	
	def get_cookies(self):
		
		return self.cookies
	
	def add_data(self, key, value):
		'''
		add data to HTTP response
		data will be sent in the request body so the request method converted automaticly to 'POST' method
		
		@param key: 
		@param value: 
		'''
		
		if key:
			self.method = Request.HTTP_METHOD_POST
			self.data[key]=value
			return True
		return False
		
	def emty_data(self):
		'''
		Empty data of request
		request method will be set to be 'Get' method
		'''
		
		self.method = Request.HTTP_METHOD_GET
		self.data = {}
	
	def add_params(self, key, value):
		'''
		add 'GET' params to the request. these params are concatenated with the url of the request after being encoded
		
		@param key: 
		@param value: 
		'''
		
		if key and value:
			self.params[key]=value
			return True
		return False
	
	def set_referrer(self, referrer):
		'''
		sets the request referrer
		
		@param referrer: 
		'''
		
		if not Validator.validate_non_empty_string(referrer):
			raise InvalidParameterError("referrer", "Must be non-empty String")
		
		self.referrer = referrer
	
	def get_referrer(self):
		
		return self.referrer
	
	def set_proxy(self, proxy):
		'''
		@param proxy: dictionary with two entries have keys ('type' and 'host')
		sets the request proxy
		'''
		
		if isinstance(proxy, dict) and proxy.has_key('type') and proxy.has_key('host'):
			self.proxy = proxy
			return True
		return False
	
		
	def set_authentication(self, auth):
		'''
		authenticates the request

		@param auth: dictionary with four entries have keys ('realm', 'uri', 'user', 'passwd')
		'''
		
		if isinstance(proxy, dict) and proxy.has_key('realm') and proxy.has_key('uri') and proxy.has_key('user') and proxy.has_key('passwd'):
			self.auth = auth
			return True
		return False
	
	def execute(self):
		'''
		create an HTTP request with suitable parameters and parse the response
		@return response object
		'''
		
		if self.params :
			params = urllib.urlencode(self.params)
			params = '?' + params
			self.url += params
		
		if Request.HTTP_METHOD_GET == self.method:
			request = urllib2.Request(url = self.url, headers = self.headers)
			
		else:
			if Request.HTTP_METHOD_POST_XWWW_DATA == self.post_encoding:
				data = urllib.urlencode(self.data)
			else:
				pass
			
			request = urllib2.Request(self.url, data, self.headers)
		
		request.add_header('Referer', self.referrer)
		request.add_header('User-Agent', Request.USER_AGENT)
		
		opener = urllib2.build_opener()
		if self.proxy:
			try:
				request.set_proxy(self.proxy['host'], self.proxy['type'])
				proxy_handler = urllib.ProxyHandler()
				opener.add_handler(proxy_handler)
			except KeyError:
				raise ProxyParamError
		
		if self.auth:
			try:
				auth_handler = urllib2.HTTPBasicAuthHandler()
				auth_handler.add_password (realm = self.auth['realm'], uri = self.auth['uri'], user = self.auth['user'],  passwd = self.auth['passwd'])
				opener.add_handler(auth_handler)
			except KeyError:
				raise AuthParamError
		
		cookie_handler = urllib2.HTTPCookieProcessor(self.cookies)
		opener.add_handler(cookie_handler)
		
		try:
			response = Response()
			res = opener.open(request)
			
			code = res.code
			response.set_status_code(code)
			
			body=''
			for line in res:
				body += line
			response.set_body(body)
			
			
			self.cookies.extract_cookies(res, request)
			response_cookies = self.cookies.make_cookies(res, request)
			response.set_cookies(response_cookies)
			
			res_info = res.info()
			response.set_info(res_info)
			response.set_validators(self.response_validator)
			
			cont_len = ''
			try:
				cont_len = res_info.dict['content-length']
			except:
				cont_len = None
			if cont_len and str(len(body)) != cont_len :
				raise IncompleteReponseError(response)
		
		except Exception, e:
			raise ExRequestError(response, str(e))
		
		return response


class Response(object):
	
	'''
	this object is returned from request execution. it contains the status code, body, cookies and headers info of the  response
	'''
	
	def __init__ (self, code = None, body = None, cookies = None):
		"""
		class constructor
		
		@param code: 
		@param body: 
		@param cookies: 
		"""
		
		self.code = code
		self.body = body
		self.cookies = cookies
		self.info = ''
		self.response_validators = []
	
	def set_status_code(self, code):
		"""
		sets the status code of Response
		
		@param code: 
		"""
		
		self.code = code
	
	def set_body(self, body):
		"""
		sets the body of Response
		
		@param body: 
		"""
		
		self.body = body
	
	def set_cookies(self, cookies):
		"""
		sets cookies of Response
		
		@param cookies: 
		"""
		
		self.cookies = cookies
	
	def get_status_code(self):
		
		return self.code
	
	def get_body(self):
		
		return self.body
	
	def get_cookies(self):
		
		return self.cookies
	
	def add_validator(self, validator):
		'''
		add a validator to the response (see ReponseValidation child classes)
		
		@param validator: instance of  ResponseValidation childs
		'''
		
		if isinstance (validator, AcceptedStatusCodeValidation) or isinstance (validator, RejectedStatusCodeValidation):
			validator.set_status_code(self.code)
			self.response_validators.append(validator)
			return True
		
		if isinstance(validator, BodyValidation):
			validator.set_body(self.body)
			self.response_validators.append(validator)
			return True
		
		if isinstance(validator, CookiesValidation):
			validator.set_cookies(self.cookies)
			self.response_validators.append(validator)
			return True
		return False

	
	def set_validators(self, validators):
		'''
		sets the response validator list
		
		@param: list of ResponseValidation childs
		'''
		
		if isinstance(validators, list):
			self.response_validators = []
			for validator in validators:
				if not self.add_validator(validator):
					return False
			return True
		return False
	 
	
	def validate(self):
		'''
		iterate validator
		
		validate the response according to validator list
		'''
		
		for res_validator in self.response_validators:
			res_validator.validate()
	
	def set_info(self, info):
		self.info = info
	
	def get_info(self):
		return self.info


##################################
# Validators
##################################

class ResponseValidator(object):
	'''
	it's abstract class should not be instantiated
	'''
	
	def validate(self):
		pass

class AcceptedStatusCodeValidation(ResponseValidator):
	'''
	this class used to check that response status code is one of a list of accepted status codes
	'''
	
	def __init__(self, accepted_codes):
		'''
		@param: list of accepted status codes
		'''
		
		self.status_code= None
		self.accepted_codes = accepted_codes
	
	def set_status_code(self, status_code):
		'''
		sets the status code to be validated
		'''
		
		self.status_code = status_code
	
	def validate(self):
		'''
		raise AcceptedCodeError if validation failed
		'''
		
		not_valid = True
		for accepted_code in self.accepted_codes:
			if accepted_code == self.status_code:
				not_valid = False
				break
		if not_valid:
			raise AcceptedCodeError


class RejectedStatusCodeValidation(ResponseValidator):
	'''
	this class used to check that response status code is not one of a list of rejected status codes
	'''
	
	def __init__(self, rejected_codes):
		
		self.status_code= None
		self.rejected_codes = rejected_codes
	
	def set_status_code(self, status_code):
		'''
		sets the status code to be validated
		'''
		
		self.status_code = status_code
	
	def validate(self):
		'''
		raise RejectedCodeError if validation failed
		'''
		
		for rejected_code in self.rejected_codes:
			if rejected_code == self.status_code:
				raise RejectedCodeError


class BodyValidation(ResponseValidator):
	'''
	this class used to validate the response body by checking that the response body contains required strings and not contain some rejects
	string values. this class matched body using Regular Expression provided to constructor of the class, than match it with two list of
	required and rejected matches
	'''
	
	def __init__(self, regex):
		'''
		@param regex: reqular expression to matched from the  response body
		'''
		
		self.body = ''
		self.regex = regex
		self.required_matches = []
		self.rejected_matches = []

	def set_body(self, body):
		'''
		sets the response body to be validated
		
		@param body: 
		'''
		
		self.body = body
	
	def set_rejected_matches(self, rejected_matches):
		'''
		sets the list of rejected matches
		
		@param rejected_matches: 
		'''
		
		if isinstance(rejected_matches, list):
			self.rejected_matches = rejected_matches
			return True
		return False
	
	def set_required_matches(self, required_matches):
		'''
		sets the list of required matched
		
		@param required_matches: 
		'''
		
		if isinstance(required_matches, list):
			self.required_matches = required_matches
			return True
		return False
	
	def validate(self):
		'''
		raise AcceptedBodyRegExError or RejectedBodyRegExError if body validation failed
		'''
		
		matches = re.findall(self.regex, self.body)
		not_valid = False
		for req_match in self.required_matches:
			not_valid =True
			for match in matches:
				if req_match == match:
					not_valid = False
					break
		if not_valid:
			raise AcceptedBodyRegExError
		
		for rej_match in self.rejected_matches:
			for match in matches:
				if rej_match == match:
					raise RejectedBodyRegExError


class CookiesValidation(ResponseValidator):
	'''
	this class used to validate cookies of the response by checking if the list of required cookies contained in response cookies
	'''
	
	def __init__(self, required_cookies):
		'''
		@param required_cookies: list of key of required cookies
		'''
		
		self.cookies = None
		self.required_cookies = required_cookies
	
	def set_cookies(self, cookies):
		'''
		sets the response cookies to be validated
		
		@param cookies: 
		'''
		
		if isinstance(cookies, list):
			self.cookies = cookies
			return True
		return False
	
	def validate(self):
		'''
		raise CookiesValidationError if validation failed
		'''
		
		for req_cookie in self.required_cookies:
			not_valid = True
			for cookie in self.cookies:
				if req_cookie == cookie.name:
					not_valid = False
					break
			if not_valid:
				raise CookiesValidationError
