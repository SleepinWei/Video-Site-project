# coding='utf-8'
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pymysql, os
from ..config import config
from flask_mail import Mail
from flask_moment import Moment


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__,
        static_folder="static",
        template_folder="templates")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(mail)
    moment.init_app(mail)

    # blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# import main as main_blueprint 

# app.register_blueprint(admin_blueprint, url_prefix="/admin")

# 404错误处理