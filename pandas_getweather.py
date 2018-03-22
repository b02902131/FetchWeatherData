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
###############
import pandas as pd
from datetime import datetime, date, timedelta


#### You can modify start and end date here
start_date = date(2018,1,14)
end_date = date(2018,1,16)

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

	df =pd.read_html(url,encoding="utf-8")[1]
	df = df[1:]
	
	df = df.drop(df.index[0])
	df = df.set_index([0])

	keys.append(dt_str)
	frames.append(df)


print("  Concatenating Data Frame ...")
concat = pd.concat(frames, keys=keys)
result = concat
result.to_csv('out.csv')