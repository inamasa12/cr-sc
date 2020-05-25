# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:17:48 2020

@author: mas
"""

"""
%bookmark crsc /Users/mas/learning/cr-sc
%cd crsc
%pwd
"""

import MeCab

tagger = MeCab.Tagger()
tagger.parse('')

node = tagger.parseToNode('すもももももももものうち')

while node:
	print(node.surface, node.feature)
	node = node.next


import sys
import os
from glob import glob
from collections import Counter

import MeCab

# メイン

#見出し語以外のテキストが段落ごとに抽出されている

def main():

	input_dir = sys.argv[1]

	tagger = MeCab.Tagger('')
	tagger.parser('')

	frequency = Counter()
	count_proccessed = 0

	for path in glob(os.path.join(input_dir, '*', 'wiki_*')):
		print('Processing {0}...'.format(path), file=sys.stderr)
		with open(path, encoding='utf-8') as file:
			#項目ごとにテキスト文をループ、名詞をカウント
			for content in iter_docs(file):
				tokens = get_tokens(tagger, content)
				#カウンターの処理
				frequency.update(tokens)
				count_proccessed += 1
				if count_proccessed % 10000 == 0:
					print('{0} documents were processed.'.format(count_proccessed),
						  file = sys.stderr)
	#上位30単語を出力
	for token, count in frequency.most_common(30):
		print(token, count)
			
#項目ごとに含まれる名詞をリスト化（重複あり）
def get_tokens(tagger, content):	
	tokens = []
	node = tagger.parseToNode(content)
	while node:
		category, sub_category = node.feature.split(',')[:2]
		if category == '名詞' and sub_category in ('固有名詞', '一般'):
			tokens.append(node.surface)
		node = node.next
	return tokens

# 項目ごとにテキストをまとめて出力、イテレーター
def iter_docs(file):
	for line in file:
		if line.startswith('<doc '):
			buffer = []
		#リストの要素を全結合し、出力
		elif line.startswith('</doc>'):
			content = ''.join(buffer)
			yield content
		else:
			buffer.append(line)
	

"""
どのようにTwitterのデータとAPIを使用するか
I am a quants analyst at an asset management company in Japan. Especially I'm in charge of foreign equity investment.
I want to use Twitter data and APIs to find out if they can be used for investment strategies.


Twitterのデータを分析するつもりか
Yes
I want to analyze the relationship between Twitter data and future asset prices and macro variables.

Twitterのどの機能を利用するか
I want to use Tweet, Retweet, like and follow. I want to analyze the relationship between then and future variables.

Twittetやそのデータをどこでどうやって使用するか

When Tweets or aggregate data are judged to be effective for  investment strategies, it will be used to explain the effect to internal companies and our customers.

"""

#直接的にTwitter APIを使用

import os

from requests_oauthlib import OAuth1Session

os.environ

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKE_SECRET']

twitter = OAuth1Session(CONSUMER_KEY,
						client_secret=CONSUMER_SECRET,
						resource_owner_key=ACCESS_TOKEN,
						resource_owner_secret=ACCESS_TOKEN_SECRET)

response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')
for status in response.json():
	print('@' + status['user']['screen_name'], status['text'])
	
	
#Twitter APIをラップしたパッケージを使用

# REST API、回数制限あり
	
import os 
import tweepy

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKE_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
public_tweets = api.home_timeline()
for status in public_tweets:
	print('@' + status.user.screen_name, status.text)


# Streaming API
	
import os 
import tweepy

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print('@' + status.author.screen_name, status.text)
		
stream = tweepy.Stream(auth, MyStreamListener())
stream.sample(languages=['ja'])


# YouTube
import os
from apiclient.discovery import build

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

# クライアントインスタンスの作成
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

search_response = youtube.search().list(
		part = 'snippet',
		q='手芸',
		type='video',
		).execute()
		
for item in search_response['items']:
	print(item['snippet']['title'])


import os
import sys

from apiclient.discovery import build
from pymongo import MongoClient, DESCENDING

YOTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

# Main

def main():
	#DBの準備
	mongo_client = MongoClient('localhost', 27017)
	collection = mongo_client.youtube.videos
	collection.delete_many({})
	
	for items_per_page in search_videos('手芸'):
		save_to_mongodb(collection, items_per_page)

	show_top_videos(collection)


def show_top_videos(collection):
	for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
		print(item['statistics']['viewCount'], item['snippet']['title'])

"""
	data_list = list()
	for item in collection.find():
		data_list.append(item)

	i = 15
	data_list[i]['snippet']['channelTitle']
	data_list[i]['snippet']['title']
