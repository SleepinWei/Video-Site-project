from flask.app import Flask
from flask.signals import message_flashed
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import EqualTo, Regexp, Required,Length,Email, ValidationError,DataRequired
from ..models import User

class LoginForm(FlaskForm):
    name = StringField("username",validators=[Required()])
    password = PasswordField("Password",validators=[Required()])
    remember_me = BooleanField('Keep me logined in')
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired('Please enter username!')\
    ,Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,"username must only have letters,numbers,dots or underscores")])
    password = PasswordField('Password',validators=[
        DataRequired('Please enter password!'),EqualTo('password2',message="Passwords must match")
    ])
    password2 = PasswordField('Confirm password',validators=[DataRequired('Please enter password again!')])
    email = StringField('Email',validators=[DataRequired('please enter email!'),Email('Email format is incorrect!')])
    phone = StringField('Phone',validators=[DataRequired('please enter phone number'),Regexp("1[3458]\\d[9]", message="Phone number format is incorrect")])
    check = BooleanField('User agreement')
    submit = SubmitField('Register')
    #请加入必须同意用户协议才能注册的逻辑
    
    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError("Username already in use")
    def validate_username(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("The email address has been registered")
    def validate_username(self,field):
        if User.query.filter_by(phone=field.data).first():
            raise ValidationError("The phone number has been registered")
        
class ChangePassword(FlaskForm):
    # 更改用户密码
    password = PasswordField("Original password",validators=[Required()])
    newpassword = PasswordField("Newpassword",validators=[Required(),
                        EqualTo('password2',message="Passwords must match!")])
    password2 = PasswordField("Confirm password",validators=[Required()])
    submit = SubmitField("Submit")

class ResetPassword(FlaskForm):
    # 忘记密码时
    # 需要加入邮箱验证
    pass

class ChangeEmail(FlaskForm):
    # 修改email
    pass
