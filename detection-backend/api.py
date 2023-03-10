import os
import shutil

from flask.views import MethodView, request
from models import File, WModel, Object, Result
from extension import db
from config import save_path, \
    result_path, img_url_show, result_url_show, cache_save_model_path, weights_path


class FileApi(MethodView):
    """
    后端接口部分 RESTful API风格
    """

    def __init__(self):
        super(FileApi, self).__init__()

    def get(self, fid):
        """
        查询数据
        :param fid: 文件id
        :return: json
        """
        try:
            if not fid:
                files: [File] = File.query.all()
                results = [
                    {
                        'fid': file.fid,
                        'name': file.name,
                        'timestamp': file.timestamp,
                        'type': file.type,
                        'origin': file.origin,
                        'width': file.width,
                        'height': file.height
                    }
                    for file in files
                ]

            else:
                file = File.query.get(fid)
                results = {
                    'fid': file.fid,
                    'name': file.name,
                    'timestamp': file.timestamp,
                    'type': file.type,
                    'origin': file.origin,
                    'width': file.width,
                    'height': file.height
                }

            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据查询出现异常',
                'info': str(e)
            }

    def delete(self, fid):
        """
        删除操作
        :param fid: 文件id
        :return: json
        """
        try:
            file: File = File.query.get(fid)
            db.session.delete(file)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据删除成功',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': '数据删除出现异常',
                'info': str(e)
            }

    def post(self):  # 添加数据
        """
        添加操作
        :return: json
        """
        try:
            height = request.json.get("height")
            width = request.json.get("width")
            name = request.json.get("name")
            type = request.json.get("type")
            origin = request.json.get("origin")

            file = File()

            file.name = name
            file.height = height
            file.width = width
            file.type = type
            file.origin = origin

            db.session.add(file)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据添加成功'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据添加出现异常',
                'info': str(e)
            }


class WModelApi(MethodView):
    """
    后端接口部分 RESTful API风格
    """

    def __init__(self):
        super(WModelApi, self).__init__()

    def get(self, wid):
        """
        查询数据
        :param wid: 模型的wid
        :return: json
        """
        try:
            if not wid:
                wmodels: [WModel] = WModel.query.all()
                results = [
                    {
                        'wid': wmodel.wid,
                        'model_name': wmodel.model_name,
                        'model_type': wmodel.model_type,
                        'model_dataset': wmodel.model_dataset,
                    }
                    for wmodel in wmodels
                ]

            else:
                wmodel: WModel = WModel.query.get(wid)
                results = {
                    'wid': wmodel.wid,
                    'model_name': wmodel.model_name,
                    'model_type': wmodel.model_type,
                    'model_dataset': wmodel.model_dataset,
                }

            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据查询出现异常',
                'info': str(e)
            }

    def delete(self, wid):
        """
        删除操作
        :param rid: 结果id
        :return: json
        """
        try:
            if wid > 6:
                wmodel: WModel = WModel.query.get(wid)

                delete_path = weights_path + wmodel.model_name + '.pt'
                os.remove(delete_path)

                db.session.delete(wmodel)
                db.session.commit()

                return {
                    'status': 'success',
                    'message': '数据删除成功',
                }

            else:
                return {
                    'status': 'error',
                    'message': '不允许删除前六个模型',
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': '数据删除出现异常',
                'info': str(e)
            }

    def put(self, wid):
        """
        修改模型信息
        :param wid: 模型id
        :return: json
        """
        try:
            model: WModel = WModel.query.get(wid)
            model.model_name = request.json.get('model_name')
            model.model_type = request.json.get('model_type')
            model.model_dataset = request.json.get('model_dataset')

            db.session.commit()

            return {
                'status': 'success',
                'message': '数据修改成功'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据修改出现异常',
                'info': str(e)
            }

    def post(self):  # 添加数据
        """
        添加操作
        :return: json
        """
        try:
            model_name = request.json.get('model_name')
            model_type = request.json.get('model_type')
            model_dataset = request.json.get('model_dataset')

            wmodel: WModel = WModel()
            wmodel.model_name = model_name
            wmodel.model_type = model_type
            wmodel.model_dataset = model_dataset

            new_path = weights_path + model_name + '.pt'
            shutil.copy(src=cache_save_model_path, dst=new_path)

            db.session.add(wmodel)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据添加成功'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据添加出现异常',
                'info': str(e)
            }


