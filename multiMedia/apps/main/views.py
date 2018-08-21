import uuid
from random import randint

from flask import render_template, request, flash, redirect, url_for, session, make_response, g
from flask_login import login_required, current_user
from sqlalchemy import or_


from apps import db
from apps.main.forms import AlbumInfoForm, AlbumUploadForm
from apps.models import User, Album, Photo, AlbumTag, AlbumFavor
from apps.utils import ALLOWED_IMAGE_EXTENSION, \
    check_filestorage_extension, secure_filename_with_uuid, create_thumbnail, photoSet, login_needed

from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('main.404.html'),404

@main.route('/album/')
def album_index():
    return render_template('album_index.html')

@main.route('/album/create/',methods=['POST','GET'])
@login_needed
def album_create():
    flash('创建相册：','danger')
    form = AlbumInfoForm()
    # 取出数据库中的全部数据
    form.album_tag.choices = [(tag.id, tag.name) for tag in AlbumTag.query.all()]
    if request.method == 'POST' and form.validate_on_submit():
        album_title = form.album_title.data
        # 确认用户相册是否已经存在
        existd = Album.query.filter(Album.user_id==session.get('user_id'),
                                    Album.title==album_title).count()
        if existd>0:
            flash('相册已经存在','danger')
            return render_template('album_create.html',form=form)
        album_uuid = str(uuid.uuid4().hex[0:10])
        if Album.query.filter_by(uuid=album_uuid).count()>0:
            # existed_count = Album.query.filter_by(title=album_title).count()
            # if existed_count > 0:
            flash('相册uuid已经存在，请重新输入','danger')
            return render_template('album_create.html',form=form)
        album_desc = form.album_desc.data
        album_privacy = form.album_privacy.data
        album_tag = form.album_tag.data
        album = Album(title=album_title,desc=album_desc,
                      privacy=album_privacy,tag_id=album_tag,
                      user_id=int(session.get('user_id')),
                      uuid=album_uuid)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for('main.album_upload'))
    return render_template('album_create.html',form=form)

@main.route('/album/upload/',methods=['POST','GET'])
@login_needed
def album_upload():
    print(current_user)
    form = AlbumUploadForm()
    # 根据user_id筛选出相册
    items = Album.query.filter_by(user_id=session.get('user_id'))
    form.album_title.choices = [(item.id, item.title) for item in items]
    if len(form.album_title.choices)<1:
        flash('请先创建相册，再上传图片','danger')
        return redirect(url_for('main.album_create'))
    print('album_upload:',request.method)
    if request.method == 'POST':
        # 同伙getlist方法获取FileStorage文件列表
        fs = request.files.getlist('main.album_upload')
        # 检查文件扩展名，将合格的文件过滤出来
        valid_fs = check_filestorage_extension(fs,allowd_extensions=ALLOWED_IMAGE_EXTENSION)
        if len(valid_fs)<1:
            flash('只允许上传类型为：'+str(ALLOWED_IMAGE_EXTENSION),'danger')
            return redirect(url_for('main.album_upload'))
        else:
            # 开始遍历保存文件
            files_url = []
            album_cover = ''
            for fs in valid_fs:
                print('fs:',fs)
                # 第四步，使用UploadSet的save方法保存文件
                name_org = secure_filename_with_uuid(fs.filename)
                for id,title in form.album_title.choices:
                    if id == form.album_title.data:
                        album_title = title
                folder = current_user.name+'/'+album_title
                fname = photoSet.save(storage=fs,folder=folder,name=name_org)
                ts_path = photoSet.config.destination + '/' + folder
                #创建并保存缩略图
                name_thumb = create_thumbnail(path=ts_path,filename=name_org,base_width=100)
                #创建并保存展示图
                name_show = create_thumbnail(path=ts_path,filename=name_org,base_width=800)
                # 把产生的photo对象保存到数据库中
                photo = Photo(name_org=name_org,name_show=name_show,name_thumb=name_thumb,
                              album_id=form.album_title.data)
                db.session.add(photo)
                db.session.commit()
                #获取刚才保存的缩略图文件的url
                fs_url = photoSet.url(folder+'/'+name_thumb)
                # # 第五步，使用UploadSet的url方法获得文件的url
                # fs_url = photoSet.url(filename=fname)
                files_url.append(fs_url)
                # 设置封面文件
                photo.album_cover = photo.name_thumb
                print('fs_url:',fs_url)
            album = Album.query.filter_by(id=form.album_title.data).first()
            album.photonum += len(valid_fs)
            album.cover = album_cover
            db.session.add(album)
            db.session.commit()
            flash('成功保存了%s张图片'%str(len(valid_fs)),'success')
            flash('当前相册共有%s张图片'%str(album.photonum),'success')
            return render_template('album_upload.html',files_url=files_url,form=form)
    return render_template('album_upload.html',form=form)

