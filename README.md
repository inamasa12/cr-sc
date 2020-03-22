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
### WEBページの取得  
`f=urlopen('URL')`: URLを指定して取得、ファイルオブジェクト同様の取り扱いが可能なHTTPResponseオブジェクトを返す  
`f.read()`: レスポンスボディをバイト型で出力  
`f.status`: ステータスコード  
`f.getheader('Content-Type')`: 指定したHTTPヘッダーの値を出力  
### エンコーディングの取得（HTTPヘッダーから）  
`encoding=f.info().get_content_charset()`: エンコーディングの取得  
`f.read().decode(encoding)`: レスポンスボディを文字列で出力  
### エンコーディングの取得（metaタグから）  
`scanned_text=f.read().decode('ascii', errors='replace')`: レスポンスボディからascii文字だけを文字列として取得  
`match=re.search(r'charset=["\']?([\w-]+)', scanned_test)`: charset属性の値を取得  
`f.read().decode(match.group(1)): レスポンスボディを文字列で出力  

# 正規表現関係  
## 欲張り型（.\*）と非欲張り型（.\*?）のマッチ  
欲張り型では最も長い文字列と、非欲張り型では最も短い文字列とマッチさせる  


