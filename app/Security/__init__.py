from flask import Blueprint

blueprint = Blueprint(
    'Security_blueprint',
    __name__,
    url_prefix='/Security',
    template_folder='templates',
    static_folder='static'
)
