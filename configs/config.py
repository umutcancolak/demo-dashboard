import os

class Config(object):
    SECRET_KEY = 'key'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db' sqlite URI
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:umut@127.0.0.1:5432/demo_dashboard"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'umut'
    ADMIN = {'username': 'admin',
             'email': 'admin',
             'password': 'admin'}

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None


class ProductionConfig(Config):
    DEBUG = False

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        os.environ.get('GENTELELLA_DATABASE_USER', 'gentelella'),
        os.environ.get('GENTELELLA_DATABASE_PASSWORD', 'gentelella'),
        os.environ.get('GENTELELLA_DATABASE_HOST', 'db'),
        os.environ.get('GENTELELLA_DATABASE_PORT', 5432),
        os.environ.get('GENTELELLA_DATABASE_NAME', 'gentelella')
    )


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
