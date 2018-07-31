from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown


from app.models.base import db
from config import Config


bootstrap = Bootstrap()
moment = Moment()
# db = SQLAlchemy() 选择在models文件夹下，为了穿件私有的sqlalchemy方法

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 'base'/None
login_manager.login_veiw = 'login'

email = Mail()
pagedown = PageDown()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册bootstrap
    bootstrap.init_app(app)

    # 注册moment
    moment.init_app(app)

    # 注册SQLAlchemy
    db.init_app(app)

    # 注册Login
    login_manager.init_app(app)

    # 注册Mail
    email.init_app(app)

    # 注册PageDown
    pagedown.init_app(app)

    # flask-login的回调函数，在此处调用为的是免去出入栈的代码
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
        # return None

    # 注册蓝本
    from .main import main
    app.register_blueprint(main)

    return app
