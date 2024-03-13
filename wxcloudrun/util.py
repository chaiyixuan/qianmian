import uuid

def generate_uid():
    return str(uuid.uuid4())

from flask import Response, jsonify
from sqlalchemy.orm import class_mapper

#定义response返回类,自动解析json

# class JSONResponse(Response):
#     @classmethod
#     def force_type(cls, response, environ=None):
#         if isinstance(response, dict):  # 判断返回类型是否是字典(JSON)
#             response = jsonify(response)  # 转换
#         else:  # 对象,只用db,Model即可转json
            
#             columns = [c.key for c in class_mapper(response.__class__).columns]
#             response = jsonify(dict((c, getattr(response, c)) for c in columns))
#             return super().force_type(response, environ)
        
class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):  # 判断返回类型是否是字典(JSON)
            response = jsonify(response)  # 转换
        return super().force_type(response, environ)