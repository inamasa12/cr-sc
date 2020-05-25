# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 21:18:26 2020

@author: mas
"""

"""
%bookmark crsc /Users/mas/learning/cr-sc
%cd crsc
%pwd
"""

#robots.txt
import urllib.robotparser
import urllib

#読めない
rp = urllib.robotparser.RobotFileParser()
rp.set_url('http://gihyo.jp/robots.txt')
rp.read()
rp.can_fetch('*', 'http://gihyo.jp/book/genre/')
rp.crawl_delay('*')

f = urllib.request.urlopen("https://gihyo.jp/robots.txt")


#読める
rp = urllib.robotparser.RobotFileParser()
rp.set_url("http://www.musi-cal.com/robots.txt")
rp.read()
rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
False
rp.can_fetch("*", "http://www.musi-cal.com/")
True
rp.can_fetch("*", "http://www.musi-cal.com/wp-admin/")
False


# クローリングのエラー処理
	
import time
import requests
TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)


def main():
	response = fetch('http://httpbin.org/status/200, 404, 503')
	if 200 <= response.status_code < 300:
		print('Success!')
	else:
		print('Error!') 
			

def fetch(url):
	max_retries = 3
	retries = 0
	while True:
		try:
			print('Retrieving {0}...'.format(url))
			response = requests.get(url)
			print('Status: {0}'.format(response.status_code))
			if response.status_code not in TEMPORARY_ERROR_CODES:
				return response
		except requests.exceptions.RequestException as ex:
			print('Exception occured: {0}'.format(ex))
			retries += 1
			if retries >= max_retries:
				raise Exception('Too many retries.')
			#待ち時間は指数関数的に伸ばす
			wait = 2 ** (retries - 1)
			print('Waiting {0} seconds...'.format(wait))
			time.sleep(wait)
			

#デコレーターを使って書き換え


import requests
from retrying import retry

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)

def main():
	response = fetch('http://httpbin.org/status/200, 404, 503')
	if 200 <= response.status_code < 300:
		print('Success!')
	else:
		print('Error!') 


#リトライ処理はデコレートする
#関数は例外を発生させるように記述
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def fetch(url):
	print('Retrieving {0}...'.format(url))
	response = requests.get(url)
	print('Status: {0}'.format(response.status_code))
	if response.status_code not in TEMPORARY_ERROR_CODES:
		return response
	raise Exception('Temporary Error: {0}'.format(response.status_code))




	
url = 'http://httpbin.org/status/200, 404, 503'
fetch(url)



import requests
from cachecontrol import CacheControl

session = requests.session()
cached_session = CacheControl(session)

response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache)

#二回目がエラーになってしまう
response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache)



import re
value = '--'

if not re.search(r'^[0-9,]+$', value):
	raise ValueError('Invalid Price')

from voluptuous import Schema, Match

#ルール設定
schema = Schema({
		'name': str,
		'price': Match(r'^[0-9,]+$'),
		}, required=True)

#チェック
schema({'name': 'ぶどう',
		'price': '3,000',
		})

schema({'name': None,
		'price': '3,000',
		})
	

	
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

msg = MIMEText('テスト送信です。')
msg['Subject'] = Header('テスト', 'utf-8')
msg['From'] = 'masahiro.inaba.100@gmail.com'
msg['To'] = 'ba-ina.m@ezweb.ne.jp'
with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
	smtp.login('masahiro.inaba.100@gmail.com', os.environ['G_PASS'])
	smtp.send_message(msg)

