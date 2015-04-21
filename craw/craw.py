__author__ = 'Linbo Fan'

"""
  in case something wrong
  fanlinbo@outlook.com
  still
  the url of the movie will be aotu find
"""


from urllib2 import Request,urlopen,URLError,HTTPError
import config
import db
import time
from bs4 import BeautifulSoup
import re
import oscar_url
import random
import cookielib
import urllib2
import collections

def geturl(movieID):
	comment_url='http://movie.douban.com/subject/%s/comments' % movieID
	return comment_url

def get_page(url,data=None):
	req=Request(url,data=data,headers=config.headers)
	html=urlopen(req).read().decode('utf-8')
	return html

"""
def get_comment():
	comment={
		movieID:self.movieID,
		comment_info:{

		}
	}

	print 'input the movieID'
	movieID_to_craw=str(raw_input())
	url=geturl(movieID_to_craw)
	doc=get_page(url)
	soup=BeautifulSoup(doc)
	article=soup.find('div',class_='article')

	for comment in article.find_all('div',class_='comment-item'):
		profile={
			'movie':movieID_to_craw,
			'time':time.time()
		}
		user_info=comment.find('div',class_="avatar")
		pattern=re.compile(r'people//()//')
		comment_userid=pattern.find(user_info.a['href'])
		profile['userid']=comment_userid
		comment_content=comment.find('div',class_='comment').p.get_text()
		profile['comment']=comment_content
		star_info=comment.find('div',class_="comment").h3
		try:
			star=int(star_info.find('span',class_='comment_info')[3]['href'][-2:])/10
			profile['star']=star
		except Exception:
			profile['star']=0

		vote=int(star_info.find('span',class_='votes pr5').string)
		profile['vote']=vote

		db.insert_review(profile)
		#db.insert_review_by_movie
"""

def read_comment(article,movieID):
	print '---read comment----','length of article',len(article)
	comments=article.find_all('div',class_='comment-item')
	print 'comment num:',len(comments)
	if comments:
		print '-----find already----'

	for comment in comments:
		profile={
			'movie':movieID,
			#  'time':time.strftime('%Y-%m-%d %X',time.localtime())
			'time':time.time()
		}
		user_info=comment.find('div',class_="avatar")
		pattern=re.compile(r'people/(.*?)/')
		link=user_info.a['href']
		comment_userid=pattern.findall(link)[0]
		profile['userid']=comment_userid
		comment_content=comment.find('div',class_='comment').p.get_text()
		profile['comment']=comment_content
		star_info=comment.find('div',class_="comment").h3
		try:
			star_content=star_info.find('span',class_='comment-info')
			star_list=list(star_content)
			star=star_list[3]
			star_no=int(star['class'][0][-2:])/10
			profile['star']=star_no
		except Exception:
			profile['star']=0

		vote=int(star_info.find('span',class_='votes pr5').string)
		profile['vote']=vote
		print '---profile right----'
		save_comment(profile)




def find_next_page(comment_url,article):
	next=article.find('div',id='paginator').find('a',class_="next")
	next_url=comment_url+next['href']
	return next_url



def save_comment(profile):
	db.insert_review(profile)


def main():
	print """
	      #################################################
	           input the movie id


	           oooooooooooooooooo
	      #################################################
	      """
	movieID=str(raw_input())
	url=geturl(movieID)
	while url:
		time.sleep(0.1)
		try:
			doc=get_page(url)
		except Exception:
			return

		soup=BeautifulSoup(doc,from_encoding='utf-8')
		article=soup.find('div',class_='article')
		read_comment(article,movieID)
		url=find_next_page(url,article)
def get_safe_page(movie_url):
	req=Request(movie_url)
	try:
		doc=urlopen(req).read()
	except HTTPError,e:
		print 'the server couldn\'t fullfill the request'
		print 'Error code:',e.code
	except URLError,e:
		print e.reason
	return doc



def main_update():
	print """
	############################################################
	  a version: the movies which have been nominated as oscar
	  or U.S.A movie
	  or movie tagged by classic


	############################################################
	"""
	movies_url=oscar_url.american_url()
	for movieID in movies_url.keys():
		url=movies_url[movieID]+'comments'
		i=0
		while url and i<50:
			time.sleep(5)
			doc=get_safe_page(url)
			i=i+1
			soup=BeautifulSoup(doc)
			article=soup.find('div',class_='article')
			read_comment(article,movieID)
			url=find_next_page(url,article)


def comments_no(url):
	req=Request(url)
	doc=urlopen(req).read()
	soup=BeautifulSoup(doc)
	no_part=soup.find('div',class_="mod-hd")
	no_part2=no_part.find('h2')
	no_info=no_part2.find('span')
	no=no_info.find('a')
	no_text=no.get_text()
	num=int(str(no_text[3:-2]))
	return num

def main_version3(start_page=0,movie_num=3):
	print """
		the old crawler make too much useless redundancy

		"""
	#  movies_url=oscar_url.american_url()
	movies_url=get_movie_url(start_page,movie_num)
	print"""

	-----------read  file correctly-----------

	"""


	cookie_support=urllib2.HTTPCookieProcessor(cookielib.CookieJar())
	opener=urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
	urllib2.install_opener(opener)
	for movieID in movies_url.keys():
		url=movies_url[movieID]+'comments'
		comments_count=comments_no(movies_url[movieID])
		half_no=comments_count/2
		if half_no>1000:
			half_no=1000
		print """
		###############################
               constructed sucessfully
		##################################
		"""
		for i in range(half_no/20):
			sleep_interval=random.random()*100%10
			time.sleep(sleep_interval)
			print '----------sleep well--------'
			url_cur=url+'?start=%s&limit=20&sort=new_score' % str(i*20)
			try:
				doc=get_page(url_cur)
				print 'the length is:',len(doc)
			except urllib2.HTTPError,e:
				print e.code
			i+=1
			soup=BeautifulSoup(doc)
			article=soup.find('div',class_='article')
			if article:
				print '-----article right----','and the lenth is',len(article)
			read_comment(article,movieID)


		print """
		     finish read one movie
		     """
	return 0


def get_movie_url(start_page=0,urls=5):
	info_file=open('f:\\craw\\movie','r')
	start=0
	infos=collections.OrderedDict()
	for info in info_file.readlines():
		if start<start_page:
			start+=1
		elif start<(start_page+urls):
			info_list=info.split(' ')
			infos[info_list[0]]=info_list[1][:-1]
			start+=1
		else:
			pass
	info_file.close()
	return infos

if __name__ =='__main__':
	main_version3(0,1)



