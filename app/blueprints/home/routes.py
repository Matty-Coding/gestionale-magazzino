from flask import Blueprint, render_template
from flask_login import current_user, login_required

home_bp = Blueprint(
    name="home",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/"
)


@home_bp.route("/")
def index():
    return render_template("index.html")


@home_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        if current_user.ruolo == "cliente":
            return render_template("cliente_dashboard.html")
        return render_template("fornitore_dashboard.html")
    
    return render_template("admin_dashboard.html")    