class ResultApi(MethodView):
    """
    后端接口部分 RESTful API风格
    """

    def __init__(self):
        super(ResultApi, self).__init__()

    def get(self, rid):
        """
        查询数据
        :param rid: 结果rid
        :return: json
        """
        try:
            if not rid:
                n_results: [Result] = Result.query.all()
                results = [
                    {
                        'rid': result.rid,
                        'wid': result.wid,  # 首要默认为检测模型
                        'timestamp': result.timestamp,  # 时间戳
                        'type': result.type,  # 文件类型
                        'addition': result.addition,  # 额外说明
                        'mission_type': result.mission_type,  # 任务类型
                        'filename': result.filename,  # 被检测的源头文件
                        'num': result.num  # 一共有多少个检测物体
                    }
                    for result in n_results
                ]

            else:
                result: Result = Result.query.get(rid)
                results = {
                    'rid': result.rid,
                    'wid': result.wid,  # 同理
                    'timestamp': result.timestamp,
                    'type': result.type,
                    'addition': result.addition,
                    'mission_type': result.mission_type,
                    'filename': result.filename,
                    'num': result.num
                }

            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据查询出现异常',
                'info': str(e)
            }

    def delete(self, rid):
        """
        删除操作，前面是与 @app.route('/delete/result', methods=['DELETE']) 紧接着操作的，
        其对应的request.json格式是
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
        前端从@app.route('/delete/result', methods=['DELETE'])相应完了之后将json的rid传入此函数中
        :param rid: 结果id
        :return: json
        """
        try:
            result: Result = Result.query.get(rid)
            path = result_path + result.filename \
                   + '_' + str(result.timestamp) + '.' + result.type
            os.remove(path)

            db.session.delete(result)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据删除成功',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': '数据删除出现异常',
                'info': str(e)
            }

    def put(self, rid):
        try:
            result: Result = Result.query.get(rid)
            result.addition = request.json.get('addition')
            result.mission_type = request.json.get('mission_type')

            db.session.commit()

            return {
                'status': 'success',
                'message': '数据修改成功',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': '数据修改出现异常',
                'info': str(e)
            }



    def post(self):  # 添加数据
        """
        添加操作, json来自 @app.route('/detect', methods=['POST']) 那里
        example: {
          "message": "检测成功",
           传入的json为
               {
                  "addition": "单独的检测任务",
                  "attr": "jpg",
                  "filename": "b7a8e795-ff80fddf",
                  "mission_type": "detection",
                  "num": 21,
                  "timestamp": 1677250829,
                  "wid": 2
               }
        }

        :return: json
        """
        try:
            form = request.json
            # print(form)

            result = Result()
            result.wid = form.get('wid')
            result.num = form.get('num')
            result.type = form.get('type')
            result.timestamp = form.get('timestamp')
            result.addition = form.get('addition')
            result.mission_type = form.get('mission_type')
            result.filename = form.get('filename')

            db.session.add(result)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据添加成功'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据添加出现异常',
                'info': str(e)
            }


