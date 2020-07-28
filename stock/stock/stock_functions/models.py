# -*- coding = utf-8 -*-


from stock import db

# 创建表结构
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

    # 定义返回的类型
    def __repr__(self):
        return "<User:%r>" % self.username


# 将创建好的实体类映射回数据库
db.create_all()
