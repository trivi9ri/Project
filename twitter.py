
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY =''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

	

class StdOutListener(StreamListener):

	def on_data(self,data):
		print(data)
		return True

	def on_error(self, status):	
		print(status)


if __name__ == '__main__':
	I = StdOutListener()
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	stream = Stream(auth, I)
	stream.filter(track = ['carmex','kamil'])
