from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app.models import User, Role
from flask import session

#注册表单
class register_form(FlaskForm):
    name = StringField(label='用户名',validators=[DataRequired('用户名不能为空')])
    phone = StringField(label='电话',validators=[DataRequired('电话不能为空',Length(11,11,'长度必须为11位'))])
    email = StringField(label='邮箱地址',validators=[DataRequired('邮箱不能为空'),Email('请输入正确的邮箱格式')])  
    pwd = PasswordField(label='密码',validators=[DataRequired('密码不能为空')])
    repwd = PasswordField(label='重复密码',validators=[DataRequired('重复密码不能为空'),EqualTo('password')])
    submit = SubmitField(label='注册')

#登陆表单
class login_form(FlaskForm):
    name = StringField(label='用户名',validators=[DataRequired('用户名不能为空')])
    pwd = PasswordField(label='密码',validators=[DataRequired('密码不能为空')])
    submit = SubmitField(label='登录')
