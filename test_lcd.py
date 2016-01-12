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

tmp_dir=devel_dir+"/danalytics/thingsweb/weblib/recv"
sys.path.append(tmp_dir)
from lastvalue import *

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

def lsraspi():
	cmd = "ls|grep ball"
	return run_cmd(cmd)

def main():
	lcd_init()
	tstr = lsraspi()
	while True:
		lcd_string('%s' % (tstr), LCD_LINE_1,1)
		whiteLCDon()
	

if __name__ == '__main__':
	
  try:
    main()
    time.sleep(2)
  except KeyboardInterrupt:
    pass
  finally:
    lcd_init()
    lcd_byte(0x01, LCD_CMD)
    retstr = ip_chk()
    retstr = retstr[:-1]
    lcd_string('%s ET' %retstr,LCD_LINE_1,1)
    lcd_string("Goodbye!",LCD_LINE_2,1)
    GPIO.cleanup()
