from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TelField, SelectField, TextAreaField, IntegerField, EmailField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Regexp, Email

class FornitoreForm(FlaskForm):
    ragione_sociale = SelectField(
        "Ragione sociale", 
        choices=[
            ("commerciale", "Commerciale"),
            ("economica", "Economica"),
            ("ambientale", "Ambientale")
        ],
        default="commercio"
        )
    
    partita_iva = StringField(
        "Partita IVA", 
        render_kw = {"placeholder": "12345678901"},
        validators = [
            DataRequired(message="Devi inserire una partita IVA!"),
            Length(min=11, max=11, message="La partita IVA deve essere di 11 caratteri!"),
            Regexp(
                regex=r"^[0-9]{11}$",
                message="La partita IVA deve contenere solo numeri!"
            )
        ]
    )

    telefono = TelField(
        "Telefono",
        render_kw = {"placeholder": "1234567890"},
        validators = [
            DataRequired(message="Devi inserire un numero di telefono!"),
            Length(min=10, max=10, message="Il numero di telefono deve essere di 10 caratteri!"),
            Regexp(
                regex=r"^[0-9]{10}$",
                message="Il numero di telefono deve contenere solo numeri!"
            )
        ]
    )

    submit = SubmitField("Cambia")


# PANNELLO AMMINISTRATORE

class ProdottoForm(FlaskForm):
    codice = StringField(
        "Codice",
        render_kw = {"placeholder": "PROD-1234"},
        validators = [
            DataRequired(message="Devi inserire un codice!"),
            Length(min=9, max=9, message="Il codice deve essere di 9 caratteri!"),
        ]
    )

    nome = StringField(
        "Nome",
        render_kw = {"placeholder": "Prodotto 1"},
        validators = [
            DataRequired(message="Devi inserire un nome!"),
            Length(min=1, max=50, message="Il nome deve essere di massimo 100 caratteri!"),
            Regexp(
                regex=r"^[A-Za-z0-9 ]+$",
                message="Il nome deve contenere solo lettere, numeri e spazi!"
            )
        ]
    )

    descrizione = TextAreaField(
        "Descrizione",
        render_kw = {"placeholder": "Descrizione del prodotto..."}
    )

    prezzo = StringField(
        "Prezzo",
        render_kw = {"placeholder": "19.99"},
        validators = [
            DataRequired(message="Devi inserire un prezzo!"),
            Length(min=3, max=7, message="Il prezzo deve essere almeno 3 caratteri e massimo 7!"),
            Regexp(
                regex=r"^[0-9]{1,4}(\.[0-9]{1,2})?$",
                message="Il prezzo deve essere del tipo XX.XX!"
            )
        ]
    )
    
    quantita = IntegerField(
        "Quantità",
        render_kw = {"placeholder": "10"}
    )


class UtenteForm(FlaskForm):
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
    
    ruolo = RadioField(
        "Ruolo",
        choices=[("ADMIN", "ADMIN"), ("CLIENTE", "CLIENTE"), ("FORNITORE", "FORNITORE")],
        default="CLIENTE"
    )

    verificato = BooleanField("Verificato", default=False)
