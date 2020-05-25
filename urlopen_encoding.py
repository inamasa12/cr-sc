# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 18:48:29 2020

@author: mas
"""

import sys
from urllib.request import urlopen

#URLを取得
f = urlopen('http://sample.scraping-book.com/dp')

#エンコーディングを取得
encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr)

#バイト型をエンコードして取得
text = f.read().decode(encoding)
print(text)
