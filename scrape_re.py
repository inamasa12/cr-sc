# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 11:51:36 2020

@author: mas
"""

import re
from html import unescape

with open('dp.html', encoding="utf-8") as f:
    html = f.read()

#必要な部分を網羅的に取得し、細部の処理をループさせる
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    #URL
    url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
    url = 'https://gihyo.jp' + url
    #title
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
    title = re.sub(r'<.*?>', '', title)
    title = unescape(title)
    print(url, title)
