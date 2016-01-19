import json
import matplotlib 
matplotlib.use('Agg')
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

fig, ax = plt.subplots()
ax.tick_params(axis ='x', labelsize =15)
ax.tick_params(axis ='y', labelsize=15)
ax.set_xlabel('Languages',fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 languages',fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax,kind='bar',color='blue')
plt.savefig('myflg.png')
