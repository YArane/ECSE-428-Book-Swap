class BaseConfig(object):
    MONGODB_SETTINGS = {'DB': 'bookswap_development', 'alias':'default'}
    TESTING = True
    SECRET_KEY = 'flask+mongoengine=<3'
    SECURITY_PASSWORD_SALT = 'istilllikenodejsmore'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'mcgillbookswap@gmail.com'
    MAIL_PASSWORD = 'ithinkthereforeiam3'
    MAIL_DEBUG = True