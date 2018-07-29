from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(401)
def Unauthorized(e):
    return render_template('errors/401.html'), 401
