# Python クローリング&スクレピング
Python クローリング&スクレピング 学習用メモ  

## 第一章 クローリング・スクレイピングとは何か  
Linux関連の説明のため割愛  

## 第二章 Pythonで始めるクローリング・スクレイピング  
Pythonのデフォルト文字はUnicodeであり、バイト列へのエンコーディングにはUTF-8を用いる  
Python標準ライブラリによるクローリング・スクレイピング  

### パッケージ  
`from ullib.request import urlopen`  
`import re`  

### WEBページ（HTML）の取得  
`f=urlopen(URL)`: URLを指定して取得、ファイルオブジェクト同様の取り扱いが可能なHTTPResponseオブジェクトを得る  
`f.read()`: レスポンスボディをバイト型で出力  
`f.status`: ステータスコード  
`f.getheader('Content-Type')`: 指定したHTTPヘッダーの値を出力  

### HTMLのエンコーディング
* HTTPヘッダーから  
`encoding=f.info().get_content_charset()`: エンコーディングの取得  
`f.read().decode(encoding)`: レスポンスボディを文字列で出力  
* metaタグから  
`scanned_text=f.read().decode('ascii', errors='replace')`: レスポンスボディからascii文字だけを文字列として取得  
`match=re.search(r'charset=["\']?([\w-]+)', scanned_test)`: charset属性の値を取得  
`f.read().decode(match.group(1))`: レスポンスボディを文字列で出力  

### 正規表現によるHTMLのスクレイピング  
`m=re.search(r'a.\*c', 'abc123DEF')`: 最初に一致する文字列を取得し、m.group(0)は一致する文字列全体、m.group(1)は指定のキャプチャ部分を返す  
`m=re.findall(r'a.\*c', 'abc 12 3DEF')`: マッチする全ての部分（文字列）をリストで返す  
`m=re.sub(r'a.\*c', 'That', 'abc 12 3DEF')`: マッチする全ての部分を指定の文字列で置き換える  

### XMLパーサーによるRSS(XML)のスクレイピング  
`tree=ElementTree.parse('abc.xml')`: RSSを指定して取得、ElementTreeオブジェクトを得る  
`root=tree.getroot()`: root要素のElementオブジェクト（階層構造）を得る  
`items = root.findall('channel/item')`: channel要素直下のitem要素を全て取得、条件はXPathで指定  
`items[0].find('title').text`: item要素の文字列を取得、条件はXPathで指定  

### データの保存  
* CSV  
~~~
import csv
open('abc.csv', 'w', newline='', encoding='utf-8-sig') as f # EXCELで使用する場合
writer = csv.writer(f)
writer.writerows(list of list)
~~~
* JSON  
~~~
import json
open('abc.json', 'w') as f
json.dump(dictionary, f)
~~~
* SQLite3  
~~~
import sqlite3
conn = sqlite3.connect('abc.db')
c = conn.cursor()
c.execute(SQL)
conn.commit()
conn.close()
~~~

### Python Tips  
`str.replace('a', 'b')`: マッチする全ての部分を指定の文字列で置き換える  


## 第三章 強力なライブラリの活用  
サードパーティライブラリによるクローリング・スクレイピング  

### パッケージ  
`import requests`  

### WEBページ（HTML）の取得  
`r=requests.get(URL)`: URLを指定して取得、Responseオブジェクトを得る  
`r.status_code`: ステータスコード  
`r.headers['Content-Type']`: 指定したHTTPヘッダーの値を出力  
`r.encoding`: エンコーディングの取得  
`r.content`: レスポンスボディをバイト型で出力  
`r.text`: レスポンスボディを文字列で出力  
`r.json()`: レスポンスボディをjson形式で出力  

### HTTPによる送受信  
`requests.post(URL, data=dictionary)`: 送信  
`requests.get(URL, auth=(ID, Password))`: 認証付きの受信  
`s=requests.Session()`: 接続を継続して送受信を行う場合はセッションを共有する  

