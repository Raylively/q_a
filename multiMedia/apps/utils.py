import datetime
import os
import uuid
from functools import wraps

from flask import session, flash, url_for, redirect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename


# 第二步，产生UploadSet类对象的实例，用来管理上传集合
from apps import app

# 第二步，产生UploadSet类对象的实例，用来管理上传集合
photoSet = UploadSet('photos', IMAGES)
# 第三步，绑定app 与UploadSet对象实例
configure_uploads(app, (photoSet,))

# 创建文件
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # os.chmod(folder_path,os.O_RDWR)

def login_needed(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            flash('请登录!','danger')
            return redirect(url_for('auth.login'))
    return wrapper

#修改文件名称
def change_filename_with_timestamp_uuid(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S")+\
        str(uuid.uuid4().hex()) + fileinfo[-1]
    return filename

#确保文件名安全性并添加时间戳
def secure_filestorage_with_timestamp(filename):
    fileinfo = os.path.splitext(filename)
    filename_prefix = secure_filename(fileinfo[0]+"_")
    filename = filename_prefix + datetime.now().strftime("%Y%m%d%H%M%S")+\
        fileinfo[-1].lower()
    return filename

#确保文件名安全性并添加时间戳
def secure_filename_with_timestamp(filename):
    filename = secure_filename(filename)
    fileinfo = os.path.splitext(filename)
    filename = fileinfo[0] + '_' + datetime.now().strftime("%Y%m%d%H%M%S")+\
        fileinfo[-1].lower()
    return filename

#确保文件名安全性并添加随机uuid
def secure_filename_with_uuid(filename):
    fileinfo = os.path.splitext(filename)
    filename_prefix = secure_filename(fileinfo[0]+'_')
    filename = filename_prefix + str(uuid.uuid4().hex)[0:6]+\
        fileinfo[-1].lower()
    return filename

ALLOWED_IMAGE_EXTENSION = set(['png','jpg','gif','jpeg','bmp'])
ALLOWED_VIDEO_EXTENSION = set(['MP4','AVI'])
ALLOWED_AUDIO_EXTENSION = set(['MP3','M4A'])

# 检查上传控件上传的文件后缀名是否符合要求
def check_files_extension(filenamelist,allowd_extensions):
    for fname in filenamelist:
        check_state = '.' in fname and \
            fname.rsplit('.',1)[1].lower() in allowd_extensions
        if not check_state:
            return False
    return True

# 检查上传控件上传的文件后缀名是否符合要求
def check_filestorage_extension(filestoragelist,allowd_extensions):
    valid_fs = []   # 有效文件列表
    for fs in filestoragelist:
        check_state = '.' in fs.filename and \
            fs.filename.rsplit('.',1)[1].lower() in allowd_extensions
        if check_state:
            valid_fs.append(fs)
    return valid_fs

import PIL
from PIL import Image

def create_thumbnail(path,filename,base_width=300):

    img_name,ext = os.path.splitext(filename)
    new_filename = img_name+'_thumb'+ext #缩略图文件名
    img = Image.open(os.path.join(path,filename)) # 根据指定的路径打开文件
    # 如果图片宽度大于base_path,将其缩放到basewidth,并保持原图宽高比
    if img.size[0]>=base_width:
        w_percent = (base_width/float(img.size[0]))
        h_size = int((float(img.size[1])*float(w_percent)))
        img = img.resize((base_width,h_size),Image.ANTIALIAS)
        img.save(os.path.join(path,new_filename))
        return new_filename
    img.save(os.path.join(path,new_filename))
    return new_filename

def create_show(path,filename,base_width=800):

    img_name,ext = os.path.splitext(filename)
    new_filename = img_name+'_show'+ext #展示图文件名
    img = Image.open(os.path.join(path,filename)) # 根据指定的路径打开文件
    # 如果图片宽度大于base_path,将其缩放到basewidth,并保持原图宽高比
    if img.size[0]<=base_width:
        w_percent = (base_width/float(img.size[0]))
        h_size = int((float(img.size[1])*float(w_percent)))
        img = img.resize((base_width,h_size),Image.ANTIALIAS)
        img.save(os.path.join(path,new_filename))
        return new_filename
    img.save(os.path.join(path,new_filename))
    return new_filename

