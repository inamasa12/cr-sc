# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 21:45:26 2020

@author: mas
"""

"""
%bookmark crsc /Users/mas/learning/cr-sc
%cd crsc
%pwd
"""
.
import re
import sqlite3
from urllib.request import urlopen
from html import unescape

def main():
    html = fetch('http://sample.scraping-book.com/dp')
    books = scrape(html)
    save('books.db', books)

def fetch(url):
    #url = 'http://sample.scraping-book.com/dp'
    f = urlopen(url)
    encoding = f.info().get_content_charset(failobj="utf-8")
    html = f.read().decode(encoding)
    return html

def scrape(html):
    books = []
    #辞書のリストを作成
    for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        url = 'https://gihyo.jp' + url
        title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
        title = re.sub(r'<.*?>', '', title)
        title = unescape(title)
        books.append({'url': url, 'title': title})
    return books

def save(db_path, books):
    #db_path='books.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS books')
    c.execute('''
              CREATE TABLE books(
                      title text,
                      url text
                      )
              ''')
    c.executemany('INSERT INTO books VALUES (:title, :url)', books)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
    