@main.route('/album/list/<int:page>',methods=['GET'])
def album_list(page):
    albumtags = AlbumTag.query.all()
    tagid = request.args.get('tag','all')
    if tagid=='all':
        albums = Album.query.filter(Album.privacy != 'private'). \
            order_by(Album.addtime.desc()).paginate(page=page,per_page=3)
    else:
        albums = Album.query.filter(Album.privacy != 'private',Album.tag_id == int(tagid)). \
            order_by(Album.addtime.desc()).paginate(page=page,per_page=3)

    for album in albums.items:  # items属性可迭代
        # cover = album.photos[0].name_thumb
        cover = album.photos[randint(0,len(album.photos)-1)].name_thumb
        folder = album.user.name + '/' + album.title
        cover_url = photoSet.url(filename=folder+'/'+cover)
        album.cover_img = cover_url
    return render_template('album_list.html',
                           albumtags=albumtags,
                           albums=albums)

@main.route('/album/browse/<int:id>',methods=['GET'])
def album_browse(id):
    # 取出相册的基本信息
    album = Album.query.get_or_404(int(id))
    # 增加对应相册的浏览量
    album.clicknum += 1
    db.session.add(album)
    db.session.commit()

    # 收藏列表
    favor_albums = []
    # print(current_user.id,current_user.name)
    if session.get('user_id'):
        for favor in current_user.album_favors:
            favor_albums.append(favor.album)
        for f_album in favor_albums:
            f_album.cover = f_album.photos[randint(0, len(f_album.photos) - 1)].name_thumb
            folder = f_album.user.name + '/' + f_album.title
            cover_url = photoSet.url(filename=folder + '/' + f_album.cover)
            f_album.cover_img = cover_url

    # 取出作者图像的url
    user_photo = album.user.photo
    folder = album.user.name + '/'
    user_photo_url = photoSet.url(filename=folder+user_photo)
    # 查询推荐相册
    recommend_album = Album.query.filter(Album.tag_id==album.tag_id,
                                         Album.id != album.id).all()
    # 获取相册封面
    for recom in recommend_album:
        recom.cover = recom.photos[randint(0,len(recom.photos)-1)].name_thumb
        folder = recom.user.name + '/' + recom.title
        cover_url = photoSet.url(filename=folder+'/'+recom.cover)
        recom.cover_img = cover_url
    # 取出该相册下面的所有图片
    # photos = album.photos
    for photo in album.photos:
        photo_folder = album.user.name + '/' + album.title + '/'
        photo.url = photoSet.url(filename=photo_folder+photo.name_show)

    # 用查询到的数据填充渲染页面
    return render_template('album_browse.html',album=album,
                           user_photo_url=user_photo_url,
                           recommand_album=recommend_album,
                           favor_albums=favor_albums)

@main.route('/album_favor/',methods=['GET','POST'])
def album_favor():
    # 获取参数
    aid = request.args.get('aid')
    uid = request.args.get('uid')
    act = request.args.get('act')
    print('act:',act)
    album = Album.query.get_or_404(int(aid))
    if act == 'add':
        # 用户不能收藏自己的相册
        if album.user_id == session.get('user_id'):
            res = {'ok':-1}
        else:
            # 查询数据库是否已经存在该记录
            existed_count = AlbumFavor.query.filter_by(user_id=uid,
                                                       album_id=aid).count()
            if existed_count:
                res = {'ok':0}
            else:
                # 添加记录到数据库
                favor = AlbumFavor(user_id=uid,album_id=aid)
                res = {'ok':1}
                # 该相册的收藏量+1
                album.favornum += 1
                db.session.add(favor)
                db.session.commit()

    if act == 'del':
        favor = AlbumFavor.query.filter_by(user_id=uid,album_id=aid).first()
        res = {'ok':2}
        # 该相册的收藏量-1
        album.favornum -= 1
        db.session.delete(favor)
        db.session.commit()

    import json
    return json.dumps(res)  # 序列化
