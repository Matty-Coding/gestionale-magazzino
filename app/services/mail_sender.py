from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config


def send_email(email: str, subject: str, message: str) -> bool:
    """Invia un email all'email con subject e message specificati."""

    sg = SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)

    message = Mail(
        from_email="tamati@myself.com",
        to_emails=email,
        subject=subject,
        html_content=message,
    )
    try:
        sg.send(message)
        return True

    except Exception:
        return False
