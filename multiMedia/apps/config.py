import os

import pymysql
pymysql.install_as_MySQLdb()


SECRET_KEY = os.urandom(24)

DEBUG = True

# 数据库配置信息  #alter database DBname character set utf8
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'Flask'

# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
SQLALCHEMY_DATABASE_URI= '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭警告信息