"""
	
def save_to_mongodb(collection, items):
	#各ID毎に処理
	for item in items:
		item['_id'] = item['id']
		#statisticsの各データを数値に変換
		for key, value in item['statistics'].items():
			item['statistics'][key] = int(value)

	#MongoDBに保存
	result = collection.insert_many(items)
	print('Inserted {0} documents'.format(len(result.inserted_ids)),
	   file=sys.stderr)

#各IDのitemsを出力
def search_videos(query, max_pages=5):
	
	#セッションの構築	
	youtube = build('youtube', 'v3', developerKey=YOTUBE_API_KEY)
	#最初の50件のIDを取得するためのリクエストを作成
	search_request = youtube.search().list(
			part='id',
			q=query,
			type='video',
			maxResults=50,
			)
	
	# 各IDの詳細情報を取得、最大50件のページ毎にループ
	i = 0
	while search_request and i < max_pages:
		#IDの取得
		search_response = search_request.execute()
		video_ids = [item['id']['videoId'] for item in search_response['items']]
		#詳細情報の取得
		videos_response = youtube.videos().list(
			part='snippet,statistics',
			id=','.join(video_ids)
			).execute()
		yield videos_response['items']
		#次の50件のIDを取得するためのリクエストを作成
		search_request = youtube.search().list_next(
				search_request,
				search_response)
		i += 1
	
	

#more: ファイルの内容をページ毎に表示、ctrl+Cで中断可能
		
# Time Series Data
import pandas as pd

chk = pd.read_csv('exchange.csv', encoding='cp932')
chk.head()
df_exchange = pd.read_csv('exchange.csv', encoding='cp932', header=1, 
			names=['date', 'USD', 'rate'], index_col=0, parse_dates=True)

type(df_exchange.rate[0])
df_exchange.iloc[1:3,]
df_exchange[1:3]


from datetime import datetime

	s = 'R2.1.8'

def parse_japanese_date(s):
	base_years = {'S': 1925, 'H': 1988, 'R': 2018}
	era = s[0]
	year, month, day = s[1:].split('.')
	year = base_years[era] + int(year)
	return datetime(year, int(month), int(day))

parse_japanese_date('H5.5.24')

df_jgbcm = pd.read_csv('jgbcm_all.csv', encoding='cp932', index_col=0, 
					   parse_dates=True, date_parser=parse_japanese_date,
					   na_values=['-'], header=1)

df_jobs = pd.read_excel('第3表.xls', skiprows=3, skipfooter=3, 
						usecols='W, Y:AJ', index_col=0)

s_jobs = df_jobs.stack()
test = list(s_jobs.index)

def parse_year_and_month(year, month):
	year = int(year[:-1])
	month = int(month[:-3])
	year += (1900 if year >= 63 else 2000)
	return datetime(year, month, 1)

y, m = test[685]
parse_year_and_month(y, m)

df_exchange.head()
df_jgbcm.head()
s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]
s_jobs.head()

import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
plt.show()

import matplotlib

#日本語表示する場合は必須
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'bx-', label='１次関数')
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 'ro--', label='２次関数')
plt.xlabel('Xの値')
plt.ylabel('Yの値')
plt.title('matplotlibのサンプル')
plt.legend(loc='best')
plt.xlim(0, 6)
plt.savefig('advanced_graph.png',dpi=300)



#日本語対応
import matplotlib.font_manager as fm
fm.findSystemFonts()


#並べて表示

from datetime import datetime

import pandas as pd
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
import matplotlib.pyplot as plt

	#為替
	df_exchange = pd.read_csv('exchange.csv', encoding='cp932', header=1, 
		names=['date', 'USD', 'rate'], index_col=0, parse_dates=True)
	
	#国債金利
	df_jgbcm = pd.read_csv('jgbcm_all.csv', encoding='cp932', index_col=0, 
					   parse_dates=True, date_parser=parse_japanese_date,
					   na_values=['-'], header=1)
	
	#有効求人倍率
	df_jobs = pd.read_excel('第3表.xls', skiprows=3, skipfooter=3, 
					usecols='W, Y:AJ', index_col=0)
	s_jobs = df_jobs.stack()
	s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]

	min_date = datetime(1973, 1, 1)
	max_date = datetime.now()

	plt.subplot(3, 1, 1)
	plt.plot(df_exchange.index, df_exchange.USD, label='ドル/円')
	plt.xlim(min_date, max_date)
	#plt.ylim(50, 350)
	plt.legend(loc='best')
	plt.subplot(3, 1, 2)
	plt.plot(df_jgbcm.index, df_jgbcm['1年'], label='1年国債金利')
	plt.plot(df_jgbcm.index, df_jgbcm['5年'], label='5年国債金利')
	plt.plot(df_jgbcm.index, df_jgbcm['10年'], label='10年国債金利')
	plt.xlim(min_date, max_date)
	plt.legend(loc='best')
	plt.subplot(3, 1, 3)
	plt.plot(s_jobs.index, s_jobs, label='有効求人倍率')
	plt.xlim(min_date, max_date)
	plt.axhline(y=1, color='gray')
	plt.legend(loc='best')
	plt.savefig('historical_data.png',dpi=300)

	df_exchange.head()
	df_jgbcm.head()
	s_jobs.head()



def parse_japanese_date(s):
	base_years = {'S': 1925, 'H': 1988, 'R': 2018}
	era = s[0]
	year, month, day = s[1:].split('.')
	year = base_years[era] + int(year)
	return datetime(year, int(month), int(day))

def parse_year_and_month(year, month):
	year = int(year[:-1])
	month = int(month[:-3])
	year += (1900 if year >= 63 else 2000)
	return datetime(year, month, 1)


#グラフオブジェクトの操作
	
fig = plt.figure()
ax1 = fig.add_subplot(3, 1, 1)
ax1.set_xlim(min_date, max_date)
ax1.legend(loc='best')
ax1.plot(df_exchange.index, df_exchange.USD, label='円/ドル')
plt.show()



# PDFの加工
# 各テキストデータは座標軸で管理される


"""
python C:/Users/mas/Anaconda3/envs/cr_sc_env/Scripts/pdf2txt.py 000232384.pdf
python C:/Users/mas/Anaconda3/envs/cr_sc_env/Scripts/pdf2txt.py -n 000232384.pdf

