from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email

class LoginForm(Form):
    username = StringField("username",validators=[Required()])
    password = PasswordField("Password",validators=[Required()])
    remember_me = BooleanField('Keep me logined in')
    submit = SubmitField("Login")
