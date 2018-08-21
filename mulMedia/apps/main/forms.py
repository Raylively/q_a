from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField

class AlbumInfoForm(FlaskForm):
    album_title = StringField(
        label='相册标题',
        validators=[DataRequired(message='相册标题不能为空'),
                    Length(min=3,max=15,message='相册标题长度在3-15之间!')],
        render_kw={'id':'album_title',
                   'class':'form-control',
                   'placeholder':'请输入相册标题',
                   'required':'required'}
    )

    album_desc = TextAreaField(
        label='相册描述',
        validators=[DataRequired(message='相册描述不能为空'),
                    Length(min=10,max=200,message='相册描述长度在10-200之间!')],
        render_kw={'id':'album_desc',
                   'class':'form-control',
                   'rows':'3',
                   'required':'required'}
    )

    album_privacy = SelectField(
        label='相册浏览权限',
        validators=[DataRequired(message='相册权限不能为空'),],
        coerce=str,
        choices=[('private','自己可见'),('protect_1','粉丝可见'),
                 ('protect_1', '收藏可见'),('public','全部可见')],
        render_kw={'id':'album_privacy',
                   'class':'form-control',}
    )

    album_tag = SelectField(
        label='相册类别标签',
        validators=[DataRequired(message='相册类别不能为空'),],
        coerce=int,
        # choices=[(1,'萌宠'),(2,'风景'),
        #          (3, '美女'),(4,'动漫')],
        # choices=[(tag.id,tag.name) for tag in album_tags],
        # choices='',
        render_kw={'id':'album_tag',
                   'class':'form-control',}
    )
    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'创建相册信息'}
    )

    #试问卷帘人，却道是海棠依旧！知否知否，应是绿肥红瘦！
    # def __init__(self, *args, **kwargs):
    #     self.album_tag.choices = [(tag.id,tag.name) for tag in AlbumTag.query.all()]
    #     super().__init__(*args, **kwargs)

class AlbumUploadForm(FlaskForm):

    album_title = SelectField(
        validators=[DataRequired(message='相册名称不能为空'),],
        coerce=int,
        # choices=[(1,'萌宠'),(2,'风景'),
        #          (3, '美女'),(4,'动漫')],
        # choices=[(tag.id,tag.name) for tag in album_tags],
        # choices='',
        render_kw={'id':'album_title',
                   'class':'form-control',}
    )

    album_upload = FileField(
        validators=[FileRequired(message='请选择一张或多张图片'),],
        render_kw={'id':'ablum_upload','class':'form-control',
                   'multiple':'multiple'}
    )

    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'上传相册图片'}
    )
