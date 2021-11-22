from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp
from wtforms import ValidationError
from ..models import Role,User,Barrage,Video,Comment,Videocol,Videolike,UserExistError,UserNotFoundError

class NameForm(FlaskForm):
    name = StringField("your name",validators=[DataRequired()])
    submit = SubmitField('Submit')
    csrf_token = BooleanField("somethign")
    pwd = StringField("pwd")
    