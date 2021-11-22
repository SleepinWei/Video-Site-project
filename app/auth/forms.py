from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import EqualTo, Regexp, Required,Length,Email, ValidationError
from ..models import User

class LoginForm(FlaskForm):
    name = StringField("username",validators=[Required()])
    password = PasswordField("Password",validators=[Required()])
    remember_me = BooleanField('Keep me logined in')
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    name = StringField('username',validators=[Required()\
    ,Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,"username must only have letters,numbers,dots or underscores")])
    password = PasswordField('Password',validators=[
        Required(),EqualTo('password2',message="Passwords must match")
    ])
    password2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Register')

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError("Username already in use")
        