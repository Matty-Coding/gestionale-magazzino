from flask import Blueprint, render_template, request, url_for, session, jsonify, current_app
from .forms import RegisterForm, LoginForm
from app.extensions import limiter
from flask_login import login_required, login_user, logout_user, current_user
from app.utils.decorators import admin_required
from app.models.user_crud import UserCRUD
from app.services.mail_sender import send_email
from app.services.security import TokenService

auth_bp = Blueprint(
    name="auth",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/auth/static",
    url_prefix="/auth"
)

usercrud = UserCRUD()
token_serivice = TokenService()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        data = request.get_json()

        # logica validazione

    return render_template("register.html", form=form)