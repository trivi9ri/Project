
devel_dir="/home/pi/devel"
tmp_dir=devel_dir+"/BerePi/apps"

import json
import matplotlib 
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pylab import savefig
from types import *
import sys
from time import strftime, localtime
sys.path.append(tmp_dir+"/lcd_berepi/lib")
from lcd import *
sys.path.append(tmp_dir+"/sht20")
from sht25class import *

import datetime
import requests
import json
import subprocess
import argparse

tmp_dir=devel_dir+"/danalytics/thingsweb/weblib/recv"
sys.path.append(tmp_dir)
from lastvalue import *


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

if __name__ == '__main__':
	try:
		lcd_init()
		lcd_string("Top 5 Languages",LCD_LINE_1,1)
		for i in range (0,5):
			arr = str(tweets_by_lang[i:]).split('\n')
			lcd_string(arr[0],LCD_LINE_2,1)
			time.sleep(3)
			
 	except KeyboardInterrupt:
  		  pass
  	finally:
    		lcd_init()
    		lcd_byte(0x01, LCD_CMD)
    		lcd_string("Goodbye!",LCD_LINE_2,1)
    		GPIO.cleanup()

 