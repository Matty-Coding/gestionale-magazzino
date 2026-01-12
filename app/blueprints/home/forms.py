from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TelField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

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