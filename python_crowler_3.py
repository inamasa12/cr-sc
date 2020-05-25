# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

#WEBクローリング

import requests
import lxml.html


def main():
    #Webページを取得、繰り返しアクセスするためSessionを使用
    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')
    #URLリストのジェネレータを取得
    urls = scrape_list_page(response)
    for url in urls:
        #各URLにアクセス
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)
        break
    

#WEBページ（html）を入力
def scrape_list_page(response):
    #htmlをパース
    root = lxml.html.fromstring(response.content)
    #URLを相対パスから絶対パスに変換
    root.make_links_absolute(response.url)
    #a要素のitemprop属性がurlの値を取得（CSSセレクター）
    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url

#各書籍の情報（タイトル、価格、目次）を取得
def scrape_detail_page():
    


if __name__ == '__main__':
    main()

