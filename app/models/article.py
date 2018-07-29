from .base import db


class Article(db.Model):

    __tablename__ = 'article'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(32))
    text = db.Column(db.Text)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<username: %r>' % self.username


# class Admin(db.Model):

#     __tablename__ = 'admin'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(32), unique=True)
#     password = db.Column(db.String(128))

#     def __repr__(self):
#         return '<username= %r>' % self.username
