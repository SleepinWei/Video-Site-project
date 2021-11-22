from . import main
import flask
from ..models import User
from ..models import Video

@main.route("/")
def index():
    # some functions to define hoempage of the website 
    pass

@main.route('/space')
def spaceDefault():
    return flask.render_template('DefaultSpace.html')

# Default space
@main.route('/space/')
def spaceDefaultAddition():
    return flask.render_template('DefaultSpace.html')

# Redirect to user space
@main.route('/space/<username>')
def spaceUser(username):
    # Wait background for query.
    user1=User(username)
    #user.FavouriteVideo[1].Name='666'
    #user.FavouriteVideo[1].Information='232323232'
    #user.FavouriteVideo[2].Name='777'
    #user.FavouriteVideo[2].Information='7676767676'

    return flask.render_template('UserSpace.html',user=user1)

@main.route('/video/<videoname>')
def playvideo(videoname):
    video1=Video(videoname)
    return flask.render_template('extend.html',video=video1)

