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
from bs4 import BeautifulSoup

tmp_dir=devel_dir+"/danalytics/thingsweb/weblib/recv"
sys.path.append(tmp_dir)
from lastvalue import *

html= urllib.urlopen('http://rottentomatoes.com')
soup = BeautifulSoup(html, "lxml")
titles = soup.find_all('p',{'class':'title noSpacing'})

def main():
	for title in titles:
		lcd_init()
		movie = title.string
		movie_len = len(movie)
		if movie_len > 16:
			movie2 = movie[16:movie_len]
			lcd_string('%s' % (movie), LCD_LINE_1,1)
			lcd_string('%s' % (movie2),LCD_LINE_2,1)
			time.sleep(5)
		else:
			lcd_string('%s' % (movie), LCD_LINE_1,1)
			time.sleep(5)
			


if __name__ == '__main__':
	main()