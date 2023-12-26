from flask import url_for
from functools import wraps
from flask_login import current_user
from werkzeug.utils import redirect

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin != 1:
            return redirect(url_for('auth.home'))
        return f(*args, **kwargs)
    return decorated_function