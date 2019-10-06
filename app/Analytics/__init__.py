from flask import Blueprint

blueprint = Blueprint(
    'Analytics_blueprint',
    __name__,
    url_prefix='/Analytics',
    template_folder='templates',
    static_folder='static'
)
