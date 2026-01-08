from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, EmailField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        render_kw = {"placeholder": "Username", "autofocus": "on"},
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
        render_kw = {"placeholder": "Email"},
        validators = [
            DataRequired(message="Devi inserire una email!"),
            Email(check_deliverability=True, message="L'email non è valida!"),
            Length(max=120, message="L'email non può essere più lunga di 120 caratteri!")
        ]
    )
        
    password = PasswordField(
        "Password",
        render_kw = {"placeholder": "Password"},
        validators = [
            DataRequired(message="Devi inserire una password!"),
            Length(min=8, message="La password deve contenere almeno 8 caratteri!"),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!%*#?&.])[A-Za-z0-9@!%*#?&.]{8,}$",
                message="La password deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale!",
            )
        ]
    )

    password2 = PasswordField(
        "Conferma Password",
        render_kw = {"placeholder": "Conferma Password"},
        validators = [
            DataRequired(message="Devi confermare la password!"),
            EqualTo("password", message="Le password non corrispondono!")
        ]
    )

    ruolo = SelectField(
        "Ruolo",
        choices = [("cliente", "Cliente"), ("fornitore", "Fornitore")],
    )

    submit = SubmitField("Registrati")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        render_kw = {"placeholder": "Email", "autofocus": "on"},
        validators = [
            DataRequired(message="Devi inserire una email!"),
            Email(check_deliverability=True, message="L'email non è valida!"),
            Length(max=120, message="L'email non può essere più lunga di 120 caratteri!")
        ]
    )

    password = PasswordField(
        "Password",
        render_kw = {"placeholder": "Password"},
        validators = [
            DataRequired(message="Devi inserire una password!"),
            Length(min=8, message="La password deve contenere almeno 8 caratteri!"),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!%*#?&.])[A-Za-z0-9@!%*#?&.]{8,}$",
                message="La password deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale!",
            )
        ]
    )

    remember = BooleanField("Ricordami", default=False)

    submit = SubmitField("Accedi")

