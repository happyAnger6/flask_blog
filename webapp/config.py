from os import path

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    debug = True
    SECRET_KEY = 'f83b0f4783562f0b8d4b27232e1abdec'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(
        path.pardir,
        'database.db'
    )
    MONGODB_SETTINGS = {
        'db': 'local',
        'host': '192.168.17.129',
        'port': 27017
    }

