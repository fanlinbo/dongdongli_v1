__author__ = 'Linbo Fan'

from urllib2 import Request,urlopen
from bs4 import BeautifulSoup
import re
import collections
import time
import config

def american_url(data=0):
	movie_url=collections.OrderedDict()

	#  url='http://movie.douban.com/tag/%%E5%%A5%%A5%%E6%%96%%AF%%E5%%8D%%A1?start=%s&type=T' % start_no
	#  url='http://movie.douban.com/tag/%%E7%%BE%%8E%%E5%%9B%%BD?start=%s&type=T' %start_no
	#  classic_url='http://movie.douban.com/tag/%%E7%%BB%%8F%%E5%%85%%B8?start=%s&type=T' % str(i*10)
	for i in range(30,50):
		#  url='http://movie.douban.com/tag/%%E5%%A5%%A5%%E6%%96%%AF%%E5%%8D%%A1?start=%s&type=T' % str(i*10)
		url='http://movie.douban.com/tag/%%E7%%BE%%8E%%E5%%9B%%BD?start=%s&type=T' % str(i*10)
		time.sleep(1)
		req=Request(url, headers=config.headers)
		try:
			doc = urlopen(req).read()
		except urllib2.URLError,e:
			print e.code
			return
		soup=BeautifulSoup(doc)
		for item in soup.find_all('div',class_='pl2'):
			content_url=item.a['href']
			pattern=re.compile(r'subject/(.*?)/')
			content=pattern.findall(content_url)[0]
			url_new=item.a['href']
			movie_url[content]=url_new


	return movie_url

if __name__=="__main__":
	movies=american_url()
	movies_url=open('movie','a')
	for i in movies.keys():
		movies_url.write(i)
		movies_url.write(' ')
		movies_url.write(movies[i])
		movies_url.write('\n')
	movies_url.close()
