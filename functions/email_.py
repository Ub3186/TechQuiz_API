import requests
from config import constant
import json

def send_welcome_message(user, email):
	return requests.post(
		"https://api.mailgun.net/v3/techquiz.xyz/messages",
		auth=("api", constant.EMAIL_API_TOKEN),
		data={"from": "Techquiz <postmaster@techquiz.xyz>",
			"to": [email],
			"subject": "Welcome to Techquiz",
			"template": "welcome",
			"h:X-Mailgun-Variables": json.dumps({"user":user })  })

def send_forget_password_message(email):
	return requests.post(
		"https://api.mailgun.net/v3/techquiz.xyz/messages",
		auth=("api", constant.EMAIL_API_TOKEN),
		data={"from": "Techquiz <postmaster@techquiz.xyz>",
			"to": [email],
			"subject": "Techquiz Password Reset",
			"template": "forget_password",
			"h:X-Mailgun-Variables": json.dumps({"email": email}) })