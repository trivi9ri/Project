import requests

def send_simple_message():
	return requests.post(
		"http://api.mailgun.net/v3/sandbox0d80107857f442c3b0ef7c23dabbcc62.mailgun.org/messages",
			auth=("api","key-b5617c700ceecd0d52a4239b923019e6"),
			data={"from":"Mailgun Sandbox <postmaster@sandbox0d80107857f442c3b0ef7c23dabbcc62.mailgun.org>",
				"to":"gadin.kang <gadin.kang@gmail.com>",
				"subject":"Hi, It's test mail",
				"text":"This mail is Mailgun test mail! from Yu-Bin"})

send_simple_message()