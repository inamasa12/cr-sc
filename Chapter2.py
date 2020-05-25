# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

"""
%bookmark crsc /Users/mas/learning/cr-sc
%cd crsc
%pwd
"""

#クローリング、スクレイピング基礎

import re
import sys
from urllib.request import urlopen

#URLを取得
f = urlopen('http://sample.scraping-book.com/dp')

type(f)

#本文をバイト型で表示
f.read()
bytes_content = f.read()

#URL情報
f.status
f.getheader('Content-Type')

#HTTPヘッダーからエンコーディングを取得
encoding = f.info().get_content_charset(failobj="utf-8")

#metaタグからエンコーディングを取得
scanned_text = bytes_content[:1024].decode('ascii', errors='replace')
match = re.search(r'charset=["\']?([\w-]+)"', scanned_text)
if match:
    encoding = match.group(1)
else:
    encoding = 'utf-8'

match.group()
match.groups()

print('encoding:', encoding, file=sys.stderr)

"""
[]: 集合、or
?: 0 or 1
(): グループ
\w: 英数字
\s: 空白文字
+: >= 1
*: >= 0
{m,}: m回の繰り返し
.: 任意の一文字
.*: なるべく多い文字数にマッチ
.*?: なるべく少ない文字数にマッチ
"""

#バイト型をエンコードして取得
text = f.read().decode(encoding)
test = bytes_content.decode(encoding)
print(text)

#htmlファイルとして保存
with open("dp.html", mode='w',encoding="utf-8") as f:
    f.write(text)


#正規表現によるHTMLのスクレイピング

import re
from html import unescape

re.search(r'a.*c', 'abc123DEF')
re.search(r'a.*d', 'abc123DEF')
re.search(r'a.*d', 'abc123DEF', re.IGNORECASE)
re.search(r'a.*d', 'abc123DEF', re.I)

m = re.search(r'a(.*)c', 'abc123DEF')
m.group()
m.group(2)

m = re.search(r'\s(\w{2,})\s', 'This is a pen')


re.findall(r'\w{2,}', 'This is a pen')

re.sub(r'\w{2,}', 'That', 'This is a pen')


with open('dp.html', encoding="utf-8") as f:
    html = f.read()

#必要な部分を網羅的に取得し、細部の処理をループさせる
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    #URL
    #抽出
    url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
    url = 'https://gihyo.jp' + url
    #title
    #抽出
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
    #置き換え
    title = re.sub(r'<.*?>', '', title)
    #文字列表現をそろえる
    title = unescape(title)
    print(url, title)


chk = re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL)
url = re.search(r'<a itemprop="url" href="(.*?)">', chk[0]).group(1)
url = 'https://gihyo.jp' + url

title = re.search(r'<p itemprop="name".*?</p>', chk[4]).group(0)
title = title.replace('<br/>', ' ')
title = re.sub(r'<.*?>', '', title)
title = unescape(title)


#専用パッケージじよるXMLのスクレイピング

from xml.etree import ElementTree

#ElementTreeオブジェクトの取得
tree = ElementTree.parse('rss2.xml')
#rootのElementオブジェクトを取得
root = tree.getroot()

#channel/item要素をループ
for item in root.findall('channel/item'):
    #title要素、link要素をテキスト取得
    title = item.find('title').text
    url = item.find('link').text
    print(url, title)

    
#csvファイルによる保存
#リスト、リストのリスト
import csv
with open('top_cities.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    #ヘッダー
    writer.writerow(['rank', 'city', 'population'])
    #データ部、リストのリスト
    writer.writerows([
            [1, '上海', 24150000],
            [2, 'カラチ', 23500000],
            [3, '北京', 21516000],
            [4, '天津', 14722100],
            [5, 'イスタンブル', 14160467],
            ])

    
#jsonファイルによる保存
#辞書のリスト
import json
cities = [
        {'rank':1, 'city': '上海', 'population': 24150000},
        {'rank':2, 'city': 'カラチ', 'population': 23500000},
        {'rank':3, 'city': '北京', 'population': 21516000},
        {'rank':4, 'city': '天津', 'population': 14722100},
        {'rank':5, 'city': 'イスタンブル', 'population': 14160467}
        ]    
print(json.dumps(cities, ensure_ascii=False, indent=2))

with open('top_cities.json', 'w') as f:
    json.dump(cities, f, ensure_ascii=False, indent=2)


#SQLiteに保存
import sqlite3

conn = sqlite3.connect('top_cities.db')

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS cities')
c.execute('''
          CREATE TABLE cities(
          rank integer,
          city text,
          population integer
          )
          ''')          
c.execute('INSERT INTO cities VALUES (?, ?, ?)', (1, '上海', 24150000))
c.execute('INSERT INTO cities VALUES (:rank, :city, :population)',
          {'rank': 2, 'city': 'カラチ', 'population': 23500000})
c.executemany('INSERT INTO cities VALUES (:rank, :city, :population)', [
        {'rank': 3, 'city': '北京', 'population': 21516000},
        {'rank': 4, 'city': '天津', 'population': 14722100},
        {'rank': 5, 'city': 'イスタンブル', 'population': 14160467},
        ])

conn.commit()

c.execute('SELECT * FROM cities')

for row in c.fetchall():
    print(row)

conn.close()

"""
sqlite3 **.db
SQL;
.exit
"""


#エンコーディングの確認
import locale
locale.getpreferredencoding()

