from flask_mail import Message

from runserver import mail
from flask import current_app,render_template



# # 异步发送邮件
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

def send_mail(to,subject,template,**kwargs):
    msg = Message(
        subject,
        sender=current_app.config(['MAIL_USERNAME']),
        recipients=[to],
    )
    msg.html = render_template(template,**kwargs)
    mail.send(msg)
    # msg = Message(
    #     '测试邮件',
    #     sender='752958210@qq.com',
    #     body='test',
    #     recipients=['752958210@qq.com']
    # )
    mail.send()