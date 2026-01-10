from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, EmailField,SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        render_kw = {"placeholder": "Mario"},
        validators=[
            DataRequired(message="Devi inserire un username!"),
            Length(min=3, max=25, message="L'username deve essere compreso tra 3 e 25 caratteri!"),
            Regexp(
                regex=r"^[A-Za-z][A-Za-z0-9 ]*$",
                message="L'username deve iniziare con una lettera e contenere solo lettere, numeri o spazi!",
            )
        ]
    )

    email = EmailField(
        "Email",
        render_kw = {"placeholder": "rossi.mario@esempio.it"},
        validators = [
            DataRequired(message="Devi inserire una email!"),
            Email(check_deliverability=True, message="L'email non è valida!"),
            Length(max=120, message="L'email non può essere più lunga di 120 caratteri!")
        ]
    )
        
    password = PasswordField(
        "Password",
        render_kw = {"placeholder": "••••••••"},
        validators = [
            DataRequired(message="Devi inserire una password!"),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!%*#?&.])[A-Za-z0-9@!%*#?&.]{8,}$",
                message="La password deve essere di almeno 8 caratteri e deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale!",
            )
        ]
    )

    password2 = PasswordField(
        "Conferma Password",
        render_kw = {"placeholder": "••••••••"},
        validators = [
            DataRequired(message="Devi confermare la password!"),
            EqualTo("password", message="Le password non corrispondono!")
        ]
    )

    ruolo = RadioField(
        "Ruolo",
        choices = [("cliente", "Cliente"), ("fornitore", "Fornitore")],
        default = "cliente"
    )

    submit = SubmitField("Registrati")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        render_kw = {"placeholder": "rossi.mario@esempio.it"},
        validators = [
            DataRequired(message="Devi inserire una email!"),
            Email(check_deliverability=True, message="L'email non è valida!"),
            Length(max=120, message="L'email non può essere più lunga di 120 caratteri!")
        ]
    )

    password = PasswordField(
        "Password",
        render_kw = {"placeholder": "••••••••"},
        validators = [
            DataRequired(message="Devi inserire una password!"),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!%*#?&.])[A-Za-z0-9@!%*#?&.]{8,}$",
                message="La password deve essere di almeno 8 caratteri e deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale!",
            )
        ]
    )

    remember = BooleanField("Ricordami", default=False)

    submit = SubmitField("Accedi")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "Email",
        render_kw = {"placeholder": "rossi.mario@esempio.it"},
        validators = [
            DataRequired(message="Devi inserire una email!"),
            Email(check_deliverability=True, message="L'email non è valida!"),
            Length(max=120, message="L'email non può essere più lunga di 120 caratteri!")
        ]
    )

    submit = SubmitField("Recupera Password")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        render_kw = {"placeholder": "••••••••"},
        validators = [
            DataRequired(message="Devi inserire una password!"),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!%*#?&.])[A-Za-z0-9@!%*#?&.]{8,}$",
                message="La password deve essere di almeno 8 caratteri e deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale!",
            )
        ]
    )

    password2 = PasswordField(
        "Conferma Password",
        render_kw = {"placeholder": "••••••••"},
        validators = [
            DataRequired(message="Devi confermare la password!"),
            EqualTo("password", message="Le password non corrispondono!")
        ]
    )

    submit = SubmitField("Cambia Password")