import datetime
import random
import time
from flask import Flask, request, make_response
from ultralytics import YOLO
import cv2

from config import save_path, \
    result_path, default_weights, default_model_json, weights_path, cache_save_model_path

from api import FileApi, ResultApi, ObjApi, WModelApi
from api import PageApi, ObjectPageApi, NumApi
from api import DeblurSearchApi, DeblurSearchNumApi

from models import File, WModel
from extension import db, cors

import os
import io
import sys
from PIL import Image
import requests

# 项目系统路径配置
curPath = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(curPath) + os.path.sep + os.path.sep)
sys.path.append(root_path)

# 创建flask项目
app = Flask(__name__)

# flask项目常量初始化设置
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///detection.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["model"] = YOLO(default_weights)
app.config["model_json"] = default_model_json
app.config["cls"] = app.config["model"].names

# 爬虫伪造头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
}

db.init_app(app)  # 注册实例化
cors.init_app(app)  # 注册跨域请求伪造相关

"""
对数据库的各个表相关操作添加相应路由规则
"""

file_view = FileApi.as_view('file_api')
app.add_url_rule('/files/', defaults={'fid': None},
                 view_func=file_view, methods=['GET'])  # 查询
app.add_url_rule('/files', view_func=file_view, methods=['POST'])  # 添加
app.add_url_rule('/files/<int:fid>', view_func=file_view,
                 methods=['GET', 'DELETE'])  # 查询，删除

wmodel_view = WModelApi.as_view('wmodel_api')
app.add_url_rule('/wmodel/', defaults={'wid': None},
                 view_func=wmodel_view, methods=['GET'])  # 查询
app.add_url_rule('/wmodel', view_func=wmodel_view, methods=['POST'])  # 添加
app.add_url_rule('/wmodel/<int:wid>', view_func=wmodel_view,
                 methods=['GET', 'PUT', 'DELETE'])  # 查询，修改，删除

result_view = ResultApi.as_view('result_api')
app.add_url_rule('/result/', defaults={'rid': None},
                 view_func=result_view, methods=['GET'])  # 查询
app.add_url_rule('/result', view_func=result_view, methods=['POST'])  # 添加
app.add_url_rule('/result/<int:rid>', view_func=result_view,
                 methods=['GET', 'DELETE', 'PUT'])  # 查询，删除，修改

obj_view = ObjApi.as_view('obj_api')
app.add_url_rule('/obj/', defaults={'rid': 1},
                 view_func=obj_view, methods=['GET'])  # 查询
app.add_url_rule('/obj', view_func=obj_view, methods=['POST'])  # 添加
app.add_url_rule('/obj/<int:rid>', view_func=obj_view,
                 methods=['GET', 'DELETE'])  # 查询，删除

"""
对数据库的各个表相关分页查找实现的路由规则
各个表相关总数输出实现路由规则
"""

page_view = PageApi.as_view('page_api')
app.add_url_rule('/page', view_func=page_view, methods=['GET'])

object_page_view = ObjectPageApi.as_view('objectPage_api')
app.add_url_rule('/objectPage/<int:rid>', view_func=object_page_view, methods=['GET'])

num_view = NumApi.as_view('num_api')
app.add_url_rule('/num', view_func=num_view, methods=['GET'])

"""
对数据库的各个表相关关键词实现模糊查找
各个表模糊查找相关总数输出实现路由规则
"""
deblur_view = DeblurSearchApi.as_view('deblurSearch_api')
app.add_url_rule('/deblurS', view_func=deblur_view, methods=['GET'])

deblur_view_num = DeblurSearchNumApi.as_view('deblurSearchNum_api')
app.add_url_rule('/deblurSNum', view_func=deblur_view_num, methods=['GET'])

"""
涉及到对数据库(相关消息传递)之外的功能
比如 显示图片，爬取图片，切换模型，图片检测，文件上传，文件删除等等
"""

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

"""
显示图片，上传图片相关操作
"""


