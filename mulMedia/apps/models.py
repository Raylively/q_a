# import datetime.datetime
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db, login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    pwd = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(50),default=None,unique=True)
    phone = db.Column(db.String(11),nullable=True,default=None)
    introduce = db.Column(db.TEXT,default=None)
    birthday = db.Column(db.Date,default=None)
    photo = db.Column(db.String(50),default=None)
    addtime = db.Column(db.DATETIME,index=True,default=datetime.now)

    albums = db.relationship('Album',backref='user')
    album_favors = db.relationship('AlbumFavor',backref='user')

    def __repr__(self):
        return '<User %r>'%self.name

    # 密码加密
    def __init__(self,*args,**kwargs):
        name = kwargs.get('name')
        pwd = kwargs.get('pwd')
        email = kwargs.get('email')
        birthday = kwargs.get('birthday')
        photo = kwargs.get('photo')



        self.name = name
        # self.pwd = generate_password_hash(pwd)
        self.pwd = pwd
        self.email = email
        self.birthday = birthday
        self.photo = photo


    # @property
    # def password(self):
    #     return self.pwd
    #
    # @password.setter
    # def password(self,pwd):
    #     self.pwd = generate_password_hash(pwd)



    # def check_password(self,pwd):
    #     return check_password_hash(self.pwd,pwd)
    #
    #     # Flask-Login integration
    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):  # line 37
    #     return True
    #
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     return self.id
    #
    #     # Required for administrative interface
    #
    # def __unicode__(self):
    #     return self.name
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AlbumTag(db.Model):
    __tablename__ = 'album_tag'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False,unique=True)

    albums = db.relationship('Album',backref='album_tag')

    def __repr__(self):
        return '<AlbumTag %r>'%self.name



class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.TEXT,default=None)
    conver = db.Column(db.String(255),default=0)
    photonum = db.Column(db.Integer,default=0)
    privacy = db.Column(db.String(20),default='public')
    clicknum = db.Column(db.Integer,default=0)
    favornum = db.Column(db.Integer,default=0)
    uuid = db.Column(db.String(255),unique=True,nullable=False)
    addtime = db.Column(db.DATETIME,index=True,default=datetime.now)

    tag_id = db.Column(db.Integer,db.ForeignKey('album_tag.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    album_favors = db.relationship('AlbumFavor',backref='album')
    photos = db.relationship('Photo',backref='album')

    def __repr__(self):
        return '<Album %r>'%self.title


class AlbumFavor(db.Model):
    __tablename__ = 'album_favor'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer,db.ForeignKey('album.id'))

    addtime=db.Column(db.DATETIME,index=True,default=datetime.now)



class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name_org = db.Column(db.String(255),unique=True,nullable=False) # 原图文件名
    name_show = db.Column(db.String(255),unique=True,nullable=False) # 展示图文件名
    name_thumb = db.Column(db.String(255),unique=True,nullable=False) # 缩略图文件名

    album_id = db.Column(db.Integer,db.ForeignKey('album.id'))
    addtime=db.Column(db.DATETIME,index=True,default=datetime.now)



