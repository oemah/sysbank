import pprint
from application import app, api, auth
from flask import jsonify, request
from flask_restful import Resource

class Index(Resource):
	@auth.requires_auth
	def get(self):
		return {
			'status':'true',
			'message':'Welcome Oemah',
		}

# error handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'Status': 404,
            'Error': 'Not Found ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

api.add_resource(Index, '/')