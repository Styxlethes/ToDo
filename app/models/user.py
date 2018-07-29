import hashlib

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request

from .base import db


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.String(32))
    email = db.Column(db.String(32))
    count = db.Column(db.Integer(), default=0)
    articles = db.relationship('Article', backref='user')
    confirmed = db.Column(db.Boolean, default=False)

    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<nickname: %r>' % self.nickname

    #???????
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def confirm_password_hash(self, raw):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw)

    def generate_confirmation_token(self, expires_in=3600):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=current_app.config['EXPIRATION'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_forget_password_token(self, expires_in=3600):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=current_app.config['EXPIRATION'])
        return s.dumps({'reset_password': self.id})

    def reset_password(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset_password') != self.id:
            return False
        return True

    def change_email(self, token):
        pass

    def gravatar(self, size=100, default='idention', rating='g'):
        if request.is_secure:
            url = 'http://www.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hahs=hash, size=size, default=default, rating=rating)