class ObjApi(MethodView):
    """
    后端接口部分 RESTful API风格
    """

    def __init__(self):
        super(ObjApi, self).__init__()

    def get(self, rid):
        """
        查询数据
        :param rid: 结果rid，外键查询
        :return: json
        """
        try:
            objects: [Object] = db.session.query(Object).filter(Object.rid == rid).all()  # 根据外键rid来查询
            results = [
                {
                    'oid': object.oid,
                    'rid': object.rid,
                    'cls': object.cls,
                    'x1': object.x1,
                    'y1': object.y1,
                    'x2': object.x2,
                    'y2': object.y2,
                    'conf': object.conf
                }
                for object in objects
            ]

            return {
                'status': 'success',
                'message': '数据查询成功',
                'length': len(results),
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据查询出现异常',
                'info': str(e)
            }

    def delete(self, rid):
        """
        删除操作，首先执行此函数，
        然后再执行@app.route('/delete/result', methods=['DELETE'])删除目标文件操作
        最后再将对应的result实例变量从数据库删除掉
        :param rid: 结果id
        :return: json
        """
        try:
            objects: [Object] = db.session.query(Object).filter(Object.rid == rid).all()  # 根据外键rid来查询
            for object in objects:
                db.session.delete(object)
            db.session.commit()

            return {
                'status': 'success',
                'message': '数据删除成功',
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据删除出现异常',
                'info': str(e)
            }

    def post(self):  # 添加数据
        """
        添加操作, json来自 @app.route('/detect', methods=['POST']) 那里
        example: {
          "message": "检测成功",
          "results": {
            "objects": [
                    .....
            ],
            "log": {
              "addition": "单独的检测任务",
              "attr": "jpg",
              "filename": "b7a8e795-ff80fddf",
              "mission_type": "detection",
              "num": 21,
              "timestamp": 1677250829,
              "wid": 2
              }
            },
          "status": "success"
        }

        :return: json
        """
        try:
            objects = request.json['results']["objects"]
            _about = request.json['results']['log']

            result: Result = db.session.query(Result).filter(Result.timestamp == _about["timestamp"]) \
                .filter(Result.filename == _about['filename']).first()

            for obj in objects:
                object = Object()

                object.rid = result.rid
                object.cls = obj['cls']
                object.x1 = obj['x1']
                object.y1 = obj['y1']
                object.x2 = obj['x2']
                object.y2 = obj['y2']
                object.conf = obj['conf']

                db.session.add(object)

            db.session.commit()

            return {
                'status': 'success',
                'message': '数据添加成功'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数据添加出现异常',
                'info': str(e)
            }