### lxmlによるHTMLスクレイピング  
~~~
import lxml.html
from urllib.request import urlopen
tree = lxml.html.parse(urlopen(URL)) #_ElementTreeオブジェクトを得る
html = tree.getroot() #root要素からなるHtmlElementオブジェクトを得る
h1 = html.xpath('//h1')[0] #h1要素（リスト）の一つ目、Xpathで指定
h1 = html.cssselect('h1')[0] #h1要素（リスト）の一つ目、cssセレクターで指定
h1.tag #タグ（要素名）を出力
h1.text #要素の値を出力
h1.get('id') #id属性の値を出力
h1.attrib #全属性の値を辞書として出力
h1.getparent() #親要素
~~~
### Beautiful SoupによるHTMLスクレイピング  
~~~
from bs4 import BeautifulSoup
open('abc.html') as f
soup = BeautifulSoup(f, 'html.parser')
soup.h1 #h1要素を出力
soup.h1.tag #タグ（要素名）を出力
soup.h1.string #要素の直接の子の文字列
soup.h1.text #要素内の全ての文字列
soup.h1['id'] #id属性の値を出力
soup.h1.get('id') #id属性の値を出力
soup.h1.attrs #全ての属性と値の辞書
soup.h1.parent #親要素
soup.find_all('h1') #全ての要素をリストで取得
soup.find_all('h1', class_='featured') #h1要素のclass属性がfeatured
soup.find_all(id='main') #id属性がmainの要素
soup.select(CSSセレクター) #CSSセレクターで抽出
~~~
### pyqueryによるHTMLスクレイピング  
CSSセレクターを用いた検索が可能  
~~~
from query import PyQuery as pq
d = pq(URL)
d('h1') #h1要素を取得
d('h1').text() #h1要素の文字列
d('h1').attr('id') #h1要素のid属性の値
d('h1').parent() #親要素
d('li.featured') #li要素のclass属性がfeatured
d('#main') #id属性がmain
d('body').find('li') #body要素の子孫からli要素を取得
d('li').filter('.featured') #li要素のclass属性がfeatured
d('li').eq(1) #取得したli要素の一番目
~~~
### feedparserによるRSS(XML)スクレイピング  
~~~
import feedparser
d = feedparser.parser(URL)
d.version # フィードのバージョン
d.feed.title # title要素
d.feed.link #link要素
d.feed.description #description要素
d.entries #各item要素をリストで取得
d.entries[0].updated #date要素
~~~
### データの保存  
* MySQL  
~~~
import MySQLdb
conn = MySQLDb.connect(db='abc', user='id', passwd='pass', charset='utf8mb4')
c = conn.cursor()
c.execute(SQL)
conn.commit()
conn.close()
~~~
* MongoDB  
~~~
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.abc #DBの作成
collection = db.xyz #コレクションの作成
collection.insert_one(dict)
collection.insert_many(list of dict)
~~~

### クローリング  
一覧ページと詳細ページの組み合わせで構成されるWEBサイトを前提  
1. 一覧ページからパーマリンク（URL）を抜き出す
~~~
import requests
import lxml.html
import from pymongo import MongoClient
response = requests.get(URL)
root = lxml.html.fromstring(response.content) #バイト型のレスポンスをパース
root.make_links_absolute(response.url) #全てのリンクを絶対パスに変換
for a in root.cssselect('#listBook a[itemprop="url"]') #id属性がlistBookの子孫で、a要素のitemprop属性がurlのものをリストで抽出
    url = a.get('href') #href属性を取得
~~~
1. スクレイプして辞書を作成  
~~~
ebook = {'url': response.url,
         'key': re.search(r'/([^/]+)$', response.url), #URLの最後の/以降をキーに使用
         'title': root.cssselect('#bookTitle')[0].text_content() #id属性がbookTitleの子孫で、全てのテキストを取得
         'price': root.cssselect('.buy')[0].text.strip() #class属性がbuyの直接のテキストを取得（前後の空白を削除）
         'content': [h3.text_content() for h3 in root.cssselect('#content > h3')], #id属性がcontent直下のh3要素をリストで抽出
         ,}
~~~
1. 追加のスクレイピング  
~~~
for i in ebook['content']:
    re.sub(r'\u3000+', ': ', i).strip() #'content'の空白をセミコロンに置き換える
~~~
1. 保存  
~~~
client = MongoClient('localhost', 27017)
collection = client.scraping.ebooks #scraping DBのebooksコレクション
collection.create_index('key', unique=True) #キーの設定
collection.insert_one(ebook)
~~~


## 第四章 実用のためのメソッド  

### クローラーの分類  
1. 状態を持つかどうか  
WEBサイトにアクセスする際に、Cookie同様の状態をクローラーに持たせる必要があるかどうか  
1. JavaScriptを解釈する必要があるかどうか  
必要な場合はヘッドレスブラウザー等を操作してクローリングさせる方法を選択する  
1. 不特定多数のサイトを対象とするかどうか  
クローラーの汎用性のレベルに影響を与える  

### 注意点  
適切な間隔をあける、連絡先を明示する、適切なエラー処理を準備する  
WEBページは著作物（著作権法の対象）となる  
2009年の著作権法改正で情報解析を目的とした複製は著作権者の許諾なく行えるようになってはいる  
WEBサイトの利用規約に従うこと  
WEBサイトに付属するrobot.txtや、robots metaタグにクローラーへの指示が記述されることがある
~~~
import urllib.robotparser
rp = urllib.rogotparser.RobotFileParser()
rp.set_url('URL')
rp.read()
rp.can_fetch('crawler', 'URL') # クローリングの可否を取得
~~~
クローリングが可能なURLをリスト化したXMLサイトマップが用意されている場合がある  
同時接続数は6以下、クロール間隔は1秒以上  
クローラーのUser-Agentヘッダーに連絡先を入れる  
HTTPステータスコードに応じて処理を分ける  
retryingパッケージを使用することで、作成した処理に対してリトライ処理を簡単にデコレートできる  

