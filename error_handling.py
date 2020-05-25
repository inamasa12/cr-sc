# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:11:56 2020

@author: mas
"""

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


if __name__ == '__main__':
	main()



