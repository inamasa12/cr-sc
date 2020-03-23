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
`f=urlopen('URL')`: URLを指定して取得、ファイルオブジェクト同様の取り扱いが可能なHTTPResponseオブジェクトを得る  
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
### XMLパーサーによるRSSのスクレイピング  
`tree=ElementTree.parse('RSS')`: RSSを指定して取得、ElementTreeオブジェクトを得る  
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


# 正規表現関係  
## 欲張り型（.\*）と非欲張り型（.\*?）のマッチ  
欲張り型では最も長い文字列と、非欲張り型では最も短い文字列とマッチさせる  


