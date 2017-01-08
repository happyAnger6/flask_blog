class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    debug = True
    SECRET_KEY = 'f83b0f4783562f0b8d4b27232e1abdec'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

