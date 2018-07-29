from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


# 调用上下文管理器实现重复功能
class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollbck()
            raise e


db = SQLAlchemy()


# 对于几乎所有的类中都会有的方法，可以在基类中定义，以减少代码量
class Base(db.Model):
    __abstract__ = True
    create_time = db.Column('create_time', db.Integer)
    status = db.Column(db.SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def delete(self):
        self.status = 0