@app.route('/img/<string:name>')
def show_img(name):
    img_url = save_path + name
    if request.method == 'GET':
        if name is None:
            pass
        else:
            image_data = open(img_url, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass


@app.route('/upload/pic/', methods=['POST'])
def upload_load():
    """
    从本地上上传图片到后端服务器上
    :return: json
    """
    try:
        filename = request.files.get('file').filename
        name = filename.split(".")[0] + "_" + str(int(time.time()))
        type = filename.split('.')[-1]
        origin = 'localhost://' + filename

        data = request.files.get('file')

        new_path = save_path + name + '.' + type
        data.save(new_path, buffer_size=10000000000)

        img = Image.open(new_path)  # 为了获取图片的长宽信息

        width, height = img.width, img.height
        return {
            'status': 'success',
            'message': '图片上传成功',
            'code': 200,
            'results': {
                'name': name,
                'type': type,
                'origin': origin,
                'width': width,
                'height': height,
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '图片上传出现异常',
            'info': str(e)
        }


@app.route('/upload/url', methods=['POST'])
def get_url_pic():
    """
    获取url上的图片
    :param url: 图片的url
    :return: json
    """
    try:
        url = request.json.get("url")
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            content = res.content
            file = url.split('/')[-1]
            name = file.split('.')[0] + '_' + str(int(time.time()))
            type = file.split('.')[-1]
            filePath = save_path + name + '.' + type

            # type = file.split('.')[-1]
            # name = file.split('.')[0]

            origin = url

            with open(filePath, 'wb') as f:
                f.write(content)
            f.close()

            img = Image.open(filePath)
            width, height = img.width, img.height

            return {
                'status': 'success',
                'message': '图片爬取成功',
                'code': 200,
                'results': {
                    'name': name,
                    'type': type,
                    'origin': origin,
                    'width': width,
                    'height': height,
                }
            }
        else:
            return {
                'status': 'fail',
                'message': '图片爬取失败',
                'code': res.status_code
            }

    except Exception as e:
        return {
            'status': 'error',
            'message': '图片爬取出现异常',
            'info': str(e)
        }


"""
模型相关操作，切换模型，显示某个模型细节，显示当前模型
"""


@app.route('/detail/model', methods=['GET'])
def show_model_detail():
    """
    查看某个模型的内部细节
    :param wid:
    :return:
    """
    try:
        args = request.args
        # print(model_json)
        path = weights_path + args.get('model_name') + '.pt'

        _cache_yolo: YOLO = YOLO(path)
        results = {
            'names': _cache_yolo.names,
            'params': _cache_yolo.model.yaml
        }
        return {
            'status': 'success',
            'message': '查看模型细节成功',
            'results': results
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': '查看模型细节失败',
            'info': str(e)
        }


@app.route('/current', methods=['GET'])
def show_current_model():
    """
    查看当前模型函数
    :return: json
    """
    try:
        return {
            'status': 'success',
            'message': '查看当前模型成功',
            'results': app.config["model_json"]
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '查看当前模型失败',
            'info': str(e)
        }


@app.route('/switch', methods=["PUT"])
def switch_model():
    """
    前端找wmodel类的参数 -> 获得参数 -> 切换模型
    切换模型，首先参数要从前端request哪里获得
    request.json格式是
    {
      "model_dataset": "bdd",
      "model_name": "yolov8l_bdd",
      "model_type": "yolov8",
      "wid": 1
    }

    :return: json
    """
    try:
        model_json = request.json
        name = model_json['model_name']

        if name is None:
            return {
                'status': 'error',
                'message': '切换模型失败',
                'info': '模型名字为空'
            }

        path = weights_path + model_json['model_name'] + '.pt'

        app.config["model"]: YOLO = YOLO(path)
        # print(app.config["model"].model.args)

        # print(app.config['model'])
        app.config["model_json"] = model_json
        app.config["cls"] = app.config["model"].names

        return {
            'status': 'success',
            'message': '切换模型成功',
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '切换模型失败',
            'info': str(e)
        }


@app.route('/upload/model/', methods=["POST"])
def save_model_cache():
    try:
        data = request.files.get('file')
        filename = request.files.get('file').filename
        type = filename.split('.')[-1]

        if type != 'pt':
            return {
            'status': 'error',
            'message': '传送的不是pt文件',
            }

        data.save(cache_save_model_path, buffer_size=10000000000)
        return {
            'status': 'success',
            'message': '模型暂缓成功',
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '模型暂缓出现异常',
            'info': str(e)
        }


"""
检测图片任务相关
"""


@app.route('/resultImg/<string:name>')
def show_result_img(name):
    """
    返回结果相关
    :param name: 结果文件名称
    :return:
    """
    img_url = result_path + name
    if request.method == 'GET':
        if name is None:
            pass
        else:
            image_data = open(img_url, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass


@app.route('/detect', methods=['POST'])
def detection():
    """
    实现检测的功能
    返回的json参数 与POST http://127.0.0.1:5000/result
    以及 POST http://127.0.0.1:5000/obj 配合使用

    前端找File类的参数 ->前端找现存文件 ->  绘制图片 -> 保存文件 -> 获得参数 -> 接下来添加数据库对应记录
                                         └─> 绘制失败则报错
    与 POST http://127.0.0.1:5000/result
    以及 POST http://127.0.0.1:5000/obj  结合使用

    最后前端获得检测结果将结果保存到后端上（result,objection表）
    request.json格式是
    {
    "fid": 2,
    "height": 720,
    "name": "b7a8e795-ff80fddf",
    "origin": "localhost://b7a8e795-ff80fddf.jpg",
    "timestamp": "Fri, 24 Feb 2023 19:04:44 GMT",
    "type": "jpg",
    "width": 1280
    }

    :return: json
    """
    try:
        detection_json = request.json

        filename = detection_json['name']
        type = detection_json['type']

        model = app.config["model"]
        cls = app.config["cls"]
        wid = app.config["model_json"]['wid']
        # print(cls)

        path = save_path + filename + '.' + type
        # print(path)
        results = model(path)

        length = 0
        info = []
        for result in results:
            boxes = result.boxes.data.cpu().numpy().tolist()
            length = len(boxes)

            # pic_data = []
            for j in range(length):
                pic_data = {
                    'x1': boxes[j][0],
                    'y1': boxes[j][1],
                    'x2': boxes[j][2],
                    'y2': boxes[j][3],
                    'conf': boxes[j][-2],
                    'cls': cls[int(boxes[j][-1])]
                }
                info.append(pic_data)

        res_plotted = results[0].plot(show_conf=True, line_width=2, font_size=3)
        timestamp = int(time.time())

        img_path = result_path + filename + '_' + str(timestamp) + '.' + type
        # print(res_plotted)
        cv2.imwrite(img_path, res_plotted)

        return {
            'status': 'success',
            'message': '检测成功',
            'results': {
                'log': {
                    'wid': wid,
                    'addition': '单独的检测任务',
                    'timestamp': timestamp,
                    'mission_type': 'detection',
                    'filename': filename,
                    'type': type,
                    'num': length
                },
                'objects': info
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '检测失败',
            'info': str(e)
        }


@app.route('/delete/result', methods=['DELETE'])
def delete_result():
    """
    这里的函数是实现删除结果图片文件，与 DELETE http://127.0.0.1:5000/result/<int:rid>
                               以及 DELETE http://127.0.0.1:5000/obj/<int:rid>  结合使用
    前端返回参数 ->前端找现存文件 ->  删除图片 -> 删除完成 -> 接下来删除数据库对应记录
                                   └─> 删除失败则报错
    request.json格式是
    {
        "addition": "单独的检测任务",
        "filename": "b7a8e795-ff80fddf",
        "mission_type": "detection",
        "num": 23,
        "rid": 1,
        "timestamp": 1677256499,
        "type": "jpg",
        "wid": 1
    }

    :return: json
    """
    try:
        result_json = request.json
        file = result_json['filename'] + '_' + str(result_json['timestamp']) + '.' + result_json['type']
        path = result_path + file
        os.remove(path)

        return {
            'status': 'success',
            'message': '删除记录图片成功',
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '删除记录图片失败',
            'info': str(e)
        }


@app.route('/delete/file', methods=['DELETE'])
def delete_file():
    """
    这里的函数是实现删除结果图片文件，与 DELETE   结合使用
    前端返回参数 ->前端找现存文件 ->  删除图片 -> 删除完成 -> 接下来删除数据库对应记录
                                   └─> 删除失败则报错

    request.json格式是,来自前端上面的
    {
          type: response.results.type,
          name: response.results.name,
    }
    :return: json
    """
    try:
        type = request.json.get("type")
        name = request.json.get("name")

        file_path = save_path + name + '.' + type
        # print(file_path)
        os.remove(file_path)
        # print(request.data)
        # print(request.json.get("type"), request.json.get('name'))
        # print(request.json)
        return {
            'status': 'success',
            'message': '删除图片成功',
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': '删除图片失败',
            'info': str(e)
        }
    pass


# @app.route('/delete/model', methods=['DELETE'])
# def delete_model():
#     """
#     这里的函数是实现删除结果图片文件，与 DELETE http://127.0.0.1:5000/result/<int:rid> 结合使用
#     前端返回参数 ->前端找现存文件 ->  删除图片 -> 删除完成 -> 接下来删除数据库对应记录
#                                    └─> 删除失败则报错
#     request.json格式是
#
#
#     :return: json
#     """
#     pass


"""
指令相关
"""


@app.cli.command('init')
def init():
    db.drop_all()  # 注销所有的数据库
    db.create_all()  # 创建所有数据库
    File.init_db()
    WModel.init_db()


if __name__ == '__main__':
    app.run(debug=True)
