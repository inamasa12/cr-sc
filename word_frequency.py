# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:43:38 2020

@author: mas
"""

import sys
import os
from glob import glob
from collections import Counter

import MeCab

# メイン

#見出し語以外のテキストが段落ごとに抽出されている

def main():

	input_dir = sys.argv[1]

	tagger = MeCab.Tagger('')
	tagger.parse('')

	frequency = Counter()
	count_proccessed = 0

	for path in glob(os.path.join(input_dir, '*', 'wiki_*')):
		print('Processing {0}...'.format(path), file=sys.stderr)
		with open(path, encoding='utf-8') as file:
			#項目ごとにテキスト文をループ、名詞をカウント
			for content in iter_docs(file):
				tokens = get_tokens(tagger, content)
				#カウンターの処理
				frequency.update(tokens)
				count_proccessed += 1
				if count_proccessed % 10000 == 0:
					print('{0} documents were processed.'.format(count_proccessed),
						  file = sys.stderr)
	#上位30単語を出力
	for token, count in frequency.most_common(30):
		print(token, count)
			
#項目ごとに含まれる名詞をリスト化（重複あり）
def get_tokens(tagger, content):	
	tokens = []
	node = tagger.parseToNode(content)
	while node:
		category, sub_category = node.feature.split(',')[:2]
		if category == '名詞' and sub_category in ('固有名詞', '一般'):
			tokens.append(node.surface)
		node = node.next
	return tokens

# 項目ごとにテキストをまとめて出力、イテレーター
def iter_docs(file):
	for line in file:
		if line.startswith('<doc '):
			buffer = []
		#リストの要素を全結合し、出力
		elif line.startswith('</doc>'):
			content = ''.join(buffer)
			yield content
		else:
			buffer.append(line)

	
if __name__ == '__main__':
	main()

