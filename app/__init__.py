# coding='utf-8'
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pymysql, os
# from config import config
from config import config
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate, migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
migrate = Migrate()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__,
        static_folder="static",
        template_folder="templates")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    db.init_app(app)
    # mail.init_app(mail)
    moment.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    
    # blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix="/auth")

    return app


# import main as main_blueprint 

# app.register_blueprint(admin_blueprint, url_prefix="/admin")

# 404错误处理