### 繰り返しを前提とした設計  
キャッシュ方針に関するHTTPヘッダーを利用することで更新されたデータだけを効率的にクロールする  
Voluptuousパッケージで効率的に内容変化を検知することができる  
メールを利用し変化を通知できる  
~~~
import smtplib
from email.mime.text import MIMEText
from email.header import Header
msg = MIMEText('テスト送信です。')
msg['Subject'] = Header('テスト', 'utf-8')
msg['From'] = 'MAIL ADDRESS'
msg['To'] = 'MAIL ADDRESS'
with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
	smtp.login('MAIL ADDRESS', 'PASSWORD')
	smtp.send_message(msg)
~~~

### Python Tips  
`export http_proxy=http://localhost:3128`: 環境変数にプロキシサーバーを設定する  


## 第五章 実践とデータの活用  

### Wikipediaデータのスクレイピング  
Wikipediaデータをスクレイピングする際には、Webサイトではなく、ダンプされたデータセットを利用する  
[Index of /jawiki/（データセットへのアクセスサイト）](https://dumps.wikimedia.org/jawiki/)  
jawiki-YYYYMMDD-pages-articlesX.xml.bz2: 記事ページの最新版のダンプ  
WikiExtractor.pyでダンプファイルをテキストに変換する ⇒ 後続は単純なテキストファイルのスクレイピング  
~~~
python WikiExtractor.py --no-templates -o articles -b 100M jawiki-YYYYMMDD-pages-articlesX.xml.bz2
~~~

### Twitterからのデータ収集  
Twitterデータ取得APIには、一件ごとにデータを取得するREST APIと、連続的に取得するStreaming APIがある  
APIの利用にはOAuth 1.0aによる認証があり、API KEY、API Secret Key、Access Token、Access Token Secretの4つが必要  
PythonパッケージTweepyが便利  

1. REST APIを使用
~~~
import tweepy
# 認証
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# クライアントインスタンスの作成とタイムラインの取得
api = tweepy.API(auth)
public_tweets = api.home_timeline()
# 出力
for status in public_tweets:
	print('@' + status.user.screen_name, status.text)
~~~
1. Streaming APIを使用
~~~
import tweepy
# 認証
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# 処理クラス
class MyStreamListener(tweepy.StreamListener):
	# ツイート取得時に実行するメソッド
	def on_status(self, status):
		print('@' + status.author.screen_name, status.text)
# クライアントインスタンスの作成と出力		
stream = tweepy.Stream(auth, MyStreamListener())
stream.sample(languages=['ja'])
~~~

### Amazonの商品情報の収集
優秀なアソシエイトでなければAPIが利用できない  

### YouTubeからの動画情報の収集  
GoogleのYouTube Data APIを利用する  
APIの利用にはOAuth 2.0aによる認証があり、API KEYが必要  
Google API Client for Pythonが便利  
~~~
from apiclient.discovery import build
# クライアントインスタンスの作成
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
# 取得データの検索
search_response = youtube.search().list(
		part = 'snippet',
		q='手芸',
		type='video',
		).execute()
# 出力		
for item in search_response['items']:
	print(item['snippet']['title'])
~~~

### PDFファイルからのデータ抽出
~~~
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
		#LTPageオブジェクト（ページ）の取得
		layout = device.get_result()
		#LTTextBoxのリストに展開
		boxes = find_textboxes_recursively(layout)
		#左上から、順にテキストボックスをソート(x0, y0, x1, y1)して表示
		boxes.sort(key=lambda b: (-b.y1, b.x0))
		for box in boxes:
			print('-' * 10)
			print(box.get_text().strip())

# LTPageオブジェクトをLTTextBox（テキストボックス）のリストに展開して返す
def find_textboxes_recursively(layout_obj):
	if isinstance(layout_obj, LTTextBox):
		return [layout_obj]
	if isinstance(layout_obj, LTContainer):
		boxes = []
		for child in layout_obj:
			boxes.extend(find_textboxes_recursively(child))
		return boxes
	return []
~~~

### Linked Open Dataからのデータ収集  
データ同士のリンク情報で公開されているものをLinked Open Dataと呼ぶ  
データのリンクはRDFという形式で記述されており、SPARQLというクエリ言語で抽出する  
日本ではDBpedia Japaneseが提供  
~~~
from SPARQLWrapper import SPARQLWrapper 

# データ取得インスタンスの設定
sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
sparql.setQuery(SPARQL)
# JSON形式で出力
sparql.setReturnFormat('json')
response = sparql.query().convert()
# 出力
for result in response['results']['bindings']:
	print(result['s']['value'], result['address']['value'])
~~~

### RoboBrowserを使用したGoogle検索情報の取得
~~~
from robobrowser import RoboBrowser

# ブラウザの設定と操作
browser = RoboBrowser(parser='html.parser')
browser.open('https://www.google.co.jp/')
form = browser.get_form(action='/search')
form['q'] = 'Python'
browser.submit_form(form, list(form.submit_fields.values())[0])

#出力（スクレイピング）
i=0
for a in browser.select('a > div[class="BNeawe vvjwJb AP7Wnd"], div > a[href^="/url"]'):
	if i % 2 == 0 and len(a.get('href')) < 400:
		href_all = a.get('href')
		m = re.search(r'q=(.*)&sa=', href_all)
		print(m.group(1))
	elif i % 2 != 0:
		print(a.text)
	i += 1
~~~

### Firefoxを用いたGoogle検索結果の取得（seleniumを使用）  
~~~
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#ブラウザにFirefoxを使用
options = FirefoxOptions()
# ヘッドレスモード
options.add_argument('-headless')
# FirefoxのWebDriverインスタンスを設定
driver = Firefox(options=options)
# Googleに接続
driver.get('https://www.google.co.jp/')
#入力フォームを取得し、検索実行
input_element = driver.find_element_by_name('q')
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)
# スクリーンショット
driver.save_screenshot('firefox_search_results.png')
# 検索結果を出力
for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    print(a.get_attribute('href'))
# ブラウザを終了
driver.quit()
~~~

