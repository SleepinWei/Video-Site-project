import os
basedir = os.path.abspath(os.path.dirname(__file__))

webName = "SabiSabi"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_SERVER = "smtp.163.com"
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = False
    MAIL_SENDER = ('SabiSabi Team',os.getenv('MAIL_USERNAME'))

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:000000@127.0.0.1:3306/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "DFVBNL"

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

config = {
    "default":Config,
    "dev":DevConfig,
}