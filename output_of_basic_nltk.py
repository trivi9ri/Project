
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


tweets_data_path = '/home/pi/Desktop/BerePi-master/apps/lcd_berepi/twitter-out.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
all_twt = 0.0
pos = 0.0
neg = 0.0

for line in tweets_file:
	all_twt = all_twt+1.0
	if str(line[0:3]) == "pos":
		pos = pos+1.0
	elif str(line[0:3]) == "neg":
		neg = neg+1.0

per_pos = (pos/all_twt)*100
per_neg = (neg/all_twt)*100

str_twt = ("Total tweet: %d") % all_twt
str_pos = ("Positive: %d percent (%d)") % (per_pos,pos)
str_neg =("Negative: %d percetn (%d)") % (per_neg,neg)


if __name__ == '__main__':
	try:
		lcd_init()
		if per_pos == per_neg:
			whiteLCDon()
		elif per_pos > per_neg:
			greenLCDon()
		elif per_neg > per_pos:
			redLCDon()
		lcd_string(str_twt,LCD_LINE_1,1)
		
		while (1):

			lcd_string(str_pos, LCD_LINE_2,1)
			time.sleep(3)
			lcd_string(str_neg,LCD_LINE_2,1)
			time.sleep(3)
			
 	except KeyboardInterrupt:
  		  pass
  	finally:
    		lcd_init()
    		lcd_byte(0x01, LCD_CMD)
    		lcd_string("Goodbye!",LCD_LINE_2,1)
    		GPIO.cleanup()