### Chromeを用いたAmazon購入履歴の取得（seleniumを使用）  
~~~
from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# ChromeのWebDriverインスタンスを設定（ヘッドレスモード）  
options = ChromeOptions()
options.headless = True
driver = Chrome(options=options)
# Amazonサイトに接続
driver.get('https://www.amazon.co.jp/gp/css/order-history')
# 入力操作
email_input = driver.find_element_by_name('email')
email_input.send_keys(AMAZON_EMAIL)
email_input.send_keys(Keys.RETURN)
password_input = driver.find_element_by_name('password')
password_input.send_keys(AMAZON_PASSWORD)
password_input.send_keys(Keys.RETURN)

# 表示結果を出力
while True:
	# 一頁分のリストを出力
	for line_item in driver.find_elements_by_css_selector('.order-info'):
		order = {}
		for column in line_item.find_elements_by_css_selector('.a-column'):
			label_element = column.find_element_by_css_selector('.label')
			value_element = column.find_element_by_css_selector('.value')
			label = label_element.text
			value = value_element.text
			order[label] = value				
		print(order['注文日'], order['合計'])
	# 次頁に移動
	link_to_next = driver.find_element_by_link_text('次へ')
	link_to_next.click()
	
# ブラウザを終了
driver.quit()
~~~


### Chromeを用いてnoteのリストを取得し、RSSとして保存（seleniumを使用）  
~~~
import sys
import time
from selenium.webdriver import Chrome, ChromeOptions
import feedgenerator

# ChromeのWebDriverインスタンスを設定（ヘッドレスモード）  
options = ChromeOptions()
options.add_argument('--headless')
driver = Chrome(options=options)

#目的のWEBサイトに接続し、全体を表示させる
driver.get('https://note.mu/')
for i in range(15):
	driver.execute_script('scroll(0, document.body.scrollHeight)')
	time.sleep(2)

# スクレイピング（データの取得）
posts = []
for div in driver.find_elements_by_css_selector('div.o-timelineNoteItem'):
	a = div.find_element_by_css_selector('h3>a')
	posts.append({'url': a.get_attribute('href'),
			'title': a.text})

# ブラウザを終了
driver.quit()

# RSSファイル出力
with open('recommend.rss', 'w', encoding='utf-8') as f:
	feed = feedgenerator.Rss201rev2Feed(
			title='おすすめノート',
			link='//note.mu/',
			description='おすすめノート')
	for post in posts:
		feed.add_item(title=post['title'], link=post['url'], description='-', unique_id=post['url'])
	feed.write(f, 'utf-8')
~~~


### Yahoo!ジオコーダAPIを使用して、GeoJSONファイルを作成  
GeoJSON: 地理情報を格納するためのフォーマット  
~~~
import sys
import os
import json
import dbm
from urllib.request import urlopen
from urllib.parse import urlencode
 
