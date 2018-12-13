# -*- coding: utf-8 -*-

import urllib.request as eq
import re
import os
import time
import codecs

tplHead = '<!DOCTYPE html><html lang="zh-cn"><head><meta http-equiv="Content-Type"content="text/html;charset=utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>'+ '电影推荐'.encode('utf-8').decode('utf-8') +'</title></head><body><ul>'
tplFoot = '</ul></body></html>'
num = 0
page = 1
limit = 1000
magnetList = []
titleList = []
origin = 'https://www.dytt8.net'

def getMagnet(url):
	global titleList
	global magnetList
	global num
	
	html2=eq.urlopen(url).read().decode('gbk')
	html2=str(html2)
	pat2='<a href="(magnet:.+?)">'
	pat3='<h1><font color=#07519a>(.+?)</font></h1>'
	title=re.compile(pat3).findall(html2)
	magnet = re.compile(pat2).findall(html2)
	
	if len(magnet) > 0:
		magnetList += [magnet[0]]
		if len(title) > 0:
			titleList += [title[0]]
		
		num += 1
		print('第'+ str(num) +'部爬取完毕')
		# time.sleep(0.2)
	
def begin():
	global page
	
	if page > limit:
		createHtmlFile()
		print('爬取完毕！')
		return
		
	url='https://www.dytt8.net/html/gndy/dyzz/list_23_'+ str(page) +'.html'
	html1=eq.urlopen(url).read()
	html1=str(html1)
	pat1='t<a href="(\/.+?\.html)" class="ulink">'
	pageList = []
	pageList = re.compile(pat1).findall(html1)
	forEach(pageList)
	
def forEach(pageList):
	global page
	global origin
	global magnetList
	
	len1 = len(magnetList)

	for link in pageList:
		getMagnet(origin + link)

	if len(magnetList) == len1:
		createHtmlFile()
		print('爬取完毕！')
	else:
		page += 1
		print('开始爬取第'+ str(page) +'页')
		# time.sleep(0.5)
		begin()
	
def createHtmlFile():
	global titleList
	global magnetList
	global num

	message = ''
	title = ''
	
	for magnet in magnetList:
		index = magnetList.index(magnet)
		title = titleList[index]
		if(index+1)%20 == 0:
			message = message + '<li>-------------------------------------------</li>'
		else:
			message = message + '<li><a href="' + magnet + '">'+ title +'</a></li>'
		
		
	f = open('index.html', 'w+')
	f.write(tplHead + message + tplFoot)
	f.close()
	convert('E:\Python\python-movie\index.html')
	
def convert(file, in_enc="GBK", out_enc="UTF-8"):
    """
    该程序用于将目录下的文件从指定格式转换到指定格式，默认的是GBK转到utf-8
    :param file:    文件路径
    :param in_enc:  输入文件格式
    :param out_enc: 输出文件格式
    :return:
    """
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    try:
        f = codecs.open(file, 'r', in_enc)
        new_content = f.read()
        codecs.open(file, 'w', out_enc).write(new_content)
    except IOError as err:
        print("I/O error: {0}".format(err))

begin()
