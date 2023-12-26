from flask import Flask, Blueprint
from jinja2 import TemplatesNotFound



auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/auth/static'
)

@auth.route('/blue')
def blue():
    return 'Hola Blue'


from . import routes