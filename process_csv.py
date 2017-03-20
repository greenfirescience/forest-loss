import os
import pandas as pd
import codecs

# Author: UNEP-WCMC
# Year: 1986
# Date: 2016-12-23 10:53:18
# Wdpaid: 10745
# hf93: 11.7525
# hf09: 17.0041
# hfcg: 5.2571

df = pd.read_csv('hffl.csv')
wh = pd.read_csv('wh_attr.csv', encoding='utf-8')


def get_fly(row):
	result = []

	for year in range(2001, 2013):
		col_name = 'Loss_area_' + str(year)
		result.append("{\"type\": 'forest-loss', \"year\": " + str(year) + ", \"forest loss\": " + str(row[col_name].iat[0]) + "}")

	result = ','.join(result)
	return "[" + result + "]"

def get_attr(wdpaid, field_name):
	row = wh[wh['wdpaid']==wdpaid]
	return row[field_name].iat[0]

def get_name(wdpaid):
	return get_attr(wdpaid, 'en_name')

def get_year(wdpaid):
	return get_attr(wdpaid, 'status_yr')

def get_country(wdpaid):
	return get_attr(wdpaid, 'country_name').replace(';', ', ')


def make_md_wdpaid(wdpaid):

	row = df[df['WDPAID']==wdpaid]

	lines = dict()
	lines['Title'] = get_name(wdpaid)
	lines['Tags'] = get_country(wdpaid)
	lines['Author'] = 'IUCN, UQ and WCS'
	lines['Year'] = get_year(wdpaid)

	lines['Date'] = 2017

	lines['wdpaid'] = wdpaid
	lines['hf93'] = row['HF_1993'].iat[0]
	lines['hf09'] = row['HF_2009'].iat[0]
	lines['hfcg'] = row['Change_HF_1993_2009'].iat[0]
	lines['fly'] = get_fly(row)
	lines['fc'] = row['Tree_area_2000'].iat[0]

	with codecs.open('.' + os.sep + 'content' + os.sep + str(wdpaid) + '.md', 'w', encoding='utf8') as f:
		for key in lines:
			f.write(key)
			f.write(': ')
			value = lines[key]
			if isinstance(value, unicode):
				f.write(value)
			else:
				f.write(str(value))
			f.write('\n')


def test_run():
	for wdpaid in df['WDPAID']:
		make_md_wdpaid(wdpaid)



