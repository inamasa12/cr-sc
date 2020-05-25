# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:08:21 2020

@author: mas
"""

import os
import sys

from apiclient.discovery import build
from pymongo import MongoClient, DESCENDING

YOTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

# Main

def main():
	#DBの準備
	mongo_client = MongoClient('localhost', 27017)
	collection = mongo_client.youtube.videos
	collection.delete_many({})
	
	for items_per_page in search_videos('フロンターレ'):
		save_to_mongodb(collection, items_per_page)

	show_top_videos(collection)


def show_top_videos(collection):
	for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
		print(item['statistics']['viewCount'], item['snippet']['title'])

"""
	data_list = list()
	for item in collection.find():
		data_list.append(item)

	i = 15
	data_list[i]['snippet']['channelTitle']
	data_list[i]['snippet']['title']
"""
	
def save_to_mongodb(collection, items):
	#各ID毎に処理
	for item in items:
		item['_id'] = item['id']
		#statisticsの各データを数値に変換
		for key, value in item['statistics'].items():
			item['statistics'][key] = int(value)

	#MongoDBに保存
	result = collection.insert_many(items)
	print('Inserted {0} documents'.format(len(result.inserted_ids)),
	   file=sys.stderr)

#各IDのitemsを出力
def search_videos(query, max_pages=2):
	
	#セッションの構築	
	youtube = build('youtube', 'v3', developerKey=YOTUBE_API_KEY)
	#最初の50件のIDを取得するためのリクエストを作成
	search_request = youtube.search().list(
			part='id',
			q=query,
			type='video',
			maxResults=50,
			)
	
	# 各IDの詳細情報を取得、最大50件のページ毎にループ
	i = 0
	while search_request and i < max_pages:
		#IDの取得
		search_response = search_request.execute()
		video_ids = [item['id']['videoId'] for item in search_response['items']]
		#詳細情報の取得
		videos_response = youtube.videos().list(
			part='snippet,statistics',
			id=','.join(video_ids)
			).execute()
		yield videos_response['items']
		#次の50件のIDを取得するためのリクエストを作成
		search_request = youtube.search().list_next(
				search_request,
				search_response)
		i += 1

if __name__ == '__main__':
	main()