"""

import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

#縦書きを許容
laparams = LAParams(detect_vertical=True)

#パーサーの設定
resource_manager = PDFResourceManager()
device = PDFPageAggregator(resource_manager, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)


#バイナリデータとして読み込み
with open(sys.argv[1], 'rb') as f:
	#ページ毎に処理
	for page in PDFPage.get_pages(f):
		#パース
		interpreter.process_page(page)
		#LTPageオブジェクトの取得
		layout = device.get_result()
		#LTTextBoxのリストに展開
		boxes = find_textboxes_recursively(layout)
		#左上から、順に各行をスキャン(x0, y0, x1, y1)
		boxes.sort(key=lambda b: (-b.y1, b.x0))
		for box in boxes:
			print('-' * 10)
			print(box.get_text().strip())
	
def find_textboxes_recursively(layout_obj):
	if isinstance(layout_obj, LTTextBox):
		return [layout_obj]
	if isinstance(layout_obj, LTContainer):
		boxes = []
		for child in layout_obj:
			boxes.extend(find_textboxes_recursively(child))
		return boxes
	return []


# Linked Open Data
from SPARQLWrapper import SPARQLWrapper 

sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
sparql.setQuery(r'''
				SELECT * WHERE {
					?s rdf:type dbpedia-owl:Museum ;
						prop-ja:所在地 ?address .
					FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
				} ORDER BY ?s
				''')
#位置情報がないデータも取得されてしまう
sparql.setQuery(r'''
				SELECT * WHERE {
					?s rdf:type dbpedia-owl:Museum ;
						prop-ja:所在地 ?address .
					OPTIONAL { ?s rdfs:label ?label . }
					OPTIONAL {
						?s prop-ja:経度度 ?lon_degree ;
							prop-ja:経度分 ?lon_minute ;
							prop-ja:経度秒 ?lon_second ;
							prop-ja:緯度度 ?lat_degree ;
							prop-ja:緯度分 ?lat_minute ;
							prop-ja:緯度秒 ?lat_second .
							}
					FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
				} ORDER BY ?s
				''')
sparql.setReturnFormat('json')
response = sparql.query().convert()
for result in response['results']['bindings']:
	if len(result) == 9 :
		print("{0}、経度:{1},{2},{3}、緯度:{4},{5},{6}".format(
				result['label']['value'], 
				result['lon_degree']['value'], result['lon_minute']['value'], result['lon_second']['value'],
				result['lat_degree']['value'], result['lat_minute']['value'], result['lat_second']['value']))


# Webページの自動操作
from robobrowser import RoboBrowser

browser = RoboBrowser(parser='html.parser')
browser.open('https://www.google.co.jp/')
form = browser.get_form(action='/search')
form['q'] = 'Python'
browser.submit_form(form, list(form.submit_fields.values())[0])

i=0
for a in browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"], div > a[href^="/url"]'):
	if i % 2 == 0 and len(a.get('href')) < 400:
		href_all = a.get('href')
		m = re.search(r'q=(.*)&sa=', href_all)
		print(m.group(1))
	elif i % 2 != 0:
		print(a.text)
	i += 1

#奇数はa.textでOK

for a in browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"]'):
	print(a.text)

for a in browser.select('div > a[href^="/url"]'):
	print(a.get('href'))


chk1 = browser.select('div[class="BNeawe vvjwJb AP7Wnd"]')
chk2 = browser.select('a[href^="/url"]')
chk3 = browser.select('div > a[href^="/url"]')
chk4 = browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"], div > a[href^="/url"]')
test = chk4[20].get('href')
len(chk4[1].text)
len(test)


import re

test
m = re.search(r'/url?q=(.*)&sa', test)
m = re.search(r'q=https://www.python.jp/&sa=', test)
m = re.search(r'q=(.*)&sa=', test)
m.group(1)


chk4[2].text

len(chk1)
len(chk2)
len(chk3)

chk3.select('*')


print(browser)

browser.select('*')
browser.select('body div')
browser.select('body')
browser.select('div > a')
browser.select('div > a[href^="/url"]')
browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"]')
type(chk)
chk.text

browser.attr
browser.select('div[class^="BNeawe"]')
browser.select('div[class^="BNeawe"]')
browser.select('div[class="BNeawe vvjwJb AP7Wnd"], div[class="BNeawe UPmit AP7Wnd"]')
browser.select('div[class="BNeawe vvjwJb AP7Wnd"]')
browser.select('div[class="BNeawe vvjwJb AP7Wnd"], div > a[href^="/url"]')
browser.select('a[href^="/url"]')
browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"]')
browser.select('div > a[href^="/url"]')
#class属性がBNeaweで始まるdiv要素
#href属性が/url?q=で始まるa要素
#a属性直下のclass属性がBNeaweで始まるdiv要素
"BNeawe vvjwJb AP7Wnd"
"BNeawe UPmit AP7Wnd"

<a href="/url?q=




#Firefox
#conda install geckodriverが必要

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#ブラウザにFirefoxを使用
options = FirefoxOptions()
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
options.add_argument('-headless')
# FirefoxのWebDriverオブジェクトを作成する。
driver = Firefox(options=options)

# Googleのトップ画面を開く。
driver.get('https://www.google.co.jp/')

# タイトルに'Google'が含まれていることを確認する。
assert 'Google' in driver.title

# 検索語を入力して送信する。
#入力フォームの取得
input_element = driver.find_element_by_name('q')
# 検索
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

# スクリーンショットを撮る。
driver.save_screenshot('firefox_search_results.png')

# 検索結果を表示する。
for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    print(a.get_attribute('href'))

driver.quit()  # ブラウザーを終了する。



#Google Chrome

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

#ブラウザにChromeを使用
options = ChromeOptions()
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = Chrome(options=options)

# Googleのトップ画面を開く。
driver.get('https://www.google.co.jp/')

# タイトルに'Google'が含まれていることを確認する。
assert 'Google' in driver.title

# 検索語を入力して送信する。
# 入力フォームの取得
input_element = driver.find_element_by_name('q')
# 検索
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

# タイトルに'Python'が含まれていることを確認する。
assert 'Python' in driver.title

# スクリーンショットを撮る。
driver.save_screenshot('chrome_search_results.png')

# 検索結果を表示する。
# HTMLの構成が変わっているため取得できない
for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    print(a.get_attribute('href'))

driver.find_elements_by_css_selector('*')

driver.quit()  # ブラウザーを終了する。



# Amazonの購入履歴を取得
import os
import logging

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#ログの出力（表示）レベルを設定
# logging.basicConfig(level=logging.INFO)
logging.root.setLevel(logging.INFO)

logging.critical('critical')
logging.error('error')
logging.warning('warning')
logging.info('info')
logging.debug('debug')
print(logging.root)
print(logging.__version__)

#認証情報
#システム環境変数とユーザー環境変数の和集合になっているよう
AMAZON_EMAIL = os.environ['AMAZON_EMAIL']
AMAZON_PASSWORD = os.environ['AMAZON_PASS']

#ブラウザにChromeを使用
options = ChromeOptions()

#最終的にヘッドレスにする
options.headless = True

driver = Chrome(options=options)

main()


def main():
	
	logging.info('Navigating...')
	driver.get('https://www.amazon.co.jp/gp/css/order-history')

	assert 'Amazonログイン' in driver.title

	email_input = driver.find_element_by_name('email')
	email_input.send_keys(AMAZON_EMAIL)
	email_input.send_keys(Keys.RETURN)

	password_input = driver.find_element_by_name('password')
	password_input.send_keys(AMAZON_PASSWORD)

	logging.info('Signing in...')
	password_input.send_keys(Keys.RETURN)
	
	while True:
		
		assert '注文履歴' in driver.title
		
		print_order_history()
		
		try:
			link_to_next = driver.find_element_by_link_text('次へ')
		except NoSuchElementException:
			break

		logging.info('Following link to next page...')
		link_to_next.click()

	driver.quit()


def print_order_history():
	
	for line_item in driver.find_elements_by_css_selector('.order-info'):
		order = {}
		for column in line_item.find_elements_by_css_selector('.a-column'):
			try:
				label_element = column.find_element_by_css_selector('.label')
				value_element = column.find_element_by_css_selector('.value')
				label = label_element.text
				value = value_element.text
				order[label] = value
			except NoSuchElementException:
				pass
				
		print(order['注文日'], order['合計'])



# note
# https://note.mu/

#Google Chrome

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

#ブラウザにChromeを使用
options = ChromeOptions()
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
#options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = Chrome(options=options)

# noteのトップ画面を開く。
driver.get('https://note.mu/')

# タイトルを確認する。
driver.title

#スクリーンショット
driver.save_screenshot('note-1.png')
#ブラウザサイズの変更とスクリーンショット
driver.set_window_size(800, 600)
driver.save_screenshot('note-2.png')

#各ブログのURL、タイトル、概要（これは現在のフォーマットでは取得できない）
div = driver.find_elements_by_css_selector('div.o-timelineNoteItem')[0]
a = div.find_element_by_css_selector('h3>a')
a.get_attribute('href')
a.text

driver.quit()  # ブラウザーを終了する。


#クラス化
import sys
import time
from selenium.webdriver import Chrome, ChromeOptions
import feedgenerator

main()

def main():
	#ブラウザにChromeを使用
	options = ChromeOptions()
	# ヘッドレスモードを有効にする
	options.add_argument('--headless')
	# ChromeのWebDriverオブジェクトを作成する。
	driver = Chrome(options=options)
	#目的のWEBサイトに接続
	navigate(driver)
	#データの取得
	posts = scrape_posts(driver)
	driver.quit()
	#標準出力
	"""
	for post in posts:
		print(post)
	"""
	#ファイル出力
	with open('recommend.rss', 'w', encoding='utf-8') as f:
		save_as_feed(f, posts)


#ファイル出力
def save_as_feed(f, posts):
	#RSSクラスの作成
	feed = feedgenerator.Rss201rev2Feed(
			title='おすすめノート',
			link='//note.mu/',
			description='おすすめノート')
	for post in posts:
		feed.add_item(title=post['title'], link=post['url'],
						   description='-', unique_id=post['url'])
	feed.write(f, 'utf-8')


#スクレイピング
def scrape_posts(driver):
	posts = []
	for div in driver.find_elements_by_css_selector('div.o-timelineNoteItem'):
		a = div.find_element_by_css_selector('h3>a')
		posts.append({
				'url': a.get_attribute('href'),
				'title': a.text})
	return posts

#画面表示
def navigate(driver):
	print('Navigating...', file=sys.stderr)
	driver.get('https://note.mu/')
	assert 'note' in driver.title
	for i in range(15):
		driver.execute_script('scroll(0, document.body.scrollHeight)')
		time.sleep(2)
		print('Waiting for contents to be loaded...', file=sys.stderr)




"""
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)
	print('Waiting for contents to be loaded...', file=sys.stderr)
