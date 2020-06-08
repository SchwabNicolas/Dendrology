from flask import redirect
from flask_login import current_user
from functools import wraps


def admin_perms_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin:
                print("TEST")
                return func()
        else:
            return redirect("/index")
    return decorated_view