While True:
	label = 名称
	address = 住所
	# Yahoo APIの使用
	url = YAHOO_GEOCORDER_API_URL + '?' + urlencode({
				'appid': os.environ['YAHOOJAPAN_APP_ID'],
				'output': 'json',
				'query': address,
				}) 
	response_text = urlopen(url).read()
	response = json.loads(response_text.decode('utf-8'))

	coordinates = response['Feature'][0]['Geometry']['Coordinates'].split(',')
	lon = float(coordinates[0])
	lat = float(coordinates[1])
	
	# GeoJSON形式でまとめる
	features.append({'type': 'Feature',
				'geometry':{'type': 'Point', 'coordinates': [lon, lat]},
				'properties': {'label': label, 'address': address},
				})

# GeoJSON形式でまとめる
feature_collection = {'type': 'FeatureCollection',
			'features': features,}

# 保存
with open('museums.geojson', 'w') as f:
	json.dump(feature_collection, f)
~~~


### Google BigQueryへのデータ保存  
~~~
from google.cloud import bigquery

client = bigquery.Client()

# データセットの準備（存在しなければ作成）
dataset_name = "twitter"
dataset_id = "{}.{}".format(client.project, dataset_name)
try:
	dataset = client.get_dataset(dataset_id)
except:
	dataset = bigquery.Dataset(dataset_id)
	dataset.location = "US"
	client.create_dataset(dataset) 

# テーブルの準備（存在しなければ作成）
table_name = 'tweets'
table_id = "{}.{}.{}".format(client.project, dataset_name, table_name)
table_names = [table.table_id for table in client.list_tables(dataset=dataset_id)]
if not table_name in table_names:
	print('Creating table {0}.{1}'.format(dataset_name, table_name), file=sys.stderr)
	schema = [
		bigquery.SchemaField('id', 'STRING', mode='REQUIRED', description='ツイートのID'),
		bigquery.SchemaField('lang', 'STRING', mode='NULLABLE', description='ツイートの言語'),
		bigquery.SchemaField('screen_name', 'STRING', mode='NULLABLE', description='ユーザー名'),
		bigquery.SchemaField('text', 'STRING', mode='NULLABLE', description='ツイートの本文'),
		bigquery.SchemaField('created_at', 'TIMESTAMP', mode='NULLABLE', description='ツイートの日時')
		]
	table = bigquery.Table(table_id, schema=schema)
	table = client.create_table(table)
table = client.get_table(dataset.table(table_name))

# データインサート
client.insert_rows_json(table, rows)
~~~


### Python Tips  
`pd.read_csv('**.csv', encoding, header, names, skipinitialspace, index_col, parse_dates)`: CSVからのインポート  
`pd.read_excel('**.xls', skiprows, skip_footer, parse_cols, index_col)`: EXCELからのインポート  


## 第六章 フレームワーク Scrapy  

Scrapyはクローリング・スクレイピングのためのフレームワーク  
Spiderクラスが処理の中心を担う  

### Spiderの基本形

`scrapy startproject myproject`で実行環境が作られる（myproject/myproject下に、items.py、pipelines.py、settings.pyが作成）  
基本的なコードは下記の形式（myproject/myproject/spider内に保存）  
各種コマンドはmyproject下で実行  
`scrapy crawl blogspider`で実行（-o bologs.jlで出力ファイルを指定）  
インタラクティブにスクレイピングを試行錯誤する場合は`scrapy shell URL`を用いる  


~~~
import scrapy
class BlogSpider(scrapy.Spider):
    name = 'blogspider'  # Spiderの名前
    allowed_domains = ["blog.scrapinghub.com"] # クロールを許可するドメイン
    start_urls = ['https://blog.scrapinghub.com']  # クロールを開始するURLのリスト
    
    # URLのレスポンスに対して実行されるメソッド
    def parse(self, response):
        # 投稿のタイトルをすべて出力
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}
        # 次のページに移動し、レスポンスに対してparseを再帰的に実行
        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse_topics)

    def parse_topics(self, response):
	# Headlineオブジェクトを作成
	item = Headline()  
	item['title'] = response.css('.pickupMain_articleTitle::text').get()
	item['body'] = response.css('.pickupMain_articleSummary').xpath('string()').get()
	yield item  # Itemをyieldして、データを抽出する。
~~~

### Items.py
取得したデータを格納しておくためのオブジェクト
データ取得用のクラス、そこに含まれるフィールドを定義できる
~~~
class Headline(scrapy.Item):
	title = scrapy.Field()
	body = scrapy.Field()
~~~

### CrawlSpider  
rulesにたどるべきリンクとコールバック関数を指定するだけで良い  
~~~
import scrapy.spiders
import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']

    # リンクをたどるためのルールのリスト
	# リンクの抽出、リクエスト、レスポンス処理関数の呼び出しを一度に行う
    rules = (
        # トピックスのページへのリンクをたどり、レスポンスをparse_topics()メソッドで処理する
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )
~~~

