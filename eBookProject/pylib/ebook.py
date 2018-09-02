# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse  import quote
import threading

home_url = "http://www.biquge.com.tw"
kv = {'user_agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  # 表示是一个浏览器
root = 'ebook/'

def get_chapter( titles,url,article,i ):
	#获取页面
	chapter = requests.get( url , headers=kv )
	chapter.raise_for_status()
	chapter.encoding = chapter.apparent_encoding
	chapter = chapter.text.replace( "&nbsp;&nbsp;" , ' ' )
	chapter = BeautifulSoup( chapter , "html.parser" )
	
	#获取章节标题
	chapter_title = chapter.find("title").text
	chapter_title = chapter_title[ :chapter_title.index("_") ].replace("\ufffd",'')
	
	#获取章节内容
	txt = chapter.find(id='content').text
	string = txt.replace('\u3000', '').replace('『', '“').replace('』', '”').replace('\ufffd', '').replace('\u30fb', '')  # 去除不相关字符
	string = string.split('\xa0')  # 编码问题解决
	string = list(filter(lambda x: x, string))
	for ii in range(len(string)):
		string[ii] = '    ' + string[ii]
		if "本站重要通知" in string[ii]:  # 去除文末尾注
			t = string[ii].index('本站重要通知')
			string[ii] = string[ii][:t]
	string = '\n'.join(string)
	
	string = '\n' + chapter_title + '\n\n' + string + '\n\n'
	string = string.replace('\ufffd', '').replace('\u30fb', '').replace('\u3000', '')
	
	#写入缓冲区
	article[i] = string
	titles[i] = chapter_title
	


def get_txt( home ):
	#获取书名
	title = home.find('head').find(attrs={'property': "og:novel:book_name"})['content']
	print(title)
	#获取章节列表
	contents = []
	for chapter in home.find_all("dd"):
		contents.append(home_url + chapter.find('a')['href'])
		#print( home_url + chapter.find('a')['href'] )

	#创建本地临时文件
	if not os.path.exists( root ):
		os.mkdir( root )
	with open( root + title + 's.txt', 'w') as f:
		f.write(title)
		f.close()

	#获取章节
	threads = []
	article = []
	titles = []
	for i in range( 0 , len(contents) , 8 ):
		with open( root+title+'s.txt' , 'a' ) as f:
			for j in range(8):
				if i+j < len(contents):
					article.append(" ")
					titles.append(" ")
					t = threading.Thread( target=get_chapter , args=( titles,contents[i+j],article,i+j) )
					threads.append( t )
					threads[i+j].start()
				else:
					break;

			for j in range(8):
				if i+j < len(contents):
					threads[i+j].join()
					f.write( article[i+j] )
		f.close()

	#重命名
	os.rename( root+title+'s.txt' , root+title+'.txt' )
	return root+title+'.txt'

def search_txt( bookname ):
	search_url = "https://www.biquge.com.tw/modules/article/soshu.php?searchkey=+"
	#搜索书名
	search_url += quote( bookname , encoding='gb2312' )
	home = requests.get( search_url , headers=kv )
	home.raise_for_status()
	home.encoding = home.apparent_encoding
	home = BeautifulSoup( home.text , "html.parser" )

	#判断书名是否完全匹配
	if home.title.text == "笔趣阁_书友最值得收藏的网络小说阅读网":
		return None
	else:
		return get_txt( home )
