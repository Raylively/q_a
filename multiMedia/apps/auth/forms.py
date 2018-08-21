from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField,TextAreaField,SelectField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空'),
                    Length(min=3,max=15,message='用户名长度在3-15之间!')],
        render_kw={'id':'user_name',
                   'class':'form-control',
                   'placeholder':'输入用户名',
                   'required':'required'}
    )
    user_pwd = PasswordField(
        label='密码',
        validators=[DataRequired(message='密码不能为空'),
                    Length(min=6, max=20, message='密码长度在6-20之间!')],
        render_kw={'id': 'user_pwd',
                   'class': 'form-control',
                   'placeholder': '输入密码',
                   'required': 'required'}

    )
    email = StringField(
        label='邮箱',
        validators=[DataRequired(message='邮箱不能为空'),
                    Email(message='邮箱格式不对')],
        render_kw={'id':'email',
                   'class':'form-control',
                   'placeholder':'输入邮箱'}

    )
    phone = StringField(
        label='手机号码',
        validators=[DataRequired(message='手机号码不能为空'),
                    Length(11,message='手机号长度必须为11')],
        render_kw={'id':'phone',
                   'class':'form-control',
                   'placeholder':'输入手机号'}

    )
    introduce = TextAreaField(
        label='自我介绍',
        validators=[],
        render_kw={'id':'introduce',
                   'class':'form-control',
                   'placeholder':'输入自我介绍'}
    )
    birthday = DateField(
        label='生日',
        validators=[DataRequired(message='用户生日不能为空')],
        render_kw={'id':'user_birthday',
                   'class':'form-control',
                   'placeholder':'请输入生日'}
    )


    photo = FileField(
        label='头像',
        validators=[FileRequired(message='图像不能为空'),
                    FileAllowed(['png','jpeg','gif','jpg'],message='只允许格式为%s的图片'%(['png','jpeg','gif','jpg']))],
        render_kw={'id':'photo',
                   'class':'form-control'}

    )
    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'注册'}
    )

class LoginForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空')],
        render_kw={'id':'user_name',
                   'class':'form-control',
                   'placeholder':'输入用户名',
                   'required':'required'}
    )
    user_pwd = PasswordField(
        label='密码',
        validators=[DataRequired(message='密码不能为空')],
        render_kw={'id': 'user_pwd',
                   'class': 'form-control',
                   'placeholder': '输入密码',
                   'required': 'required'}

    )
    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'登录'}
    )

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='密码',
        validators=[DataRequired(message='密码不能为空')],
        render_kw={'id': 'user_pwd',
                   'class': 'form-control',
                   'placeholder': '输入旧密码',
                   'required': 'required'}

    )
    new_pwd = PasswordField(
        label='密码',
        validators=[DataRequired(message='密码不能为空')],
        render_kw={'id': 'user_pwd',
                   'class': 'form-control',
                   'placeholder': '输入新密码',
                   'required': 'required'}

    )
    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'修改'}
    )

class DatailForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空'),
                    Length(min=3,max=15,message='用户名长度在3-15之间!')],
        render_kw={'id':'user_name',
                   'class':'form-control',
                   'placeholder':'输入用户名',
                   'required':'required'}
    )
    email = StringField(
        label='邮箱',
        validators=[DataRequired(message='邮箱不能为空'),
                    Email(message='邮箱格式不对')],
        render_kw={'id':'email',
                   'class':'form-control',
                   'placeholder':'输入邮箱'}

    )
    phone = StringField(
        label='手机号码',
        validators=[DataRequired(message='手机号码不能为空'),
                    Length(11,message='手机号长度必须为11')],
        render_kw={'id':'phone',
                   'class':'form-control',
                   'placeholder':'输入手机号'}

    )
    introduce = TextAreaField(
        label='自我介绍',
        validators=[],
        render_kw={'id':'introduce',
                   'class':'form-control',
                   'placeholder':'输入自我介绍'}

    )
    birthday = DateField(
        label='生日',
        validators=[DataRequired(message='用户生日不能为空')],
        render_kw={'id':'user_birthday',
                   'class':'form-control',
                   'placeholder':'请输入生日'}
    )
    photo = FileField(
        label='头像',
        validators=[],
        render_kw={'id':'photo',
                   'class':'form-control'}

    )
    submit = SubmitField(
        label='提交',
        render_kw={'class':'from-control btn btn-success',
                   'value':'修改'}
    )