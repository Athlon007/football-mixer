import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    RESTX_MASK_SWAGGER = False
    ALLOWED_HOSTS = []

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOWED_HOSTS = ['*']

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    ALLOWED_HOSTS = ['*']

class ProductionConfig(Config):
    DEBUG = False
    ALLOWED_HOSTS = ['http://localhost:9000', 'http://127.0.0.1:9000']

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY