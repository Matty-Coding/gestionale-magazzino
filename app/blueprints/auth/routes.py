from flask import Blueprint, render_template, request, url_for, session, jsonify, current_app, redirect
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
token_service = TokenService()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        data = request.get_json()
        form = RegisterForm(data=data)

        if form.validate():
            if usercrud.get_user_by_email(data.get("email")):
                return jsonify({"status": "warning", "message": "Email già registrata"})   

            user_obj = usercrud.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
                ruolo=data.get("ruolo")
            )

            token = token_service.get_auth_token(user_obj.email)
            url = url_for("auth.verify_email", token=token, _external=True)
            
            try:
                send_email(
                    email=user_obj.email,
                    subject="Verifica email",
                    message=f"Per verificare la tua email <a href='{url}'>clicca qui</a><br> In alternativa incolla il seguente link nel tuo browser: {url}"
                )
                
                return jsonify({"status": "success", "message": "Ti abbiamo mandato una email di verifica"})
            
            except Exception:
                return jsonify({"status": "error", "message": "Errore nell'invio dell'email"})
 
        return jsonify({"status": "error", "message": form.errors})

    return render_template("register.html", form=form)


@auth_bp.route("/verify_email/<token>")
def verify_email(token):
    print("\n\n\n>>>", token)
    email = token_service.check_auth_token(token)
    if email:
        usercrud.get_user_by_email(email).validate_email
        return redirect(url_for("auth.login", result="success", message="Email verificata correttamente, puoi effettuare il login"))

    return render_template("login.html", form=LoginForm(), result="error", message="Link non valido o scaduto")
        

@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5/minute")
def login():
    form = LoginForm()

    if request.method == "POST":
        data = request.get_json()
        form = LoginForm(data=data)

        if form.validate():
            user_obj = usercrud.get_user_by_email(data.get("email"))

            if not user_obj:
                return jsonify({"status": "warning", "message": "Email non registrata"})

            if not user_obj.check_password(data.get("password")):
                return jsonify({"status": "error", "message": "Credenziali errate"})

            if not user_obj.is_verified:
                token = token_service.get_auth_token(user_obj.email)
                url = url_for("auth.verify_email", token=token, _external=True)
                
                try:
                    send_email(
                        email=user_obj.email,
                        subject="Verifica email",
                        message=f"Per verificare la tua email, clicca <a href='{url}'>qui</a>\n Oppure incolla il seguente link nel tuo browser: {url}"
                    )
                    
                    return jsonify({"status": "success", "message": "Ti abbiamo mandato una nuova email di verifica"})
                
                except Exception:
                    return jsonify({"status": "error", "message": "Errore nell'invio dell'email"})

            login_user(user_obj, remember=data.get("remember"))

            return jsonify({"status": "success", "message": "Login avvenuto con successo", "redirect": url_for("home.dashboard")})

        return jsonify({"status": "error", "message": form.errors})
    
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))


# RIVEDERE
@auth_bp.route("/block")
def block():
    if current_user.is_authenticated:
        logout_user()
    
    timer = request.args.get("timer")
    return render_template("block.html", timer=timer)