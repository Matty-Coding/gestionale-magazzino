from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config

def send_email(email:str, subject:str, message:str) -> bool:
    """Invia un email all'email con subject e message specificati."""
    
    message = Mail(
        from_email=Config.SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=message,
    )
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        sg.send(message)
        return True

    except Exception:
        return False

