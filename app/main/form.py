from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from flask_login import current_user
from flask_pagedown.fields import PageDownField

from app.models.user import User


class TODOForm(FlaskForm):

    title = StringField('输入题目', validators=[
        DataRequired(), Length(min=0, max=20)])
    text = PageDownField('输入ToDo', validators=[DataRequired()])
    # checkbox = BooleanField('have do?', validators=[DataRequired()])
    submit = SubmitField('提交')


class RegisterForm(FlaskForm):

    nickname = StringField('输入您的昵称', validators=[
        DataRequired(), Length(1, 32),
        Regexp('^[A-Za-z][A-Za-z-9_.]*$',
               0, '昵称只能由文字或者字母构成，不能使用下划线或者符号')])
    email = StringField('输入您的邮件地址', validators=[DataRequired(), Email()])
    password = PasswordField('输入您的密码', validators=[DataRequired()])
    password2 = PasswordField('重复您的密码', validators=[
                              DataRequired(), EqualTo('password', message='两次密码输入不一致')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已经注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('此昵称已存在，请更换昵称')


class LoginForm(FlaskForm):

    email = StringField('输入您的邮件地址', validators=[DataRequired()])
    password = PasswordField('输入您的密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class ChangePassword(FlaskForm):
    old_password = PasswordField('输入您的旧密码', validators=[
                                 DataRequired(), Length(8, 16)])
    new_password = PasswordField('输入您的新密码', validators=[
                                 DataRequired(), Length(8, 16), EqualTo('old_password', message='新密码与旧密码重复，请输入新的密码')])
    new_password2 = PasswordField('重复您的新密码', validators=[
                                  DataRequired(), EqualTo('new_password', message='两次密码输入不一致')])
    submit = SubmitField('提交')

    # def validate_old_password(self, field):
    #     if not User.query.filter_by(password_hash=field.data).first():
    #         raise ValidationError('当前用户密码输入错误，请输入当前使用的密码')


class ForgetPassword(FlaskForm):
    email = StringField('输入您的账户邮箱', validators=[Email(), DataRequired()])
    submit = SubmitField('点击发送更改密码邮件')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('您输入的邮箱未注册，请输入正确的邮箱地址')


class ResetPassword(FlaskForm):
    email = StringField('您的邮箱账号', validators=[Email(), DataRequired()])
    new_password = PasswordField('新的密码', validators=[DataRequired()])
    new_password2 = PasswordField('重复新的密码', validators=[
                                  DataRequired(), EqualTo('new_passworde', message='两次密码输入不一致')])
    submit = SubmitField('确认提交')


class ResetEmail(FlaskForm):
    old_email = StringField('输入您旧的邮箱地址', validators=[DataRequired(), Email()])
    new_email = StringField('输入您新的邮箱地址', validators=[DataRequired(), Email()])
    submit = SubmitField('确认')

    def validate_old_email(self, field):
        if current_user.email != field.data:
            raise ValidationError('您不能更改他人的账号的绑定邮箱')
