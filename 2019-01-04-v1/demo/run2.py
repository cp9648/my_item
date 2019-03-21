# -*- coding: utf-8 -*-
import re
import json

from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api

from pymongo import MongoClient
from bson.objectid import ObjectId


# ======================================================================

app = Flask(__name__)

# MongoDB配置
mongo_config = {
    'host': 'localhost',
    'port': 27017,
    'serverSelectionTimeoutMS': 500  # 超时时间设置(单位: 毫秒)
}

# --------------------------------------------------------

class CustomEncoder(app.json_encoder):
    '''自定义json编码器'''
    def default(self, obj):
        if isinstance(obj, ObjectId):
            # 如果是 ObjectId 类型，就在转为 str
            return str(obj)
        return app.json_encoder.default(self, obj)

# 让 jsonify() 支持 ObjectId
app.json_encoder = CustomEncoder

# --------------------------------------------------------

# RESTful API (有可能 RESTFUL_JSON 配置并不存在，所以需要区别对待)
if 'RESTFUL_JSON' in app.config:
    app.config['RESTFUL_JSON']['cls'] = CustomEncoder
else:
    app.config['RESTFUL_JSON'] = {'cls': CustomEncoder}

# 实例化 api（需要在 RESTFUL_JSON 设置之后）
api = Api(app)

# ======================================================================

class JobList(Resource):
    '''职位列表'''
    def get(self):
        # 获取分页参数
        req_page = request.args.get('page', '1')
        # 默认页码
        page = 1  # 第几页(从1开始)
        # 处理请求的得到的分页参数
        if req_page.isdigit():
            # 如果是合法的数据，就使用请求传入的page参数
            page = int(req_page)
        # 查询参数
        req_kw = request.args.get('kw', None)
        if not bool(req_kw):
            req_kw = request.args.get('keyword', None)

        client = MongoClient(**mongo_config)
        db = client['Jobs']
        page_size = 5  # 分页大小
        offset = (page - 1) * page_size
        condition = {}  #  查询条件
        if bool(req_kw):
            # re.escape(): 转义正则中的特殊字符
            # re.compile(): 从字符串中构造正则对象
            kw_pattern = r'{0}'.format(re.escape(req_kw), re.IGNORECASE)
            condition['Job_name'] = {
                '$regex': re.compile(kw_pattern)
            }
        # 分页查询
        data_list = db['JobList'].find(condition).limit(page_size).skip(offset)
        # 数据总条数
        total = db['JobList'].count_documents(condition)
        # 查询完毕后，关闭数据库
        client.close()

        data = {
            'total': total,
            'page': page,
            'size': page_size,
            'rows': list(data_list)
        }
        return data

api.add_resource(JobList, '/')

# ======================================================================

if __name__ == '__main__':
    app.run(debug=True)
