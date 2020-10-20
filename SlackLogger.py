from requests import post


class SlackLogger:
	def __init__(self, slack_token, slack_channel, slack_url):
		self.slack_token = slack_token
		self.slack_channel = slack_channel
		self.slack_url = slack_url

	def log_to_slack(self, message):
		header = {"Content-Type": "text/plain; charset=utf-8"}
		params = (('token', self.slack_token),('channel', self.slack_channel))
		message = message.encode('utf-8')
		response = post(slack_url, params=params, data=data, headers=header)


def log_to_slack(logger, request):
	logger.log_to_slack(main_string)
