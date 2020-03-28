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
response = requests.get(URL)
root = lxml.html.fromstring(response.content) #バイト型のレスポンスをパース
for a in root.cssselect('a[itemprop="url"]') #a要素のitemprop属性がurlのものをリストで抽出
  url = a.get('href') #href属性を取得
~~~


# 正規表現関係  
## 欲張り型（.\*）と非欲張り型（.\*?）のマッチ  
欲張り型では最も長い文字列と、非欲張り型では最も短い文字列とマッチさせる  


