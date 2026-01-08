from flask import Blueprint, render_template, request, url_for, session, jsonify, current_app
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
token_serivice = TokenService()

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

        token = token_serivice.get_auth_token(user_obj.email)
        url = url_for("auth.verify", token=token, _external=True)

        if not send_email(
            email=user_obj.email,
            subject="Autenticazione e Attivazione dell'account",
            message=f"Verifica della registrazione di {user_obj.username}\nClicca o incolla questo link nel tuo browser\n{url}"
        ):
            return jsonify({"stato": "error", "messaggio": "Email non inviata!"})

        return jsonify({
            "stato": "success", 
            "messaggio": "Registrato con successo!",
            "redirect": url_for("auth.login")
            })

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_obj = usercrud.get_user_by_email(form.email.data)
        if user_obj and user_obj.check_password(form.password.data):
            login_user(user_obj)
            session["user_id"] = user_obj.id
            
            return jsonify({
                "stato": "success", 
                "messaggio": "Login effettuato con successo!",
                "redirect": url_for("home.dashboard")
                })

        return jsonify({"stato": "warning", "messaggio": "Credenziali errate!"})

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return jsonify({"stato": "success", "messaggio": "Logout effettuato con successo!"})



@auth.get("/block")
def block():
    timer = request.args.get("timer")
    logout_user()
    session.clear()
    return render_template("block.html", timer=timer)