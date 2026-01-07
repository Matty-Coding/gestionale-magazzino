from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for
from app.extensions import db

# =============================================
# Decoratore per verificare se l'utente è admin
# =============================================

def admin_required(f):
    """
    Decoratore per verificare se l'utente è admin.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        
        if not current_user.is_admin:
            abort(403)  # Forbidden (non hai i permessi necessari)

        return f(*args, **kwargs)
    return decorated_function


# ==============================================
# Decoratore per eseguire commit/rollback sul db
# ==============================================
def db_commiter(f):
    """
    Decoratore per eseguire commit/rollback sul db.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result

        except Exception as e:
            db.session.rollback()
            raise e
            
    return decorated_function
