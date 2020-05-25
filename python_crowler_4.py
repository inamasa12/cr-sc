# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

#WEBクローリング
import time
import re

import requests
import lxml.html
from pymongo import MongoClient

def main():
        
    client = MongoClient('localhost', 27017)
    #scrapingデータベースのebooksコレクションを作成
    collection = client.scraping.ebooks
    #keyフィールドとしてユニークなインデックスを設定
    collection.create_index('key', unique=True)
    
    #Webページを取得、繰り返しアクセスするためSessionを使用
    response = requests.get('https://gihyo.jp/dp')
    #URLリストのジェネレータを取得
    urls = scrape_list_page(response)
    #url_list = [str(url) for url in urls]

    for url in urls:
        #url = url_list[0]
        #キーの取得
        key = extract_key(url)
        #キーが同じ最初のドキュメントを取得
        ebook = collection.find_one({'key': key})
        #キーが同じドキュメントが存在しない場合
        if not ebook:
            #各URLにアクセス
            time.sleep(1)
            response = requests.get(url)
            #ebookコレクションのドキュメントを作成
            ebook = scrape_detail_page(response)
            #DBにドキュメントを追加
            collection.insert_one(ebook)
        print(ebook)

#WEBページ（html）を入力
def scrape_list_page(response):
    #htmlをパース
    root = lxml.html.fromstring(response.content)
    #URLを相対パスから絶対パスに変換
    root.make_links_absolute(response.url)
    #id属性がlistBookの子孫で、a要素のitemprop属性がurlの値を取得（CSSセレクター）
    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url

#各書籍の情報（タイトル、価格、目次）を取得
def scrape_detail_page(response):
    root = lxml.html.fromstring(response.content)
    ebook = {
            'url': response.url,
            'key': extract_key(response.url),
            'title': root.cssselect('#bookTitle')[0].text_content(),
            'price': root.cssselect('.buy')[0].text,
            'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],
            }
    return ebook

def extract_key(url):
    #末尾から遡って、最初の/までの文字列を取得
    m = re.search(r'([^/]+)$', url)
    return m.group(1)

#任意の空白文字を取り除く
def normalize_spaces(s):
    #return re.sub(r'\s+', ' ', s).strip()
    return re.sub(r'\u3000+', ': ', s).strip()

if __name__ == '__main__':
    main()



chk = {'a':0, 'b':1, 'c':3}
for val in chk:
    chk[val] += 1
