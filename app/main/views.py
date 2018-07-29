# 标准库
from datetime import datetime
# 第三方库
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
# 自写模块
from . import main
from .form import TODOForm, LoginForm, RegisterForm, ResetPassword, ForgetPassword, ChangPassword, ResetEmail
from app.models.article import Article
from app.models.user import User
from .. import db
from app.email import send_email
from flask_login import current_user


# 主页
@main.route('/')
def index():
    return render_template(
        'index.html', current_time=datetime.utcnow())


# ToDo编写页
@main.route('/prepare', methods=['POST', 'GET'])
@login_required
def prepare():
    form = TODOForm()
    if form.validate():
        with db.auto_commit():
            article = Article(title=form.title.data,
                              text=form.text.data)
            db.session.add(article)
            return redirect(url_for('main.index'))
    return render_template('prepare.html', form=form)


# 登录页
@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.confirm_password_hash(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('错误的密码或者邮箱地址')
    return render_template('login.html', form=form)


# 登出页
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出')
    return redirect(url_for('main.index'))


# 注册页
@main.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate():
        new_user = User(nickname=form.nickname.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        send_email(new_user.email, '确认您的账户', 'confirm',
                   user=new_user, token=token)
        flash('确认邮箱已发送至您的注册邮箱')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


# 账户确认页
@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经确认了账户')
    else:
        flash('确认账号链接出错或者链接超时')
    return redirect(url_for('main.index'))


# 钩子
@main.before_request
def before_request():
    if current_user.is_authenticated\
            and not current_user.confirmed:
            # and request.endpoint[:5] != 'main.'\
            # and request.endpoint != 'static':
        # return redirect(url_for('main.index'))
        return render_template('unconfirmed.html')


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')


@main.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的账户',
               'email/comfirm', user=current_user, token=token)
    flash('新的确认邮件已发送，请查收')
    return redirect(url_for('main.index'))


# 重设密码
@login_required
@main.route('/resetpassword', methods=['POST', 'GET'])
def reset_password():
    form = ChangPassword()
    if form.validate():
        with db.auto_commit():
            current_user.password = form.new_password.data
            db.session.add(current_user)
            logout_user()
            return redirect(url_for(main.login))
    return render_template('ChangPassword.html', form=form)


# 忘记密码
@main.route('/forgetpassword')
def forget_password():
    form = ForgetPassword()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_forget_password_token()
        send_email(user.email, '重置密码', 'email/reset_password',
                   user=user, token=token)
        flash('更改密码的邮件已发送至您的邮箱')
        return redirect(url_for('main.index'))
    return render_template('ForgetPassword.html', form=form)


# 重置密码页
@main.route('/resetpassword/<token>')
def resetpassword(token):
    form = ResetPassword()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        with db.auto_commit():
            user.password = form.new_password.data
            db.session.add(user)
            flash('重置密码成功')
            return redirect(url_for('main.login'))
    return render_template('ResetPassword.html', form=form)


# 重设电子邮箱地址
# @login_required
# @main.route('/resetemail')
# def reset_email():
#     form=ResetEmail()
#     if form.validate():
