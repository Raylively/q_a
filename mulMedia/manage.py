
# python manage.py dev
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand,upgrade

from apps import db, app

# app = create_app()
manager = Manager(app)


migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# python manager.py db init
# python manager.py db migrate -m 'Initial migration'
# python manager.py db upgrade


@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)  # 自动打开浏览器
    # live_server.serve(open_url=True)  # 自动打开浏览器

@manager.command
def test():
    pass

@manager.command
def deploy():
    pass


if __name__ == '__main__':
    manager.run()