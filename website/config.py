import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    #SQLALCHEMY_DATABASE_URI = 'postgresql://gwsqrcgk:ErDiJiKEHXR1Bc_PnXglo6nl3J3W44BA@hattie.db.elephantsql.com/gwsqrcgk'
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_POSTGRES")
    SECRET_KEY = "oWtvvLGmRqQgwBmsnryX4s3a6JFGcelX"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = "secret_for_test_environment"
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True