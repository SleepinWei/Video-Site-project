from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required
from flask_migrate import current
from flask_login import current_user
from werkzeug.urls import url_decode
from werkzeug.utils import redirect
from app.main.forms import EditProfileForm
from . import main
import flask
# from ..models import User
# from ..models import Video
from ..models import *

@main.route("/")
def index():
    # some functions to define hoempage of the website 
    pass

@main.route('/space')
def spaceDefault():
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
        return flask.render_template('UserSpace.html', user=current_user)

# Default space
@main.route('/space/')
def spaceDefaultAddition():
    #the same as above
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
        return flask.render_template('UserSpace.html', user=current_user)

# Redirect to user space
@main.route('/space/<username>')
@login_required
def spaceUser(username):
    #get the user from the database
    user1=User(username)

    return flask.render_template('UserSpace.html',user=user1)

@main.route('/video/<videoname>')
def playvideo(videoname):
    video1=Video(videoname)
    return flask.render_template('extend.html',video=video1)

@main.route("/edit-profile",methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickName = form.nickName.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("You have updated your profile")
        return redirect(url_for(".spaceUser",username=current_user.name))
    form.nickName.data = current_user.nickName
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)
