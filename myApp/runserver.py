

from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_mail import Mail
import config
from decorators import login_reuired
from exts import db
from forms.auth import ResetPasswordForm
from models import User, Question,Answer
from sqlalchemy import or_

app = Flask(__name__)
mail = Mail(app)

app.config.from_object(config)
db.init_app(app)
mail.init_app(app)



@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('-create_date').all()
    }

    return render_template('index.html',**context)

@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # username = request.form['username']
        username = request.form.get('username')
        # password = request.form['password']
        password = request.form.get('password')
        print('input:{}-{}'.format(username,password))
        # user_info = User.query.filter(User.username == username,User.password == password).first()
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 设置31天内不需要登录
            session.permanent = True
            return redirect(url_for('index',username=username))
        else:
            return '用户名或密码错误，请核对好重新登录'


@app.route('/register/',methods=['POST','GET'])
def register():
    print('register method is:',request.method)
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 用户名验证
        db_username = User.query.filter(User.username == username).first()
        # print('username':)
        if db_username:
            return '该用户名已注册，请另取一个'
        else:
            #　密码验证
            if password1 != password2:
                return '两次输入的密码不行等，请核对后再次输入'
            else:
                user_info = User(username=username,password=password1)
                db.session.add(user_info)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('user_id')
    # del session['user_id']
    # session.clear()
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_reuired
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        user = g.user
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
# @login_reuired
def detail(question_id):
    question_info = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_info)

@app.route('/add_comment/',methods=['POST'])
@login_reuired
def add_comment():
    print('in add_comment:')
    content = request.form.get('comment')
    question_id = request.form.get('question_id')
    print('add_comment:',question_id,content)
    answer = Answer(content=content)
    # user_id = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    user = g.user
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    print('in search:',q)
    # 或条件
    questions = Question.query.filter(or_(Question.title.contains(q),
                              Question.content.contains(q))).order_by('-create_date')
    # 与条件
    # Question.query.filter(Question.title.contains(q),Question.content.contains(q))
    return render_template('index.html',questions=questions)

# @app.route('/reset_password',methods=['GET','POST'])
# def forget_password():
#
#     if request.method == 'POST':
#         if form.validate():
#             account_email = form.email.data
#             user = User.query.filter_by(email=account_email).first_or_404()
#
#             send_mail(form.email.data,
#                       '重置你的密码',
#                       'reset_password.html',
#                       user=user,
#                       token='123123')
#     return render_template('forget_password.html',form=form)
#
# @app.route('/reset/password/<token>',methods=['POST','GET'])
# def reset_password(token):
#     form = ResetPasswordForm(request.form)
#     if request.method == 'POST' and form.validate():
#         pass

# 每次请求都会先执行此函数
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # g 对象
            g.user = user


# 上下管理器，定义的变量在模板中通用，返回值必须是字典类型－－－－钩子函数的一种
@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

if __name__ == '__main__':
    app.run()