### SitemapSpider  
XMLサイトマップからクローリング  
~~~
from scrapy.spiders import SitemapSpider

class IkeaSpider(SitemapSpider):
    name = 'ikea'
    allowed_domains = ['www.ikea.com']

    # この設定がないと 504 Gateway Time-out となることがある
    custom_settings = {
        'USER_AGENT': 'ikeabot',
    }

    # robots.txtのURLを指定すると、SitemapディレクティブからXMLサイトマップのURLを取得する
    sitemap_urls = [
        'https://www.ikea.com/robots.txt',
    ]
	
    # サイトマップインデックスからたどるサイトマップURLの正規表現のリスト
    # sitemap_followを指定しない場合は、すべてのサイトマップをたどる
    sitemap_follow = [
        r'prod-ja-JP',  # 日本語の製品のサイトマップのみたどる
    ]
	
    # サイトマップに含まれるURLを処理するコールバック関数を指定するルールのリスト
    # sitemap_rulesを指定しない場合はすべてのURLのコールバック関数はparseメソッドとなる
    sitemap_rules = [
        (r'/products/', 'parse_product'),  # 製品ページをparse_productで処理する
    ]

    # 実際は該当するURLがないため下記コールバック関数は実行されない
    def parse_product(self, response):
        # 製品ページから製品の情報を抜き出す。
        yield {
            'url': response.url,  # URL
            'name': response.css('#name::text').get().strip(),  # 名前
            'type': response.css('#type::text').get().strip(),  # 種類
            'price': response.css('#price1::text').re_first('[\S\xa0]+').replace('\xa0', ' '),
        }
~~~

### Pipeline  
クローリング、スクリーニングの前後に行う処理を定義する  
pipelines.pyに記述  
settings.pyに処理順序等の設定を追加する必要がある（下記）
~~~
settings.py

ITEM_PIPELINES = {
 	#'myproject.pipelines.ValidationPipeline': 300, #Itemを検証するPipeline
	#'myproject.pipelines.MongoPipeline': 800, #ItemをMongoDBに挿入するPipeline
}
~~~

* MongoDBにデータを保存するPipeline
~~~
pipelines.py

from pymongo import MongoClient

class MongoPipeline:
    # Spider開始時の処理
    def open_spider(self, spider):
        # MongoDBに接続
        self.client = MongoClient('localhost', 27017)  # ホストとポートを指定してクライアントを作成
        self.db = self.client['scraping-book']  # scraping-book データベースを取得
        self.collection = self.db['items']  # items コレクションを取得

    # Spider終了時の処理
    def close_spider(self, spider):
        # MongoDBへの接続を切断
        self.client.close()

    # 取得したデータの処理
    def process_item(self, item, spider):
        # Itemをコレクションに追加する
        self.collection.insert_one(dict(item))
        return item
~~~

* MySQLにデータを保存するPipeline
~~~
pipelines.py
    # Spider開始時の処理
    def open_spider(self, spider):
        # MySQLサーバーに接続
        itemsテーブルが存在しない場合は作成する
        settings = spider.settings  # settings.pyから設定を読み込む。
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'scraping'),  # データベース名
            'user': settings.get('MYSQL_USER', ''),  # ユーザー名（setting.pyから取得）
            'passwd': settings.get('MYSQL_PASSWORD', ''),  # パスワード（setting.pyから取得）
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続
        self.c = self.conn.cursor()  # カーソルを取得

    # Spider終了時の処理
    def close_spider(self, spider):
        # MySQLサーバーへの接続を切断
        self.conn.close()

    # 取得したデータの処理
    def process_item(self, item, spider):
        # Itemをitemsテーブルに挿入
        self.c.execute('INSERT INTO `items` (`title`) VALUES (%(title)s)', dict(item))
        self.conn.commit()  # 変更をコミット
        return item
~~~

### Scrapyの設定  

下記の優先順序で指定した設定が用いられる  
1. コマンドライン  
1. Spider内のcustom_settings  
1. ブロジェクト毎のSettings.py  
1. scrapyコマンドのサブコマンド  
1. scrapy.settings.derault_settingsでグローバルに設定  

### 食べログのレストラン情報を取得  

CrawlSpiderを使用した処理  

~~~
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant

class TabelogSpider(CrawlSpider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1']

    # リンクをたどるためのルールのリスト
    # 一覧から個別頁へのリンクをたどり、レスポンスをparse_restaurant()メソッドで処理する
    rules = [
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')), # 一覧
	Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'), # 個別
    ]

    # コールバック関数
    # 地理情報を取得し、itemに収録
    def parse_restaurant(self, response):
        latitude, longitude = response.css(
                'img.js-map-lazyload::attr("data-original")').re(
                        r'markers=.*?%7C([\d.]+),([\d.]+)')
				
        item = Restaurant(
                name = response.css('.display-name').xpath('string()').extract_first().strip(),
				latitude = latitude,
				longitude = longitude,
				station = response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
				count = response.css('[property="v:count"]::text').extract_first()
				)

        yield item

~~~


### ライブラリを用いた独自関数の使用

Readabilityパッケージを用いたWEBデータのスクレイピング  

関数の定義（Utils.py）  
~~~
utils.py

import lxml.html
import readability

def get_content(html: str) -> Tuple[str, str]:
    
    # HTMLの文字列から (タイトル, 本文) のタプルを取得
    document = readability.Document(html)
    content_html = document.summary()
    
    # HTMLタグを除去して本文のテキストのみを取得する。
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text
~~~

本体  
~~~
import scrapy

from myproject.items import Page
from myproject.utils import get_content

class BroadSpider(scrapy.Spider):
    name = 'broad'
    start_urls = ['http://b.hatena.ne.jp/entrylist/all']

    def parse(self, response):
        # 個別のWebページへのリンクをたどってperse
        for url in response.css('.entrylist-contents-title > a::attr("href")').getall():
            yield scrapy.Request(url, callback=self.parse_page)
		
    #perse処理
    def parse_page(self, response):
        # utils.pyに定義したget_content()関数でタイトルと本文を抽出する
        title, content = get_content(response.text)
        yield Page(url=response.url, title=title, content=content)
~~~

### Elasticsearchへのデータ投入と検索サイトの作成  
データ投入  
~~~
import hashlib
import json

from elasticsearch import Elasticsearch

# Elasticsearchインスタンス
es = Elasticsearch(['localhost:9200'])

#index: news1, type: newsでインサート
#newsはtitle、bodyを要素に持つ
file_n = './myproject/news2.jl'
f =  open(file_n)
for line in f:
	news = json.loads(line)
	doc_id = hashlib.sha1(news['title'].encode('utf-8')).hexdigest()
	result = es.index(index='news1', doc_type='news', id=doc_id, body=news)
	print(result)
~~~

Bottleを使用した検索サーバー  
~~~
from typing import List  # 型ヒントのためにインポート

from elasticsearch import Elasticsearch
from bottle import route, run, request, template

es = Elasticsearch(['localhost:9200'])

@route('/')
def index():
    """
    / へのリクエストを処理する。
    """
    query = request.query.q  # クエリ（?q= の値）を取得する
    pages = search_pages(query) if query else []
    # queryとpagesの値を渡してレンダリングした結果をレスポンスボディとして返す
    return template('search', query=query, pages=pages)

def search_pages(query: str) -> List[dict]:
    # Simple Query Stringを使って検索する。
    result = es.search(index='news1', body={
        "query": {
            "simple_query_string": {
                "query": query,
                "fields": ["title^5", "body"],
                "default_operator": "or"
            }
        },
        # contentフィールドでマッチする部分をハイライトするよう設定
        "highlight": {
            "fields": {
                "body": {
                    "fragment_size": 150,
                    "number_of_fragments": 1,
                    "no_match_size": 150
                }
            }
        }
    })
    # 個々のページを含むリストを返す。
    return result['hits']['hits']
~~~

### Flickrから画像ファイルをDLし、人の顔を抽出  

画像ファイルのDL  

~~~
import os
from urllib.parse import urlencode
import scrapy

class FlickrSpider(scrapy.Spider):
    name = 'flickr'
    allowed_domains = ['api.flickr.com']

    # 初期化インスタンスをラップ
    def __init__(self, text='sushi'):
		
        super().__init__()  # 親クラスの__init__()を実行
	# クロールを開始するURLをFlickrのAPIに設定
        self.start_urls = [
            'https://api.flickr.com/services/rest/?' + urlencode({
                'method': 'flickr.photos.search',
                'api_key': os.environ['FLICKR_API_KEY'],  # FlickrのAPIキーは環境変数から取得。
                'text': text,
                'sort': 'relevance',
                'license': '4,5,9',  # CC BY 2.0, CC BY-SA 2.0, CC0を指定。
            }),
        ]

    def parse(self, response):
        # file_urlsというキーを含むdictをyieldし、画像処理関数に投げる
        for photo in response.css('photo'):
            yield {'file_urls': [flickr_photo_url(photo)]}

# 画像のURLを返す
def flickr_photo_url(photo: scrapy.Selector) -> str:
    attrib = dict(photo.attrib)  # photo要素の属性をdictとして取得
    attrib['size'] = 'b'  # サイズの値を追加
    return 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(**attrib)
~~~

顔を抽出  

~~~
import sys
import os
import cv2

output_dir = 'faces'

# 抽出器の設定 
cascade_path = 'C:/Users/mas/learning/cr-sc/haarcascade_frontalface_alt.xml'
classifier = cv2.CascadeClassifier(cascade_path)

for image_path in os.listdir(sys.argv[2]):

	image_path = './myproject/images/full/' + image_path
	
	#画像の読み込み、グレースケールに変換、顔を検出
	image = cv2.imread(image_path)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = classifier.detectMultiScale(gray_image)
	
	#顔フレームの書き込み
	image_name = os.path.splitext(os.path.basename(image_path))[0]
	for i, (x, y, w, h) in enumerate(faces):
		face_image = image[y:y + h, x: x + w]
		output_path = os.path.join(output_dir, '{0}_{1}.jpg'.format(image_name, i))
		cv2.imwrite(output_path, face_image)
~~~


## 第七章 クローラーの継続的な運用・管理  

### AWSを用いたクローラーの運営  

* サーバーの設定  
1. 権限を限定したIAMユーザーを作成  
1. EC2にログインするためのキーペア（**.pem）を作成  
1. 仮想サーバー（インスタンス）の作成（起動）  
1. Tera Termから、パブリックDNSにログイン  

* 運営環境設定  
1. Cronによるクローラー運営スケジュールの管理  
1. Postfixによるメール通知設定  

* クローリングとスクレイピングの分離  
送信側がクローリング結果と処理関数をキューに投入し、受信側がキューのジョブを処理する  
両者の作業を独立化させる  

~~~

# クローリング

import time
import re
# 型アノテーション用のパッケージ
from typing import Iterator
import logging

import requests
import lxml.html
from pymongo import MongoClient
from redis import Redis
from rq import Queue

def main():
    """
    クローラーのメインの処理
    """
    
    #Redisを使用してキューオブジェクトを作成
    q = Queue(connection=Redis())

    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続
    
    # URL保存用のコレクションを準備
    collection = client.scraping.ebook_htmls
    collection.create_index('key', unique=True)

    # 目標のサイトにアクセス
    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)  # 詳細ページのURL一覧
    
    for url in urls:
        key = extract_key(url)  # URLからキーを取得する
        # MongoDBからkeyに該当するデータを探す
        ebook_html = collection.find_one({'key': key})  
        # MongoDBに存在しない場合だけ、詳細ページをクロールする
	if not ebook_html:
            time.sleep(1)
            logging.info(f'Fetching {url}')
            response = session.get(url)  # 詳細ページを取得する

            # HTMLをそのままMongoDBに保存する（スクレイピングはしない）
            collection.insert_one({
                'url': url,
                'key': key,
                'html': response.content,
            })
            # キューにタスク（処理用の関数と外生変数）を追加する
            q.enqueue('scraper_tasks.scrape', key, result_ttl=0)