"""

"""
python -m http.server
http://localhost:8000/recommend.rss
⇒ ブラウザには表示できなかった
"""

"""
rss自体はできている

from xml.etree import ElementTree
tree = ElementTree.parse('recommend.rss')
root = tree.getroot()
for item in root.findall('channel/item'):
	title=item.find('title').text
	print(title)
"""	
#https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&query=%e6%9d%b1%e4%ba%ac%e9%83%bd%e6%b8%af%e5%8c%ba%e5%85%ad%e6%9c%ac%e6%9c%a8
#https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&query=東京都台東区上野公園7番7号
#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&query=東京都台東区上野公園7番7号"
#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&query=%e6%9d%b1%e4%ba%ac%e9%83%bd%e6%b8%af%e5%8c%ba%e5%85%ad%e6%9c%ac%e6%9c%a8" | jq .
#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&query=%e6%9d%b1%e4%ba%ac%e9%83%bd%e5%8f%b0%e6%9d%b1%e5%8c%ba%e4%b8%8a%e9%87%8e%e5%85%ac%e5%9c%927%e7%95%aa7%e5%8f%b7"


#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&output=json&query=%e6%9d%b1%e4%ba%ac%e9%83%bd%e5%8f%b0%e6%9d%b1%e5%8c%ba%e4%b8%8a%e9%87%8e%e5%85%ac%e5%9c%927%e7%95%aa7%e5%8f%b7" | jq .
#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&output=json&query=%e6%9d%b1%e4%ba%ac%e9%83%bd%e6%b8%af%e5%8c%ba%e5%85%ad%e6%9c%ac%e6%9c%a8" | jq .

#DOSの場合、文字列がshift-jisでエンコードされるため、正しくレスポンスを受けることが出来ない
#先にutf-8でエンコードしたバイトデータでリクエストする
#curl -G "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=<ClientID>&output=json&query=東京都台東区上野公園7番7号" | jq .

#コマンドプロンプトのエンコーディング
#UTF-8に設定する場合
#chcp 65001
#chcp 932
# 65001: UTF-8
# 932: shift-jis(Default)


r_bytes = '%e6%9d%b1%e4%ba%ac%e9%83%bd%e6%b8%af%e5%8c%ba%e5%85%ad%e6%9c%ac%e6%9c%a8'
a = '東京都台東区上野公園7番7号'
a_utf8 = a.encode('utf-8')
a_utf8_str = str(a_utf8)
a_utf8_str.replace('\\', '%')
a_utf8 = a.encode('utf-8')
a_utf8_str = str(a_utf8)
a_utf8_str.replace('\\x', '%')

#yahooAPIはutf-8でエンコードしたバイナリデータしか受け付けない


# 美術館の位置情報
import sys
import os
import json
import dbm
from urllib.request import urlopen
from urllib.parse import urlencode

from SPARQLWrapper import SPARQLWrapper

YAHOO_GEOCORDER_API_URL = 'https://map.yahooapis.jp/geocode/V1/geoCoder'
geocoding_cache = dbm.open('geocoding.db', 'c')

main()

def main():

	features = []
	#SPARQLで取得した、各美術館の属性値を処理
	for museum in get_museums():
		#print(museum['label'])
		label = museum.get('label', museum['s'])
		address = museum['address']
		if 'lon_degree' in museum:
			lon = float(museum['lon_degree']) +	float(museum['lon_minute']) / 60 + \
				float(museum['lon_second']) / 3600
			lat = float(museum['lat_degree']) + float(museum['lat_minute']) / 60 + \
				float(museum['lat_second']) / 3600
		#SPARQLで取得できない場合は、YAHOO APIから取得
		else:
			lon, lat = geocode(address)
			
		#SPARQLに位置情報がない場合は、yahoo APIを用いる
		print(label, address, lon, lat)
		
		#結果をリストに保存
		features.append({
				'type': 'Feature',
				'geometry':{'type': 'Point', 'coordinates': [lon, lat]},
				'properties': {'label': label, 'address': address},
				})

	feature_collection = {
			'type': 'FeatureCollection',
			'features': features,
			}
	
	with open('museums.geojson', 'w') as f:
		json.dump(feature_collection, f)
			

# YAHOO API で位置情報を取得
def geocode(address):

	#キャッシュに位置データが無ければYAHOO APIから取得
	if address not in geocoding_cache:
		print('Geocoding {0}...'.format(address), file=sys.stderr)
		url = YAHOO_GEOCORDER_API_URL + '?' + urlencode({
				'appid': os.environ['YAHOOJAPAN_APP_ID'],
				'output': 'json',
				'query': address,
				}) 
		response_text = urlopen(url).read()
		#一旦、キャッシュに保存
		geocoding_cache[address] = response_text

	#キャッシュから位置データを取得	
	response = json.loads(geocoding_cache[address].decode('utf-8'))
	
	if 'Feature' not in response:
		return(None, None)

	coordinates = response['Feature'][0]['Geometry']['Coordinates'].split(',')
	return (float(coordinates[0]), float(coordinates[1]))


#美術館毎の属性辞書をジェネレート
def get_museums():
	
	print('Executing SPARQL query...', file=sys.stderr)
	
	#SPQRQLエンドポイント
	sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
	
	#type属性がMuseumで、所在地属性（address）が得られる
	#所在地属性に加えて、label属性、位置属性を取得
	#所在地属性に都道府県を含むもの
	sparql.setQuery(r'''
					SELECT * WHERE {
						?s rdf:type dbpedia-owl:Museum ;
							prop-ja:所在地 ?address .
					OPTIONAL { ?s rdfs:label ?label . }
					OPTIONAL {
						?s prop-ja:経度度 ?lon_degree ;
							prop-ja:経度分 ?lon_minute ;
							prop-ja:経度秒 ?lon_second ;
							prop-ja:緯度度 ?lat_degree ;
							prop-ja:緯度分 ?lat_minute ;
							prop-ja:緯度秒 ?lat_second .
							}
					FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
				} ORDER BY ?s
				''')
	
	sparql.setReturnFormat('json')
	
	response = sparql.query().convert()
	
	print('Got {0} results'.format(len(response['results']['bindings']), file=sys.stderr))
	#美術館毎にループ
	for result in response['results']['bindings']:
		#各属性の辞書を出力
		yield {name: binding['value'] for name, binding in result.items()}
		
		