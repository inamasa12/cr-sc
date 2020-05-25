# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 22:03:05 2020

@author: mas
"""


"""
%bookmark crsc /Users/mas/learning/cr-sc
%cd crsc
%pwd
"""

#標準ライブラリ

import requests

r = requests.get('http://sample.scraping-book.com/dp')

r.status_code
r.headers['content-type']
r.encoding

#本文、文字列
r.text
#本文、バイト
r.content

r = requests.get('http://weather.livedoor.com/forecast/webservice/json/v1?city=130010')
r.json()

#POST処理に対するレスポンスを確認
r = requests.post('http://httpbin.org/post', data={'key1': 'value1'})
r.json()

#ヘッダーの指定
r = requests.get('https://httpbin.org/get',
                 headers={'user-agent': 'my-crawler/1.0 (+foo@example.com)'})
r.json()

#認証
r = requests.get('https://api.github.com/user',
                 auth=('inamasa12', 'aHLkn3ffJp5N4Q5'))
r.json()

#URLのパラメータ指定
r = requests.get('http://httpbin.org/get', params={'key1': 'value'})
r.json()

#セッション
s = requests.Session()
s.headers.update({'user-agent': 'my-crawler/1.0 (+foo@example.com)'})
r = s.get('https://gihyo.jp/')
r.text
r = s.get('https://gihyo.jp/dp')
r.text
r = s.get('http://sample.scraping-book.com/dp')
r.text


#lxml
#早い、XPathとCSSの両方がフルで使用できる

import lxml.html
from urllib.request import urlopen

#パース（構文解析）
#URLの直接指定、URLをオープンしたファイルオブジェクトを指定することも可能
tree = lxml.html.parse('index.html')
type(tree)
tree = lxml.html.parse('http://example.com/')
tree = lxml.html.parse(urlopen('http://example.com/'))

#htmlオブジェクトの取得
#文字列を直接読み込むこともできる
html = tree.getroot()
type(html)
html = lxml.html.fromstring('''HTML文''')

#マッチする要素のリスト
html.xpath('//li')
html.cssselect('li')

#マッチする要素
h1 = html.xpath('//h1')[0]
h1.tag
h1.text
h1.get('id')
h1.attrib
h1.getparent()

import lxml.html

tree = lxml.html.parse('index.html')
html = tree.getroot()
for a in html.cssselect('a'):
    print(a.get('href'), a.text)

html.cssselect('a')[1].get('href')
html.cssselect('a')[1].text




#Beautiful Soup
#簡単
from bs4 import BeautifulSoup

#ファイルオブジェクトで指定
#文字列を直接読み込むこともできる
with open('index.html',encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')

html = BeautifulSoup('''HTML文''')

#マッチするタグ、構成する属性等の取得
#タグ
soup.h1
type(soup.h1)
soup.h1.name
soup.li.string
type(soup.li.string)
soup.ul.text
type(soup.ul.text)
#属性
soup.h1['id']
soup.h1.get('id')
soup.li.attrs
soup.h1.parent
soup.li
soup.find('li')
soup.find_all('li')
soup.find_all('li', class_="num01")
soup.find_all(id='main')
#CSS形式
soup.select('li')
soup.select('li.num01')
soup.select('#main')

#同じ
chk1 = soup.find_all('li')
chk2 = soup.select('li')
chk3 = soup.select('#main')


#リンク要素（a）の抽出
from bs4 import BLeautifulSoup
                   
with open('index.html',encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
                  
for a in soup.find_all('a'):
    print(a.get('href'), a.text)

soup.find_all('a')[0].get('href')
soup.find_all('a')[1].text
soup.find_all('a')[1].string


#pyquery
from pyquery import PyQuery as pq

#読み込み
#URLの指定、直接文字列も可能
with open('index.html', encoding="utf-8") as f:
    html = f.read()
d = pq(html)
d = pq(url='http://example.com/')
d = pq('''HTML文''')

#抽出
d('h1') #タグ指定
type(d('h1'))
d('li')[0]
d('li').text()
d('h1').attr('id')  #属性指定
d('h1').attr.id
d('h1').attr['id']
d('h1').parent()    #親タグと属性
d('li')
d('li.change')
d('#main')
  
d('body').find('Li')
d('li').filter('.change')
d('li').eq(5)



#RSS(XML)
import feedparser

#ファイルパス、ファイルオブジェクト、文字列の指定も可能
d = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss')
type(d)
d.version
d.feed.title
d['feed']['title']
d.feed.link
d.feed.description
#各フィード
len(d.entries)
d.entries[0].title
d.entries[1].title
d.entries[0].link
d.entries[0].description
d.entries[0].updated
d.entries[0].updated_parsed



import feedparser

d = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss')
for entry in d.entries:
    print(entry.link, entry.title)


# 保存

# MySQL
import MySQLdb

conn = MySQLdb.connect(db='scraping', user='scraper', passwd='password', charset='utf8mb4')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS cities')
c.execute("""
          CREATE TABLE cities (
          `rank` integer, 
          `city` text, 
          `population` integer)
          """)
c.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 24150000))
c.execute('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', 
        {'rank': 2, 'city': 'カラチ', 'population': 23500000})
c.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', [
        {'rank': 3, 'city': '北京', 'population': 21516000},
        {'rank': 4, 'city': '天津', 'population': 14722100},
        {'rank': 5, 'city': 'イスタンブル', 'population': 14160467}
        ])
conn.commit()
c.execute('SELECT * FROM cities')
for row in c.fetchall():
    print(row)
conn.close()

# SELECT @@datadir;: データの保存先

c.close()

#Shift + @


#MongoDB

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
#データベースを取得
db = client.test
db = client['test']
#コレクションを取得
collection = db.spots
collection = db['spots']
#ドキュメントをインサート
collection.insert_one({'name': '東京スカイツリー', 'prefecture': '東京'})
collection.insert_many([{'name': '東京ディズニーランド', 'prefecture': '千葉'},
                        {'name': '東京ドーム', 'prefecture': '東京'}])
collection.find()
for spot in collection.find():
    print(spot)
    
for spot in collection.find({'prefecture': '東京'}):
    print(spot)
    
collection.find_one() #先頭を取得
collection.find_one({'prefecture': '千葉'})


import lxml.html

tree = lxml.html.parse('index.html')
html = tree.getroot()
client = MongoClient('localhost', 27017)
db = client.scraping
collection = db.links
collection.delete_many({})
for a in html.cssselect('a'):
    collection.insert_one({
            'url': a.get('href'),
            'title': a.text,
            })
for link in collection.find().sort('_id'):
    print(link['_id'], link['url'], link['title'])

collection.find_one()

-- bind_ip 127.0.0.1
27017
52438


"""
C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe" --config "C:\Program Files\MongoDB\Server\4.2\bin\mongod.cfg" --service
mongod --install --config "C:\Program Files\MongoDB\Server\4.2\bin\mongod.cfg" --service
mongod --install --config "C:\Program Files\MongoDB\Server\4.2\bin\mongod.cfg"
"""



#WEBクローリング



import requests
import lxml.html

#Webページを取得
response = requests.get('https://gihyo.jp/dp')
response.url
#htmlをパース
root = lxml.html.fromstring(response.content)
#URLを相対パスから絶対パスに変換
root.make_links_absolute(response.url)

#id属性がlistBookの要素の下にあり、a要素のitemprop属性がurlの要素を取得（CSSセレクター）
for a in root.cssselect('#listBook a[itemprop="url"]'):
    #href属性を取得
    url = a.get('href')
    print(url)

url = 'https://gihyo.jp/dp/ebook/2020/978-4-297-11298-1'
response2 = requests.get(url)
root2 = lxml.html.fromstring(response2.content)
response2.url
#id属性がbookTitleの0番目の要素の全ての文字列を取得
root2.cssselect('#bookTitle')[0].text_content()
#class属性がbuyの0番目の要素の直接の文字列のみを取得
root2.cssselect('.buy')[0].text.strip()
#id属性がcontentの要素の直接の子であるh3要素
root2.cssselect('#content > h3')

ebook = {
    'url': response2.url,
    'title': root2.cssselect('#bookTitle')[0].text_content(),
    'price': root2.cssselect('.buy')[0].text.strip(),
    'content': [h3.text_content() for h3 in root2.cssselect('#content > h3')],
    }

import re

#\s: タブ、スペース等空白文字全般
re.sub(r'\u3000', ': ', ebook['content'][1]).strip()
ebook['content'][1].strip()

#URLからキーを作成
url
#[^ab]: a、b以外
#$: 文字列の末尾
m = re.search(r'/([^/]+)$', url)
m.group(1)

re.search(r'([^/]+)$', url).group(1)
url

#最初にマッチする文字列
re.search(r'/([^]+)$', url).group(1)
re.search(r'/([^/]+)$', url).group(0)
re.search(r'([^/]+)$', url).group()
re.search(r'[dp]', url).group(0)
re.search(r'[epk]', url).group()

re.search(r'[^/]+$', url).group(0)
re.search(r'[^/]', url).group(1)


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
collection = client.scraping.ebooks
collection.create_index('key', unique=True)

collection.find_one({'key': re.search(r'[^/]+$', url).group(0)})