from re import S
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp
from wtforms import ValidationError
# from ..models import Role,User,Barrage,Video,Comment,Videocol,Videolike,UserExistError,UserNotFoundError

class NameForm(FlaskForm):
    name = StringField("your name",validators=[DataRequired()])
    submit = SubmitField('Submit')
    csrf_token = BooleanField("somethign")
    pwd = StringField("pwd")

class EditProfileForm(FlaskForm):
    nickName = StringField("Nick name",validators=[Length(0,64)])
    location = StringField("Location",validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

