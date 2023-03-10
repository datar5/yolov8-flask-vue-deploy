import os

from sqlalchemy import ForeignKey
from config import cache_save_path
from PIL import Image

from extension import db
import datetime

fixed_model_type = [
    'yolov5', 'yolov8'
]


class File(db.Model):
    __tablename__ = 'file_table'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    type = db.Column(db.String(255), nullable=False)  # 文件类型
    origin = db.Column(db.String(255), nullable=False)  # 来源
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    @staticmethod
    def init_db():
        count: int = 1
        files = os.listdir(cache_save_path)

        # rets = [
        #     (1, 'b6f77fda-02b6e75b', 'jpg', 'localhost://b6f77fda-02b6e75b.jpg', 1280, 720),
        #     (2, 'b7a8e795-ff80fddf', 'jpg', 'localhost://b7a8e795-ff80fddf.jpg', 1280, 720),
        # ]

        rets = []
        for filename in files:
            filename = cache_save_path + filename
            # print(filename)
            img = Image.open(filename)
            rets.append([
                count, filename.split('\\')[-1].split('.')[0], filename.split('.')[-1],
                'localhost://' + filename.split('\\')[-1], img.width, img.height
            ])
            count += 1
        # print(rets)

        for ret in rets:
            file = File()
            file.fid = ret[0]
            file.name = ret[1]
            file.type = ret[2]
            file.origin = ret[3]
            file.width = ret[4]
            file.height = ret[5]
            db.session.add(file)
        #
        db.session.commit()


class WModel(db.Model):
    __tablename__ = 'model_table'
    wid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)  # 名称
    model_type = db.Column(db.String(255), nullable=False)  # 类型
    model_dataset = db.Column(db.String(255), nullable=False)  # 适用数据集

    @staticmethod
    def init_db():
        rets = [
            (1, 'yolov8l_coco', 'yolov8', 'coco'),
            (2, 'yolov8m_coco', 'yolov8', 'coco'),
            (3, 'yolov8s_coco', 'yolov8', 'coco'),
            (4, 'yolov8n_coco', 'yolov8', 'coco'),
            (5, 'yolov5su_coco', 'yolov5', 'coco'),
            (6, 'yolov5nu_coco', 'yolov5', 'coco')
        ]

        for ret in rets:
            wmodel = WModel()
            wmodel.wid = ret[0]
            wmodel.model_name = ret[1]
            wmodel.model_type = ret[2]
            wmodel.model_dataset = ret[3]
            db.session.add(wmodel)

        db.session.commit()


class Result(db.Model):
    __tablename__ = 'result_table'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wid = db.Column(db.Integer, ForeignKey("model_table.wid", ondelete='SET NULL'))  # 首要默认为检测模型
    timestamp = db.Column(db.Integer, nullable=False)  # 时间戳
    type = db.Column(db.String(255), nullable=True)  # 文件类型
    addition = db.Column(db.String(255), nullable=True)  # 额外说明
    mission_type = db.Column(db.String(255), nullable=False)  # 任务类型
    filename = db.Column(db.String(255), nullable=False)  # 被检测的源头文件
    num = db.Column(db.Integer, nullable=False)  # 一共有多少个检测物体


class Object(db.Model):
    __tablename__ = 'obj_table'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer, ForeignKey("result_table.rid", ondelete='SET NULL'))  # 和检测完成好的文件相关联, 外键
    cls = db.Column(db.String(255), nullable=False)  # 类别名称
    x1 = db.Column(db.Float, nullable=False)  # 边框的坐标值
    y1 = db.Column(db.Float, nullable=False)
    x2 = db.Column(db.Float, nullable=False)
    y2 = db.Column(db.Float, nullable=False)
    conf = db.Column(db.Float, nullable=False)  # 置信度
