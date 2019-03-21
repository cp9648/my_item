# -*- coding: utf-8 -*-
'''
* 参考:
* https://github.com/flask-restful/flask-restful/issues/116#issuecomment-128419699
* https://stackoverflow.com/questions/41723252/json-serialisation-of-dates-on-flask-restful
'''
# import json
from datetime import datetime

from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api

from bson.objectid import ObjectId


app = Flask(__name__)

# class CustomEncoder(json.JSONEncoder):
class CustomEncoder(app.json_encoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, ObjectId):
            return str(obj)
        # return json.JSONEncoder.default(self, obj)
        return app.json_encoder.default(self, obj)

# jsonify
app.json_encoder = CustomEncoder

# RESTful API (有可能 RESTFUL_JSON 配置并不存在，所以需要区别对待)
if 'RESTFUL_JSON' in app.config:
    app.config['RESTFUL_JSON']['cls'] = CustomEncoder
else:
    app.config['RESTFUL_JSON'] = {'cls': CustomEncoder}

# 实例化 api（需要在 RESTFUL_JSON 设置之后）
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': 'world',
            'id': ObjectId('5'.ljust(24, '6'))  # 构造一个假的 ObjectId
        }

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
