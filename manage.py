from app.__init__ import create_app, db
# from app.models.article import Article, Admin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)


# def make_shell_context():
#     return dict(app=app, db=db, Article=Article, Admin=Admin)


# manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
