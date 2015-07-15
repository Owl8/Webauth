#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from os import path
import getpass
import json

try:
	import requests
except ImportError:
	print "requestsがインストールされていません"
	exit()
argvs = sys.argv
argc = len(argvs)

appPath = path.dirname(path.abspath(__file__))
if argc > 2:
	payload = {'name' : argvs[1], 'pass' : argvs[2], 'authid' : '2'}
elif argc > 1:
	pswd = getpass.getpass('input pass : ')
	payload = {'name' : argvs[1], 'pass' : pswd, 'authid' : '2'}
else:
	data = []

	try:
		for line in open(appPath + '/user.txt', 'r'):
			data.append(line.strip())
	except IOError:
		print "user.txt が開けません"
		while (True):
			yorn = raw_input("ユーザー名とパスワードを入力しますか[Y/n] : ").strip()
			if yorn == "n" or yorn == "N":		
				exit()
			elif yorn == "y" or yorn == "Y" or yorn == "":
				break
		data.append(raw_input("input username : ").strip())
		data.append(getpass.getpass("input pass : ").strip())

	payload = {'name' : data[0], 'pass' : data[1], 'authid' : '2'}

try:
	urlfile = open(appPath + '/url.txt', 'r')
except IOError:
	print "url.txt が開けません"
	exit()

try:
	rq = requests.post(urlfile.read().strip(), data=payload)
except requests.exceptions.ConnectionError:
	print "接続できませんでした"
	exit()

successText = ""
try:
	for line in open(appPath + '/success.txt', 'r'):
		successText = successText + line
except IOError:
	print "success.txt が開けません"
	print rq.text
	while(True):
		yorn = raw_input("今回の結果をsuccess.txtに書き込みますか[y/N] : ").strip()
		if yorn == "n" or yorn == "N" or yorn== "":
			exit()
		elif yorn == "y" or yorn == "Y":
			break
	successFile = open(appPath + '/success.txt', 'w')
	successFile.write(rq.text.encode('utf-8'))

if successText == rq.text.encode('utf-8'):
	print "認証成功"
else:
	print "認証失敗"
