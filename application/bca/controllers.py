import config, requests, pprint
from application import api, mongo
from flask import request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource
from datetime import datetime
from bs4 import BeautifulSoup

class Crawler_BCA(Resource):
	def __init__(self):
		self.username = request.form['user']
		self.pswd = request.form['password']
		self.url = config.BCAURL
		self.urlLogin = config.BCALOGIN
		self.cmongo = mongo.db.sysbca

	def post(self):
		cookie = self.getCookie()
		login = self.login(cookie)
		mutasi = self.mutasi(cookie)
		logout = self.logout(cookie)
		return cookie

	def getCookie(self):
		s = requests.Session()
		header = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Connection':'keep-alive',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
		}
		r = s.post(self.url, headers=header)
		self.saveDb('getCookie', header, '', r.headers, r.text)
		raw = BeautifulSoup(r.text)
		resp = {
			'dtcookie':s.cookies.get_dict(),
			'Submit':raw.find('input',{'name':'value(Submit)'}).attrs.get('value'),
			'actions':raw.find('input',{'name':'value(actions)'}).attrs.get('value'),
			'CurNum':raw.find('input',{'name':'value(CurNum)'}).attrs.get('value'),
			'user_ip':raw.find('input',{'name':'value(user_ip)'}).attrs.get('value'),
			'browser_info':raw.find('input',{'name':'value(browser_info)'}).attrs.get('value'),
			'mobile':raw.find('input',{'name':'value(mobile)'}).attrs.get('value'),
		}
		return resp

	def login(self, arg):
		post = {
			'value(actions)':arg['actions'],
			'value(CurNum)':arg['CurNum'],
			'value(user_ip)':arg['user_ip'],
			'value(browser_info)':arg['browser_info'],
			'value(mobile)':arg['mobile'],
			'value(Submit)':arg['Submit'],
			'value(pswd)':self.pswd,
			'value(user_id)':self.username,
		}
		header = {
			'Referer':self.url,
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Connection':'keep-alive',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
		}
		r = requests.post(self.urlLogin, data=post, cookies=arg['dtcookie'], headers=header)
		self.saveDb('getLogin', header, post, r.headers, r.text)
		return 'Login'

	def mutasi(self, arg):
		# get mutasi
		urlMutasi = 'https://ibank.klikbca.com/accountstmt.do?value(actions)=acctstmtview'
		refMutasi = 'https://ibank.klikbca.com/accountstmt.do?value(actions)=acct_stmt'
		post = {
			'value(D1)':0,
			'value(r1)':2,
			'value(x)':2,
			'value(fDt)':'0103',
			'value(tDt)':'3103',
			'value(submit1)':'View Account Statement'
		}
		header = {
			'Referer':refMutasi,
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Connection':'keep-alive',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
		}
		r = requests.post(urlMutasi, data=post, cookies=arg['dtcookie'], headers=header)
		self.saveDb('getMutasi', header, post, r.headers, r.text)
		return 'Mutasi'

	def logout(self, arg):
		post = {
			'value(actions)':'logout'
		}
		header = {
			'Referer':'https://ibank.klikbca.com/nav_bar/menu_bar.htm',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Connection':'keep-alive',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
		}
		r = requests.post(self.urlLogin, data=post, cookies=arg['dtcookie'], headers=header)
		self.saveDb('getLogout', header, post, r.headers, r.text)
		return 'Logout'

	def saveDb(self, name, rqHead, rqPost, rsHead, rsData):
		data = {
			'name':name,
			'requestHeader':dumps(rqHead),
			'requestData':dumps(rqPost),
			'responseHeader':dumps(rsHead),
			'responseData':dumps(rsData),
			'timestamp':datetime.now()
		}
		insert = {
			name : data
		}
		cmongo = self.cmongo
		if name == 'getCookie':
			dtId = cmongo.insert(insert)
			self.dtId = dtId
		else:
			cmongo.update({'_id':self.dtId}, {"$set": insert}, upsert=False)

		return self.dtId

api.add_resource(Crawler_BCA, '/bca/crawler')
