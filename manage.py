# from Danmu_db import User
from app.models import User,Role
from app import create_app,db 
# from flask_script import Manager,Shell
# from flask_migrate import Migrate 
# Flask_script and Migrate is no longer supported!
from flask.cli import FlaskGroup
from dotenv import load_dotenv

load_dotenv()
app = create_app('default')
# manager = Manager(app)
# migrate = Migrate(app,db)
cli = FlaskGroup(app)


# def make_shell_context():
#     return dict(app=app,db=db,User=User,Role=Role)
#     # return dict(app=app,db=db) don't know how to make commands here

# manager.add_command("shell",Shell(make_context=make_shell_context))
# manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    # manager.run()
    cli()