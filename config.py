import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # wtform
    SECRET_KEY = os.environ.get('SECRCT_KEY') or 'caonimab'

    # flask
    DEBUG = True

    # flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:081791@localhost:3376/todo'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-mail
    MAIL_DEBUG = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '642698748@qq.com'
    MAIL_PASSWORD = 'khsdmeyhivmibbcg'
    MAIL_SENDER = '642698748@qq.com'

    # 邮件过期时间
    EXPIRATION = 3600
