import config, requests, pprint
from application import api, mongo
from flask import request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource
from datetime import datetime
from bs4 import BeautifulSoup

class Crawler_BNI(Resource):
	def __init__(self):
		self.username = request.form['user']
		self.pswd = request.form['password']
		self.url = config.BNIURL
		self.cmongo = mongo.db.sysbni

	def post(self):
		cookie = self.getCookie()
		return cookie

	def getCookie(self):
		s = requests.Session()
		post = {
			'__START_TRAN_FLAG__':'Y',
			'FORMSGROUP_ID__':'AuthenticationFG',
			'__EVENT_ID__':'LOAD',
			'FG_BUTTONS__':'LOAD/ACTION.LOAD=Y',
			'AuthenticationFG.LOGIN_FLAG':'1',
			'BANK_ID':'BNI01',
			'LANGUAGE_ID':'002'
		}
		header = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Connection':'keep-alive',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
		}
		url = self.url+'AuthenticationController?'
		r = s.get(url, params=post, headers=header)
		raw = BeautifulSoup(r.text)
		self.captcha = raw.find('img',{'id':'IMAGECAPTCHA'}).attrs.get('src')
		captcha = self.url+self.captcha
		return captcha

	# def saveDb(self, name, rqHead, rqPost, rsHead, rsData):
	# 	data = {
	# 		'name':name,
	# 		'requestHeader':dumps(rqHead),
	# 		'requestData':dumps(rqPost),
	# 		'responseHeader':dumps(rsHead),
	# 		'responseData':dumps(rsData),
	# 		'timestamp':datetime.now()
	# 	}
	# 	insert = {
	# 		name : data
	# 	}
	# 	cmongo = self.cmongo
	# 	if name == 'getCookie':
	# 		# insert data
	# 		dtId = cmongo.insert(insert)
	# 		self.dtId = dtId
	# 	else:
	# 		# update data
	# 		cmongo.update({'_id':self.dtId}, {"$set": insert}, upsert=False)

	# 	return self.dtId


api.add_resource(Crawler_BNI, '/bni/crawler')
