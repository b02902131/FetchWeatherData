###############
# Bigyo
# ---
# Fetch Data From CWB Observation Data Inquire System
#    link : http://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
# ---
# Inquriements:
# 	python3
#		pandas
#		datetime
# ---
# Usage:
#	Just modify start_date and end_date as you need and then run this program.
# ---
# Problems:
#	1. unicode will fail in .CSV
#	2. 


# Version2
#	Fetch then Insert to SQL database
#
#	the SQL config is in another file, which will be a safer way.
#
#
###############
import pandas as pd
from datetime import datetime, date, timedelta
import pyodbc
import math
import sys

if len(sys.argv) > 1:
	td = timedelta(days=int(sys.argv[1]))
else:
	td = timedelta(days=5)

def isFloat(string):
	try:
		float(string)
		return True
	except ValueError:
		return False


from sqlServerUtil import * 
# sqlServerUtil include (server, database, username, password)
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#### You can modify start and end date here
start_date = date.today() - td
end_date = date.today()			# you can use today
# end_date = date(2017,10,19)	# you can use this to customize day

print("  the date range is from", start_date, " to ", end_date)

d = start_date
delta = timedelta(days=1)

dt_list = []
while d <= end_date:
	dt_list.append(d)
	d += delta

keys = []
frames = []
url_pre = 'http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466880&stname=%25E6%259D%25BF%25E6%25A9%258B&datepicker='
for dt in dt_list:

	print ("  Downloading Data of %s ..."%(dt.strftime("%Y-%m-%d")))
	dt_str = dt.strftime("%Y-%m-%d")
	url = url_pre+dt_str

	df =pd.read_html(url)[1]
	df = df[1:]
	
	df = df.drop(df.index[0])
	df = df.set_index([0])

	values = df.values

	print("\tinsert to SQL database: ", server, ":", database)
	for h in range(len(values)):
		s = dt_str + " " + str(h)  	# s = date + time
		time_in_format = "%Y-%m-%d %H"
		t_in = datetime.strptime(s, time_in_format)
		time_out_format = "%Y-%m-%d %H:%M:%S"
		t_out = datetime.strftime(t_in, time_out_format)

		v = values[h]
		v_str = ""
		for i in range(len(v)):
			if not isFloat(v[i]) or math.isnan(float(v[i])):
				v_str += ", 0"
			else:
				v_str += ", "+str(v[i])	

		command = "DECLARE @dt datetime = " + "'" + t_out + "'"
		command += "\nBEGIN\n\tIF NOT EXISTS( SELECT *FROM WeatherNew WHERE ObsTime = @dt)"
		command += "\n\tBEGIN \n\t\tInsert into WeatherNew (ObsTime, StnPres, SeaPres, Temperature, Td_dew_point, RH, WS, WD, WSGust, WDGust, Precp, PrecpHour, SunShine, GloblRad, Visb) "
		command += "\n\t\tVALUES(@dt"+v_str+")"
		command += "\n\tEND\nEND"
		# print("cmd =",command)
		cursor.execute(command)

# to check whether it's success
# cmd2 = "Select * from WeatherNew"
# cursor.execute(cmd2)

# row = cursor.fetchone()
# print(row)

# while row:
# 	# print (str(row[0]) + " " + str(row[1]))
# 	row = cursor.fetchone()
# 	print(row)

cnxn.commit()
