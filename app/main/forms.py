# from re import S
# from typing_extensions import Required
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField,IntegerField,PasswordField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError
from wtforms import ValidationError
# from ..models import Role,User,Barrage,Video,Comment,Videocol,Videolike,UserExistError,UserNotFoundError

class NameForm(FlaskForm):
    name = StringField("your name",validators=[DataRequired()])
    submit = SubmitField('Submit')
    csrf_token = BooleanField("somethign")
    pwd = StringField("pwd")

# 重定向至编辑界面（从Space被引用）
class RedirectToEditForm(FlaskForm):
    editButton = SubmitField('Edit Profile')

# 用户编辑资料表单
class EditProfileForm(FlaskForm):
    nickName = StringField('Username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password=PasswordField('Password',validators=[EqualTo('password2',message='Passwords must match')])
    password2=PasswordField('Confirm password',validators=[])
    introduction=TextAreaField('Introduction',validators=[DataRequired()])
    submit=SubmitField('更新')


class EditProfileAdminForm(FlaskForm):
    # 管理员资料编辑表单
    pass 

class CommentForm(FlaskForm):
    body = TextAreaField("发送一条评论",validators=[DataRequired()])
    submit = SubmitField("发送")


