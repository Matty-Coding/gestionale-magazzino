from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from .forms import RegisterForm, LoginForm
from app.extensions import limiter
from flask_login import login_required, login_user, logout_user, current_user
from app.utils.decorators import admin_required
from app.models.user_crud import UserCRUD
from app.services.mail_sender import send_email
from app.services.security import TokenService


auth = Blueprint(
    name="auth",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/auth"
)

usercrud = UserCRUD()

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if usercrud.get_user_by_email(form.email.data):
            return jsonify({"stato": "warning", "messaggio": "Email già registrata!"})

        user_obj = usercrud.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            ruolo=form.ruolo.data
        )

        return jsonify({"stato": "success", "messaggio": "Registrato con successo!"})


    return render_template("register.html", form=form)




@auth.get("/block")
def block():
    timer = request.args.get("timer")
    logout_user()
    session.clear()
    return render_template("block.html", timer=timer)