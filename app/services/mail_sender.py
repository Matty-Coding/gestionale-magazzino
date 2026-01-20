from app.extensions import mail
from flask_mail import Message


def send_email(email: str, subject: str, message: str) -> bool:
    """Invia un email all'email con subject e message specificati."""

    msg = Message(
        subject=subject,
        recipients=[email],
        html=message
    )

    try:
        mail.send(msg)
        return True

    except Exception:
        return False
