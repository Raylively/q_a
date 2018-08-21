import os
import shutil
from random import randint

from flask import flash, redirect, url_for, render_template, request, session, make_response, g
from flask_login import login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps import  db
from apps.auth.forms import RegisterForm, LoginForm, PwdForm, DatailForm
from apps.models import User, Album
from apps.utils import check_files_extension, create_folder, login_needed, ALLOWED_IMAGE_EXTENSION, photoSet
from manage import app
from . import auth




@auth.route('/')
def index():
    return render_template('auth.index.html')

@auth.route('/register/',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # 检查用户上传的图像文件是否符合要求
        if not check_files_extension([form.photo.data.filename],ALLOWED_IMAGE_EXTENSION):
            flash('图片格式不正确!', 'danger')
            return redirect(url_for('auth.register'), form=form)

        user_name_db = User.query.filter(User.name==form.user_name.data).first()
        if user_name_db:
            flash('用户名已经存在!','danger')
            return render_template('register.html', form=form)
        user_email_db = User.query.filter(User.email==form.email.data).first()
        if user_email_db:
            flash('邮箱已经被注册过!','danger')
            return render_template('register.html', form=form)
        user_phone_db = User.query.filter(User.phone==form.phone.data).first()
        if user_phone_db:
            flash('手机号已经被注册过!','danger')
            return render_template('register.html', form=form)

        user = User()
        user.name = form.user_name.data
        user.pwd = generate_password_hash(form.user_pwd.data)
        user.email = form.email.data
        user.phone = form.phone.data
        user.introduce = form.introduce.data
        user.birthday = form.birthday.data
        # 文件上传
        # img_file = request.files['photo']
        img_file = request.files.get('photo')
        user.photo = secure_filename(img_file.filename)

        flash('注册成功','success')
        db.session.add(user)
        db.session.commit()
        # file_path = file_bastpath + img_file.filename
        user_folder = os.path.join(app.config['UPLOADED_FOLDER'],user.name)
        create_folder(user_folder)
        img_file.save(os.path.join(user_folder, user.photo))

        return redirect(url_for('auth.login',user_name=user.name))
    # user_name = form.data['user_name']
    return render_template('register.html', form=form)

@auth.route('/login/',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.user_name.data
        pwd = form.user_pwd.data

        user = User.query.filter(User.name==name).first()
        # if user and user.check_password(pwd):
        if user and check_password_hash(user.pwd,pwd):
            login_user(user)  # 将登陆信息保存
            flash('登录成功!','success')
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误','danger')
            render_template('login.html', form=form)

    return render_template('login.html', form=form)

@auth.route('/logout/',methods=['POST','GET'])
def logout():
    session.clear()  #session.pop()
    flash('你已经成功退出','success')
    logout_user()  # 将登陆信息保存
    return redirect(url_for('auth.login'))


@auth.route('/user_center/',methods=['POST','GET'])
@login_needed
def user_center():
    return render_template('user_center.html')


@auth.route('/user_detail/',methods=['POST','GET'])
@login_needed
def user_detail():
    user_info = User.query.filter(User.id==session.get('user_id')).first()
    return render_template('user_detail.html', user=user_info)

@auth.route('/change_pwd/',methods=['POST','GET'])
@login_needed
def change_pwd():
    form = PwdForm()
    user = User.query.filter(User.id == session.get('user_id')).first()
    if form.validate_on_submit():
        old_pwd = check_password_hash(user.pwd,form.old_pwd.data)
        new_pwd = generate_password_hash(form.new_pwd.data)
        if not old_pwd:
            flash('旧密码输入有误','danger')
            return render_template('change_pwd.html', form=form)
        user.pwd = new_pwd
        # old_pwd = form.old_pwd.data
        # if old_pwd == user.pwd:
        #     user.pwd = form.new_pwd.data
        db.session.add(user)
        db.session.commit()
        flash('密码修改成功！','success')
        return redirect(url_for('auth.user_center'))
        flash('旧密码输入错误','danger')
    return render_template('change_pwd.html', form=form)


@auth.route('/change_info/',methods=['POST','GET'])
def change_info():
    form = DatailForm()
    user = User.query.filter(User.id == session.get('user_id')).first()
    old_name = user.name
    old_file = user.photo
    if form.validate_on_submit():
        user.email = form.email.data
        user.phone = form.phone.data
        user.introduce = form.introduce.data
        user.birthday = form.birthday.data
        # img_file = request.files['photo']
        img_file = request.files.get('photo')
        print(img_file)
        if img_file != None:
            # if user.photo != '':
            user.photo = secure_filename(img_file.filename)

            # if not check_files_extension([form.photo.data.filename], ALLOWED_IMAGE_EXTENSION):
            if not check_files_extension([img_file.filename], ALLOWED_IMAGE_EXTENSION):
                flash('图片格式不正确!', 'danger')
                return redirect(url_for('auth.change_info', form=form))
            user_folder = os.path.join(app.config['UPLOADED_FOLDER'],old_name)
            os.remove(path=os.path.join(user_folder,old_file))
            user.photo = secure_filename(img_file.filename)
            img_file.save(os.path.join(user_folder,user.photo))
        if old_name != user.name:
            new_name = form.user_name.data
            user_db = User.query.filter(User.name == new_name).first()
            if user_db:
                flash('用户名已经存在!', 'danger')
                return redirect(url_for('auth.change_info', form=form))
            os.rename(os.path.join(app.config['UPLOADED_FOLDER'], old_name),
                      os.path.join(app.config['UPLOADED_FOLDER'], user.name))
        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('auth.user_center'))
    return render_template('change_info.html', user=user, form=form)

@auth.route('/cancel_id/',methods=['POST','GET'])
@login_needed
def cancel_id():
    print(request.method)
    if request.method == 'POST':
        user = User.query.filter(User.id==session.get('user_id')).first()
        # if user and form.validate_on_submit():
        del_path = os.path.join(app.config['UPLOADED_FOLDER'],
                                user.name)
        shutil.rmtree(del_path,ignore_errors=True)
        # save 方法获取文件路径并删除
        # fpath = photoSet.path(filename='')
        # os.remove(fpath)
        db.session.delete(user)
        db.session.commit()
        flash('注销成功','success')
        return redirect(url_for('auth.register'))
    return render_template('cancel_id.html')

@auth.route('/my_photos/',methods=['POST','GET'])
def my_photos():
    my_albums = Album.query.filter_by(user_id=current_user.id).all()
    # 获取相册封面
    for my_album in my_albums:
        my_album.cover = my_album.photos[randint(0,len(my_album.photos)-1)].name_thumb
        folder = my_album.user.name + '/' + my_album.title
        cover_url = photoSet.url(filename=folder+'/'+my_album.cover)
        my_album.cover_img = cover_url

        user_photo = my_album.user.photo
        folder = my_album.user.name + '/'
        user_photo_url = photoSet.url(filename=folder+user_photo)
    #     #取出该相册下面的所有图片
    #     for photo in my_album.photos:
    #         photo_folder = my_album.user.name + '/' + my_album.title + '/'
    #         photo.url = photoSet.url(filename=photo_folder+photo.name_show)
    return render_template('my_photos.html',my_albums=my_albums,
                           user_photo_url=user_photo_url,)

@auth.route('/collection_photos/',methods=['POST','GET'])
@login_needed
def collection_photos():
    # 收藏列表
    favor_albums = []
    # print(current_user.id,current_user.name)
    if session.get('user_id'):
        # user = User.query.get_or_404(int(session.get('user_id')))
        # favor = current_user.album_favors
        # favors = user.album_favors
        for favor in current_user.album_favors:
            favor_albums.append(favor.album)
        for f_album in favor_albums:
            f_album.cover = f_album.photos[randint(0, len(f_album.photos) - 1)].name_thumb
            folder = f_album.user.name + '/' + f_album.title
            cover_url = photoSet.url(filename=folder + '/' + f_album.cover)
            f_album.cover_img = cover_url

            user_photo = f_album.user.photo
            folder = f_album.user.name + '/'
            user_photo_url = photoSet.url(filename=folder + user_photo)
            # 取出该相册下面的所有图片
            # for photo in my_album.photos:
            #     photo_folder = my_album.user.name + '/' + my_album.title + '/'
            #     photo.url = photoSet.url(filename=photo_folder + photo.name_show)
    return render_template('collection_photos.html',favor_albums=favor_albums)

@auth.errorhandler(404)
def page_bot_found(error):
    # return render_template('404.html'),404
    resp = make_response(render_template('404.html'), 404)
    resp.headers['X-Something'] = 'hahahaha'

# 每次请求都会先执行此函数
@auth.before_request
def my_before_request():
    user_id = session.get('user_id')
    # user_id = session.get('user_id')
    # flash(user_id,'danger')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user      # g 对象
# 上下管理器，定义的变量在模板中通用，返回值必须是字典类型－－－－钩子函数的一种
@auth.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}


