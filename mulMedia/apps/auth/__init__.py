from flask import Blueprint

auth = Blueprint('auth',__name__)

#
# # 第二步，产生UploadSet类对象的实例，用来管理上传集合
# photoSet = UploadSet('photos', IMAGES)
# # 第三步，绑定app 与UploadSet对象实例
# configure_uploads(app, (photoSet,))

from apps.auth import views