class PageApi(MethodView):  # 分页接口
    def __init__(self):
        super(PageApi, self).__init__()

    def get(self):
        try:
            # print(request.args)
            curPage = int(request.args.get('curPage'))
            pageSize = int(request.args.get('pageSize'))
            tableName = request.args.get('tableName')
            # print(curPage, pageSize, tableName)
            results = []
            if tableName == 'file':
                resultsIteam = File.query.order_by(File.fid.asc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items
                results = [
                    {
                        'fid': file.fid,
                        'name': file.name,
                        'timestamp': file.timestamp,
                        'type': file.type,
                        'origin': file.origin,
                        'width': file.width,
                        'height': file.height,
                        'img_url': img_url_show + str(file.name) + '.'
                                   + str(file.type)
                    }
                    for file in resultsIteam
                ]

            elif tableName == 'model':
                resultsIteam = WModel.query.order_by(WModel.wid.asc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items
                results = [
                    {
                        'wid': wmodel.wid,
                        'model_name': wmodel.model_name,
                        'model_type': wmodel.model_type,
                        'model_dataset': wmodel.model_dataset,
                    }
                    for wmodel in resultsIteam
                ]

            elif tableName == 'result':
                resultsIteam = Result.query.order_by(Result.rid.asc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items
                results = [
                    {
                        'rid': result.rid,
                        'wid': result.wid,
                        'timestamp': result.timestamp,
                        'type': result.type,
                        'addition': result.addition,
                        'mission_type': result.mission_type,
                        'filename': result.filename,
                        'num': result.num,
                        'img_url': result_url_show + str(result.filename) + '_' + str(result.timestamp) + '.'
                                   + str(result.type)
                    }
                    for result in resultsIteam
                ]

            else:
                pass

            return {
                'status': 'success',
                'message': '分页查找成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '分页查找出现异常',
                'info': str(e)
            }


class ObjectPageApi(MethodView):
    def __init__(self):
        super(ObjectPageApi, self).__init__()

    def get(self, rid):
        """
        :param rid:
        Object检测子结果的分页实现
        :return:
        """
        try:
            curPage = int(request.args.get('curPage'))
            pageSize = int(request.args.get('pageSize'))
            # print(curPage, pageSize)
            resultsItem = Object.query \
                .filter(Object.rid == rid).order_by(Object.conf.desc()).paginate(
                page=curPage, per_page=pageSize, error_out=True
            ).items
            # print(resultsItem)
            results = [
                {
                    'oid': object.oid,
                    'rid': object.rid,
                    'cls': object.cls,
                    'x1': object.x1,
                    'y1': object.y1,
                    'x2': object.x2,
                    'y2': object.y2,
                    'conf': object.conf
                } for object in resultsItem
            ]

            return {
                'status': 'success',
                'message': '分页查找成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '分页查找出现异常',
                'info': str(e)
            }


class NumApi(MethodView):  # 分页显示数目的接口
    def __init__(self):
        super(NumApi, self).__init__()
        self.config = ['file', 'model', 'result']

    def get(self):
        """
        :param tableName:
        :return: 总数数字
        """
        try:
            results = 0
            # print(results)
            # curPage = request.args.get('curPage')
            # pageSize = request.args.get('pageSize')
            # print(request.args)
            tableName = request.args.get('tableName')
            rid = int(request.args.get('rid'))

            if tableName in self.config:
                if tableName == 'file':
                    results = File.query.count()
                elif tableName == 'model':
                    results = WModel.query.count()
                else:
                    results = Result.query.count()
            else:
                if rid > 0:
                    results = Object.query.filter(Object.rid == rid).count()

            return {
                'status': 'success',
                'message': '数量查找成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数量查找出现异常',
                'info': str(e)
            }


class DeblurSearchApi(MethodView):  # 分页实现模糊查找的接口
    def __init__(self):
        super(DeblurSearchApi, self).__init__()

    def get(self):
        try:
            results = []
            tableName = request.args.get('tableName')
            keyword = request.args.get('keyword')
            curPage = int(request.args.get('curPage'))
            pageSize = int(request.args.get('pageSize'))
            # print(tableName, keyword, curPage, pageSize)
            if tableName == 'file':
                resultsIteam = File.query.filter(File.name.like('%' + keyword + '%')) \
                    .order_by(File.fid.desc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items
                # print(len(resultsIteam))
                results = [
                    {
                        'fid': file.fid,
                        'name': file.name,
                        'timestamp': file.timestamp,
                        'type': file.type,
                        'origin': file.origin,
                        'width': file.width,
                        'height': file.height,
                        'img_url': img_url_show + str(file.name) + '.'
                                   + str(file.type)
                    }
                    for file in resultsIteam
                ]

            elif tableName == 'model':
                resultsIteam = WModel.query.filter(WModel.model_name.like('%' + keyword + '%')) \
                    .order_by(WModel.wid.asc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items
                results = [
                    {
                        'wid': wmodel.wid,
                        'model_name': wmodel.model_name,
                        'model_type': wmodel.model_type,
                        'model_dataset': wmodel.model_dataset,
                    }
                    for wmodel in resultsIteam
                ]

            elif tableName == 'result':
                resultsIteam = Result.query.filter(Result.filename.like('%' + keyword + '%')) \
                    .order_by(Result.rid.desc()).paginate(
                    page=curPage, per_page=pageSize, error_out=True
                ).items

                results = [
                    {
                        'rid': result.rid,
                        'wid': result.wid,
                        'timestamp': result.timestamp,
                        'type': result.type,
                        'addition': result.addition,
                        'mission_type': result.mission_type,
                        'filename': result.filename,
                        'num': result.num,
                        'img_url': result_url_show + str(result.filename) + '_' +
                                   str(result.timestamp) + '.' + str(result.type)
                    }
                    for result in resultsIteam
                ]

            else:
                pass

            return {
                'status': 'success',
                'message': '模糊查找成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '模糊查找出现异常',
                'info': str(e)
            }


class DeblurSearchNumApi(MethodView):
    def __init__(self):
        super(DeblurSearchNumApi, self).__init__()
        self.config = ['file', 'model', 'result']

    def get(self):
        try:
            tableName = request.args.get('tableName')
            # rid = int(request.args.get('rid'))
            keyword = request.args.get('keyword')
            results = 0

            if tableName in self.config:
                if tableName == 'file':
                    results = File.query.filter(File.name
                                                .like('%' + keyword + '%')).count()
                elif tableName == 'model':
                    results = WModel.query.filter(WModel.model_name
                                                  .like('%' + keyword + '%')).count()
                else:
                    results = Result.query.filter(Result.filename
                                                  .like('%' + keyword + '%')).count()
            else:
                pass

            return {
                'status': 'success',
                'message': '数量关键词模糊查找成功',
                'results': results
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': '数量关键词模糊查找出现异常',
                'info': str(e)
            }
