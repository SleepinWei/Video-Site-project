# coding='utf-8'
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pymysql, os

app = Flask(__name__,
    static_folder="static",
    template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "some mysql database here"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "someVerySecretKey"
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')  # 设置上传文件保存路径
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/users/')  # 设置上传文件保存路径
app.debug = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from app.main import main as main_blueprint

app.register_blueprint(main_blueprint)
# app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 404错误处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
