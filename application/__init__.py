from flask import Flask, request, make_response
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from flask_restful import Api

app = Flask(__name__)

# config mongodb
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'sysbca'
mongo = PyMongo(app)

# output format
def output_json(obj, code, headers=None):
	resp = make_response(dumps(obj), code)
	resp.headers.extend(headers or {})
	return resp

DEFAULT_REPRESENTATIONS = {'application/json':output_json}
api = Api(app)
api.representation = DEFAULT_REPRESENTATIONS

# blueprint route
import application.index
import application.bca.controllers
import application.bni.controllers
