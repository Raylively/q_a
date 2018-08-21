import os
from os import path

from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_login import LoginManager

from flask_pagedown import PageDown
from flask_gravatar import Gravatar # 图像管理
from flask_uploads import UploadSet, IMAGES, configure_uploads

from werkzeug.routing import BaseConverter
from apps import config, app


# 自定义的正则路由匹配


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


basedir = path.abspath(path.dirname(__file__))
bootstrap = Bootstrap()
pagedown = PageDown()
# nav = Nav()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_views = 'auth.login'  # 默认登录页


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.from_object(config)

# app.register_blueprint(main_blueprint,static_folder='static',templates_folder='templates')
APPS_DIR = os.path.dirname(__file__)  # 当前工作空间的地址
STATIC_DIR = os.path.join(APPS_DIR, 'static')  # 静态文件的地址

app.config['UPLOADED_RELATIVE'] = 'uploads'  # 上传文件的目标文件夹
app.config['UPLOADED_FOLDER'] = os.path.join(STATIC_DIR, app.config['UPLOADED_RELATIVE'])

# 第一步：配置上传文件保存地址
app.config['UPLOADED_PHOTOS_DEST'] = app.config['UPLOADED_FOLDER']
# app.config['UPLOADED_MUSICS_DEST'] = app.config['UPLOADED_FOLDER']
# 创建文件夹
from apps.utils import create_folder
create_folder(app.config['UPLOADED_FOLDER'])




# manager = Manager(app)
# nav.register_element('top', Navbar('flask入门',
#                                    View('主页', 'home'),
#                                    View('关于', 'about'),
#                                    View('服务', 'services'),
#                                    View('项目', 'projects')))

db.init_app(app)
bootstrap.init_app(app)
# nav.init_app(app)
login_manager.init_app(app)
pagedown.init_app(app)

Gravatar(app,size=64) # 默认图像大小

# 注册蓝图
from apps.auth import auth as auth_blueprint
from apps.main import main as main_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth/')
app.register_blueprint(main_blueprint)













# def create_app():
#     app = import_app()
#     app.url_map.converters['regex'] = RegexConverter
#     app.config.from_object(config)
#
#     # app.register_blueprint(main_blueprint,static_folder='static',templates_folder='templates')
#     APPS_DIR = os.path.dirname(__file__)  # 当前工作空间的地址
#     STATIC_DIR = os.path.join(APPS_DIR, 'static')  # 静态文件的地址
#
#     app.config['UPLOADED_RELATIVE'] = 'uploads'  # 上传文件的目标文件夹
#     app.config['UPLOADED_FOLDER'] = os.path.join(STATIC_DIR, app.config['UPLOADED_RELATIVE'])
#
#     # 第一步：配置上传文件保存地址
#     app.config['UPLOADED_PHOTOS_DEST'] = app.config['UPLOADED_FOLDER']
#     # app.config['UPLOADED_MUSICS_DEST'] = app.config['UPLOADED_FOLDER']
#     # 创建文件夹
#     from apps.utils import create_folder
#     create_folder(app.config['UPLOADED_FOLDER'])
#
#     # 第二步，产生UploadSet类对象的实例，用来管理上传集合
#     # from apps import import_app
#
#     photoSet = UploadSet('photos', IMAGES)
#     # 第三步，绑定app 与UploadSet对象实例
#     configure_uploads(app, (photoSet,))
#
#     # # 第二步，产生UploadSet类对象的实例，用来管理上传集合
#     # photoSet = UploadSet('photos', IMAGES)
#     # # 第三步，绑定app 与UploadSet对象实例
#     # configure_uploads(app, photoSet)
#
#
#     # manager = Manager(app)
#     # nav.register_element('top', Navbar('flask入门',
#     #                                    View('主页', 'home'),
#     #                                    View('关于', 'about'),
#     #                                    View('服务', 'services'),
#     #                                    View('项目', 'projects')))
#
#     db.init_app(app)
#     bootstrap.init_app(app)
#     # nav.init_app(app)
#     login_manager.init_app(app)
#     pagedown.init_app(app)
#
#     Gravatar(app,size=64) # 默认图像大小
#
#     # 注册蓝图
#     from apps.auth import auth as auth_blueprint
#     from apps.main import main as main_blueprint
#     app.register_blueprint(auth_blueprint, url_prefix='/auth/')
#     app.register_blueprint(main_blueprint)
#
#
#     return app

