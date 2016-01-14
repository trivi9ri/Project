# -*- coding:utf-8 -*-
#!/usr/bin/python
# Author : ipmstyle, https://github.com/ipmstyle
#        : jeonghoonkang, https://github.com/jeonghoonkang
# for the detail of HW connection, see lcd_connect.py

devel_dir="/home/pi/devel"
tmp_dir=devel_dir+"/BerePi/apps"

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
import urllib
import tweepy
from bs4 import BeautifulSoup

tmp_dir=devel_dir+"/danalytics/thingsweb/weblib/recv"
sys.path.append(tmp_dir)
from lastvalue import *

targetXML = urllib.urlopen('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName=%EC%A2%85%EB%A1%9C%EA%B5%AC&dataTerm=month&pageNo=1&numOfRows=10&ServiceKey=I77BWymB0y6QnMh3psGXJDLJIVmgNcP6zMoQhE52odnNWt5O%2BNXxvhuY9U38%2FwEhZwOQ2iUAnZHtJugPjphqCg%3D%3D&ver=1.0')
soup = BeautifulSoup(targetXML, "lxml")


def main():
	lcd_init()
	for element in soup.findAll('item'):
		lcd_init()
		now = time.localtime()
		hour = now.tm_hour
		hour2 = int(element.datatime.text[11:13])
		if hour==hour2:
			pm10value = element.pm10value.text
			pm25value = element.pm25value.text
			so2value = element.so2value.text
			covalue = element.covalue.text
			o3value = element.o3value.text
			pm10grade = element.pm10grade.text
			pm10 = "PM10: "+pm10value
			pm25 = "PM25: "+pm25value
			so2 = "SO2: "+so2value
			co = "CO: "+covalue
			o3 = "O3: "+o3value
			city = "City: JONGRO"
			date = element.datatime.text
			Grade(pm10grade)
			lcd_string ('%s' % (date), LCD_LINE_1,1)
			lcd_string ('%s' % (city), LCD_LINE_2,1)
			time.sleep(3)
			lcd_string ('%s' % (pm10), LCD_LINE_2,1)
			time.sleep(3)
			lcd_string ('%s' % (pm25), LCD_LINE_2,1)
			time.sleep(3)
			lcd_string ('%s' % (so2), LCD_LINE_2,1)
			time.sleep(3)
			lcd_string ('%s' % (co), LCD_LINE_2,1)
			time.sleep(3)
			lcd_string ('%s' % (o3), LCD_LINE_2,1)
			time.sleep(3)
			text = date+" standards\n"+city+"\n"+pm10+"\n"+pm25+"\n"+so2+"\n"+co+"\n"+o3
			twiiter(text)


	
def Grade(pm10grade):
	if pm10grade == '1':
		blueLCDon()
	elif pm10grade == '2':
		greenLCDon()
	elif pm10grade == '3':
		yellowLCDon()
	elif pm10grade == '4':
		redLCDon()


def twiiter(text):	
	CONSUMER_KEY ='your consumer key'
	CONSUMER_SECRET = 'your consumer secret'
	ACCESS_KEY = 'your access key'
	ACCESS_SECRET = 'your access secret'
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	status = api.update_status(text)
	

if __name__ == '__main__':
	try:	
		main()
	except KeyboardInterrupt:
    		pass
  	finally:
   		lcd_init()
    		lcd_byte(0x01, LCD_CMD)
    		lcd_string("Goodbye!",LCD_LINE_2,1)
		GPIO.cleanup()