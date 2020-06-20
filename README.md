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



# 正規表現関係  
## 欲張り型（.\*）と非欲張り型（.\*?）のマッチ  
欲張り型では最も長い文字列と、非欲張り型では最も短い文字列とマッチさせる  
## 参考サイト
[分かりやすいpythonの正規表現の例](https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3)  

