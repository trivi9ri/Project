
devel_dir="/home/pi/devel"
tmp_dir=devel_dir+"/BerePi/apps"

import json
from tweepy import OAuthHandler
import tweepy
import urllib2
from types import *
import sys
from unidecode import unidecode
from time import strftime, localtime
sys.path.append(tmp_dir+"/lcd_berepi/lib")
from lcd import *
sys.path.append(tmp_dir+"/sht20")
from sht25class import *
import datetime
import requests
import subprocess
import argparse
import re

tmp_dir=devel_dir+"/danalytics/thingsweb/weblib/recv"
sys.path.append(tmp_dir)
from lastvalue import *


CONSUMER_KEY =''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

URL_SENTIMENT140 = "http://www.sentiment140.com/api/bulkClassifyJson"
Politician = "samsung"
Limit = 100
Language = 'en'

def parse_response(json_response):
	neutral_tweets, negative_tweets, positive_tweets = 0,0,0
	for j in json_response["data"]:
		if int(j["polarity"]) == 0:
			negative_tweets += 1
		elif int(j["polarity"])== 4:
			positive_tweets += 1
		elif int(j["polarity"]) == 2:
			neutral_tweets += 1
	return neutral_tweets, negative_tweets, positive_tweets


def main():
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	tweets = []
	
	for tweet in tweepy.Cursor(api.search, q = Politician, result_type = ' recent', include_entities = True, lang = Language).items(Limit):
		tweet.text = re.sub("@[\S]+","",tweet.text)
		tweet.text = re.sub("((www.\.[^\s]+)|(https?://[^\s]+))","",tweet.text)
		aux = {"text": unidecode(tweet.text)}
		print aux
		tweets.append(aux)
	result = {"data" : tweets}
	
	req = urllib2.Request(URL_SENTIMENT140)
	req.add_header('Content-Tyle','application/json')
	response = urllib2.urlopen(req, str(result))
	json_response = json.loads(response.read())
	neutral_tweets, negative_tweets, positive_tweets = parse_response(json_response)
	posi = (float(positive_tweets)/100.0) * 100.0
	nega = (float(negative_tweets)/100.0) * 100.0
	neut = (float(neutral_tweets)/100.0) * 100.0
	print str(posi)
	print str(nega)
	print str(neut)
	if posi > nega and posi > neut:
		greenLCDon()
	elif nega > posi and nega > neut:
		redLCDon()
	elif neut > posi and neut > nega:
		whiteLCDon()
	lcd_string("Keyword: "+Politician,LCD_LINE_1,1)
	lcd_string("Total tweets: 80", LCD_LINE_2,1)
	time.sleep(3)
	lcd_string("Positive:"+str(posi),LCD_LINE_2,1)
	time.sleep(3)
	lcd_string("Neutral:"+str(neut),LCD_LINE_2,1)
	time.sleep(3)
	lcd_string("Negative:"+str(nega),LCD_LINE_2,1)
	time.sleep(3)
		


if __name__ == '__main__':
	try:
		lcd_init()
		main()
 	except KeyboardInterrupt:
  		  pass
  	finally:
    		lcd_init()
    		lcd_byte(0x01, LCD_CMD)
    		lcd_string("Goodbye!",LCD_LINE_2,1)
    		GPIO.cleanup()

 