def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url

def extract_key(url: str) -> str:
    """
    URLからキー（URLの末尾のISBN）を抜き出す
    """
    m = re.search(r'/([^/]+)$', url)  # 最後の/から文字列末尾までを正規表現で取得
    return m.group(1)

if __name__ == '__main__':
    main()



# スクレイピング

import re

import lxml.html
from pymongo import MongoClient

def scrape(key: str):
    """
    ワーカーで実行するタスク
    """
    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続
	
    # 指定キーのWEBデータを取得し、スクレイピング
    html_collection = client.scraping.ebook_htmls  # scrapingデータベースのebook_htmlsコレクション
    ebook_html = html_collection.find_one({'key': key})  # MongoDBからkeyに該当するデータを探す
    ebook = scrape_detail_page(key, ebook_html['url'], ebook_html['html'])

    # スクレイピングした結果を別のコレクションに保存
    ebook_collection = client.scraping.ebooks  # ebooksコレクションを得る
    # keyで高速に検索できるように、ユニークなインデックスを作成する
    ebook_collection.create_index('key', unique=True)
    # ebookを保存する
    ebook_collection.insert_one(ebook)

def scrape_detail_page(key: str, url: str, html: str) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで得る
    """
    root = lxml.html.fromstring(html)
    ebook = {
        'url': url,  # URL
        'key': key,  # URLから抜き出したキー
        'title': root.cssselect('#bookTitle')[0].text_content(),  # タイトル
        'price': root.cssselect('.buy')[0].text.strip(),  # 価格
        'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],  # 目次
    }
    return ebook

def normalize_spaces(s: str) -> str:
    """
    連続する空白を1つのスペースに置き換え、前後の空白を削除した新しい文字列を取得する。
    """
    return re.sub(r'\s+', ' ', s).strip()

~~~


# 正規表現関係  
## 欲張り型（.\*）と非欲張り型（.\*?）のマッチ  
欲張り型では最も長い文字列と、非欲張り型では最も短い文字列とマッチさせる  
## 参考サイト
[分かりやすいpythonの正規表現の例](https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3)  

