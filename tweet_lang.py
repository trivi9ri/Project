import json
import pandas as pd
import matplotlib.pyplot as plt
from pylab import savefig


tweets_data_path = '/home/pi/Desktop/test/twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")

for line in tweets_file:
	try:
		tweet = json.loads(line)
		tweets_data.append(tweet)
				
	except:
		continue

def lang_twt(tweet):
	return tweet['lang']

tweets = pd.DataFrame(map(lang_twt, tweets_data),columns=['lang'])

tweets_by_lang = tweets['lang'].value_counts()
