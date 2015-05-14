import config
from functools import wraps
from flask import jsonify, request

def check_auth(username, password):
	return username == config.USERNAME and password == config.PASWD

def authenticate():
	message = {
		'status':'false',
		'message':'Unauthorized access.'
	}
	resp = jsonify(message)
	resp.status_code = 401
	resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'

	return resp

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth: 
			return authenticate()
		elif not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)

	return decorated