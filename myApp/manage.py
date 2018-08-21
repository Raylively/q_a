'''
命令管理
'''
from runserver import app
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
from models import User,Question,Answer
import pymysql
pymysql.install_as_MySQLdb()

# python manage.py db init　
# 迁移
# python manage.py db migrate
# python manage.py db upgrade

manager = Manager(app)

# 绑定app和db
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
