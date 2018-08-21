from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class EmailForm(Form):
    email = StringField(validators=[
        DataRequired(),Length(8,64),
        Email(message='电子邮箱不符合规范')
    ])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6,32,message='密码长度在6-32个字符之间'),
        EqualTo('password2',message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(),Length(6,32)
    ])