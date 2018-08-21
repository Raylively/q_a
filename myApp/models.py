
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# alter  database webApp CHARACTER SET utf8;
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(100),nullable=False)


    # 密码加密
    def __init__(self,*args,**kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.username = username
        self.password = generate_password_hash(password)


    def check_password(self,password):
        result = check_password_hash(self.password,password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # now()　获取的是服务器第一次运行的时间
    # now就是每次创建一个模型时，获取当前的时间
    create_date = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('question'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship('Question',backref=db.backref('answer',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('answer'))


