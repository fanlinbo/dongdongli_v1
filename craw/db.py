# -*- coding:utf-8 -*-


from pymongo import MongoClient
import time

client=MongoClient('localhost',27017)
db=client.douban

def insert_review(review):
	db.review.save(review)
	time.sleep(0.01)
	print 'saved one review'