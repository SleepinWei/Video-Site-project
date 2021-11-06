import flask

#Temporary definition
class User:
    #def __init__(username,NickName, ID, VIP,Level, LevelProgress,    Coins,    Stars,    Introduction):
    def __init__(self,name):
        self.NickName=name+'Nick'
        self.ID=name+'ID'
        self.VIP=True
        self.Level=4
        self.LevelProgress=30
        self.Coins=10
        self.Stars=4
        self.Introduction="23333333"
        self.FavouriteVideo=[{'name':'v1', 'Information':'i1john','Path':'none'},{'name':'v2', 'Information':'i2john','Path':'none'}]

app = flask.Flask(__name__)

# Default space
@app.route('/space')
def spaceDefault():
    return flask.render_template('DefaultSpace.html')

# Default space
@app.route('/space/')
def spaceDefaultAddition():
    return flask.render_template('DefaultSpace.html')

# Redirect to user space
@app.route('/space/<username>')
def spaceUser(username):
    # Wait background for query.
    user1=User(username)
    #user.FavouriteVideo[1].Name='666'
    #user.FavouriteVideo[1].Information='232323232'
    #user.FavouriteVideo[2].Name='777'
    #user.FavouriteVideo[2].Information='7676767676'

    return flask.render_template('UserSpace.html',user=user1)
app.run();