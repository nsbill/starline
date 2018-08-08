class Configuration(object):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='postgresql://dbuser:3a3Hfde20NEN@db/dbaser'
    SECRET_KEY='pdFS8sd0H9SD0Dsddfgsad3iu03aj99GJkgXKSS5uP3i9yY8NjsOvibKKOZ7T'
    ### Flask-Security
    SECURITY_PASSWORD_SALT='salt'
    SECURITY_PASSWORD_HASH='sha512_crypt'
