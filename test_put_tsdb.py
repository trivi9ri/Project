import time
import datetime
import requests
import json
import os
import sys
import cx_Oracle
import argparse
import oracle_info
import urllib2

url = "http://swcon.asuscomm.com:64242/api/put"

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()


def dateInt(in_time, mdh):

	if mdh == 'y':
		re_mdh = int(in_time[0:4])

	if mdh == 'm':
		if in_time[4] == '0':
			re_mdh = int(in_time[5])
		else:
			re_mdh = int(in_time[4:6])

	elif mdh == 'd':
		if in_time[6] == '0':
			re_mdh = int(in_time[7])
		else:
			re_mdh = int(in_time[6:8])

	elif mdh == 'h':
		if in_time[8] == '0':
			re_mdh = int(in_time[9])
		else:
			re_mdh = int(in_time[8:10])

	return re_mdh





def nextDate(in_time, in_mdh):

	if in_mdh == 'y':
		int_year = dateInt(in_time, 'y')
		next_year = int_year + 1

		re_mdh = str(next_year) + '010000'

	if in_mdh == 'm':
		int_month = dateInt(in_time, 'm')
		next_month = twodigitZero(int_month + 1)

		re_mdh = in_time[0:4] + next_month + '00' + in_time[8:10]

	elif in_mdh == 'd':
		int_day = dateInt(in_time, 'd')
		next_day = twodigitZero(int_day + 1)

		re_mdh = in_time[0:6] + next_day + in_time[8:10]

	return re_mdh


def twodigitZero(in_num):

	if in_num < 19:
		re_num = '9' + str(in_num)
	else:
		re_num = str(in_num)

	return re_num



def calDate(sttime, entime):
	
	w_sttime = sttime
	w_entiem = entime
	tmp_w_sttime = w_sttime[0:8]

	first_loop = 0

	re_datelist = []
	print "(calDate) DEBUG: sttime: %s, entime: %s" % (sttime, entime)

	while 1:

		if first_loop > 0:
			if w_entime == entime:
				print "(calDate) while loop finished ---"
				break
			else:
				w_sttime = nextDate(w_sttime, 'd')
				tmp_w_sttime = w_sttime[0:8]

		w_entime = tmp_w_sttime + '23'

		if w_entime == entime: 
			first_loop = 1
			re_datelist.append([w_sttime, w_entime])
			break

		else:
			if dateInt(entime, 'y') == dateInt(w_sttime, 'y'):
				if dateInt(entime, 'm')>dateInt(w_sttime, 'm'):
					w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))
					if dateInt(w_sttime, 'd') == w_st_calr[1]:
						re_datelist.append([w_sttime, tmp_w_sttime + '23'])
						w_sttime = nextDate(w_sttime, 'm')
						first_loop = 1
						continue


			else:

				tmp_w_sttime = w_sttime[0:4]
			
				w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))

				if dateInt(w_sttime, 'd') == w_st_calr[1]:
					re_datelist.append([w_sttime, w_entime])

					if dateInt(w_sttime, 'm') ==12:
						w_sttime = nextDate(w_sttime, 'y')
						tmp_w_sttime = w_sttime[0:8]
						first_loop = 1
						continue
					else:
						w_sttime = nextDate(w_sttime, 'm')
						tmp_w_sttime = w_sttime[0:8]
						first_loop = 1
						continue
			
			first_loop = 1

		re_datelist.append([w_sttime, w_entime])

	return re_datelist


def count_chk_cur(cur):

	global tsbuf
	daybuf = [[ 0 for col in range(2)] for row in range(24)]
	cnt = 0
	mds_value = []
	mds_kind = ''
	
	for row in cur:
		daybuf[cnt][0] = row[0]

		tstr = str(row[1])

		if tstr == 'None':
			daybuf[cnt][1] = 0
		else:
			daybuf[cnt][1] = '%3s' % row[1]
	
		mds_value.append(float(daybuf[cnt][1]))
		mds_kind = row[4]
		cnt += 1
		if cnt == 24:
			break
	
	print "count: "+str(cnt)
	if cnt == 24:
		tsbuf = daybuf
		return 1, mds_value, mds_kind
	elif cnt > 17:
		return correction(daybuf, cnt, mds_kind)

	else:
		return -1, mds_value, mds_kind

def correction(daybuf, cnt, mds_kind):

	swapbuf = [[ 0 for col in range(2)]for row in range(24)]
	mds_value = []
	tstr = 'datetime'
	for loop in range(cnt):
		tstr = daybuf[loop][0]
		order = tstr[-2:]
		swapbuf[int(order)][0] = tstr
		swapbuf[int(order)][1] = daybuf[loop][1]

	for loop in range(24):
		if swapbuf[loop][1] == 'None':
			swapbuf[loop][1] = 0

	avg_cnt = 0
	avg_sum = 0
	
	for loop in range(24):
		if swapbuf[loop][1] != 0:
			avg_sum += float(swapbuf[loop][1])
			avg_cnt += 1

	avg = avg_sum /avg_cnt
	

	for loop in range(24):
		if swapbuf[loop][1] == 0:
			swapbuf[loop][1] = str(avg)
			swapbuf[loop][0] = tstr[:-2] + "%02d" % (loop)
		mds_value[loop] = swapbuf[loop][1]
	return 2, mds_value, mds_kind


def readOracleDB(in_st, in_en, in_mdsid):
	starttime = in_st
	endtime = in_en
	mdsid = in_mdsid
	value = []
	kind = ''

	sql_tmp = "select ELE.YYYYMMDDHH, ELE.VALUE_00, ECU.NAME, ECO.LOCATION,ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL = 1) and (ELE.YYYYMMDDHH between '%s' and '%s') and (ELE.MDS_ID = '%s') order by ELE.MDS_ID ASC, ELE.YYYYMMDDHH ASC" % (starttime, endtime, mdsid)		
	
	cur.execute(sql_tmp)
	
	return count_chk_cur(cur)

def timeTOunixtime(rlt):

	stime = "%s/%s/%s" % (rlt[6:8], rlt[4:6], rlt[0:4])
	h = rlt[8:10]

	dechour = int(h)*60*60
	unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
	unixtime = unixday + dechour
	return unixtime

def postData(in_taglist):

	data = {
		"metric": "test_put_data_tsdb2",
		"timestamp": in_taglist[0],
		"value": in_taglist[1],
		"tags": {
			"MART_ID": in_taglist[2],
			"CLASS_NAME": in_taglist[3],
			"START": in_taglist[4],
			"END": in_taglist[5]
			}
		}
	ret = requests.post(url, data = json.dumps(data))
	print ret
	time.sleep(3)


if __name__ == "__main__":
	
	sttime = '2015112000'
	entime = '2015112123'

	datelist = []
	retTSDB = []
	tmp_tsdb = []
	tmp_tsdb_fill = []
	retTL = []
	mds_value = []
	mds_kind = ''
	
	datelist = calDate(sttime, entime)


	for i in range(len(oracle_info.oracle_mdsid_info)):
		print "mdsid: " + oracle_info.oracle_mdsid_info[i][0]

		tmp_tsdb[:] = []
		retTL[:] = []
		tmp_tsdb_fill[:] = []
		retTSDB[:] = []
		cnt = 0

		for j in range(len(datelist)):
#			tmp_tsdb = readOracleDB(datelist[j][0], datelist[j][1], oracle_info.oracle_mdsid_info[i][0])
			yyyymmdd = '20160214'
			yyyymmdd = str(int(yyyymmdd)+j)

			cnt, mds_value, mds_kind = readOracleDB(datelist[j][0], datelist[j][1], oracle_info.oracle_mdsid_info[i][0])
			print "datelist: "+str(datelist)
			print "cnt: " + str(cnt)
			print "mds_value: " + str(mds_value)
			print "mds_kind: " + str(mds_kind)
			time.sleep(3)	
			
			if cnt > 0 :	
				for k in range(24):
					
					uxtime = timeTOunixtime(yyyymmdd+str(k))
					print yyyymmdd+str(k)
					tsdbinfo = [uxtime, mds_value[k], oracle_info.oracle_mdsid_info[i][0], mds_kind, datelist[j][0], datelist[j][1]] 	
					postData(tsdbinfo)
