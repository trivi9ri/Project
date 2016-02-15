#code:pythonprogramming.net/twitter-sentiment-analysis-nltk-tutorial/

sent_dir = "/home/pi/Desktop/BerePi-master/apps/lcd_berepi"

from tweepy import Stream
from tweepy import OAuthHandler	
from tweepy.streaming import StreamListener
import json
import sys
import re
sys.path.append(sent_dir)
import sentiment_mod as s

CONSUMER_KEY ='euJVsZtssnSdgdXKm4jaIAbK5'
CONSUMER_SECRET = 'LG30eLwdNlKOS3WyImdOFUf2imvRldo5a7xPYI94qQiv2UGwPg'
ACCESS_KEY = '1805474768-SbWh1Blp2GqRelRsu3CeQ0i8753L2mUXKGBFyuc'
ACCESS_SECRET = 'RplRY27OLNRCKcjJ1YjSOEHsUfmShrZYURG1SwWk9IR7Y'


class listener(StreamListener):

	def on_data(self,data):	
		all_data = json.loads(data)
		tweet = all_data["text"]
		tweet = re.sub("@[\S]+","",tweet)
 		tweet = re.sub("((www.\.[^\s]+)|(http?://[^\s]+))","",tweet)
		tweet = tweet.lower()
		if ("makes" in tweet)|("i'm" in tweet)|("feel" in tweet)|("i am" in tweet):
 
			sentiment_value, confidence = s.sentiment(tweet)
			print(tweet, sentiment_value, confidence)

			if confidence*100 >= 80:
				output = open("twitter-out.txt","w")
				output.write(sentiment_value)
				output.write('\n')
				output.close()
	
		return True

	def on_error(self, status):
		print status


auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

twitterStream = Stream(auth, listener())
twitterStream.filter(track = ["donald trump"])

