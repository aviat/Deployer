@TODO Draft, needs a lot of work!
@http://www.thinkspot.net/sheila/article.php?story=20040822174141155
@

import sys
import smtplib

class Email:

	def __init__(self):
		raise NotImplementedError()

	@staticmethod
	def send_by_smtp(email_message, server, username = "", password = "", port = 25):
		
		'''
		Send an E-Mail message using an SMTP server.

		@param email_message An instance of EmailMessage
		@param server The address of the SMTP server
		@param username The username of the SMTP server account (optionl)
		@param password The passwrord of the SMTP server account (optional)
		@param port The port of the SMTP server (optional, defaults to 25)

		@return True on success
		'''

		smtp_session = smtplib.SMTP(server)
		if username:
			smtp_session.login(username, password)
		smtp_result = smtp_session.sendmail(email_message.get_from(), email_message.get_to(), email_message.get_message())

		if smtp_result:
			errstr = ""
		for recip in smtpresult.keys():
			errstr = """Could not delivery mail to: %s"""
		
	@staticmethod
	def send_by_sendmail(email_message, sendmail_path):

		# prepare message

		message = "To: ", email_message.get_to(), "\nFrom: ",
			email_message.get_from(), "\nSubject: ",
			email_message.get_subject(), "\n\n",
			email_message.get_message()
		
		# open a pipe to the mail program and write the data to the pipe

		pipe = os.popen("%s -t" % MAIL, 'w')
		pipe.write(message)
		if pipe.close():
			print "Exit code: %s" % exitcode

		

class EmailMessage:

	# from
	# to
	# subject
	# message

	def __init__(self, from, to, subject, message):

		if "" == from:
			raise InvalidParameterError("from", "Not empty")
		elif "" == to:
			raise InvalidParameterError("to", "Not empty")
		elif "" == subject:
			raise InvalidParameterError("subject", "Not empty")
		elif "" == message:
			raise InvalidParameterError("message", "Not empty")

		self.from = from
		self.to = to
		self.subject = subject
		self.message = message

	def get_from(self):
		return from

	def get_to(self):
		return to

	def get_subject(self):
		return subject

	def get_message(self):
		return message
