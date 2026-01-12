from app.models.user_crud import UserCRUD
from app.utils.decorators import db_commiter
from secrets import token_hex
from email_validator import validate_email, EmailNotValidError
from app.services.mail_sender import send_email

usercrud = UserCRUD()

@db_commiter
def create_admin():
    while True:
        email = input("Inserisci un'email valida: ").strip().lower()
        try:
            validate_email(email, check_deliverability=True)
            break
            
        except EmailNotValidError:
            print("L'email non è valida!")

    password = f"ADMIN.{token_hex(4)}"

    user_obj = usercrud.create_user(
        username=f"admin-{token_hex(3)}",
        email=email,
        password=password,
        ruolo="ADMIN"
    )
    
    setattr(user_obj, "verificato", True)

    print("\nCreazione del profilo ADMIN in corso...")
    print(f"\n>>> Username: {user_obj.username}\n>>> Email: {user_obj.email}\n>>> Password: {password}")
    print("\nTi invieremo un'email con le credenziali per il login! Suggeriamo di cambiare la password dopo il login.")

    # send_email(
    #     email=user_obj.email,
    #     subject="Credenziali per il login con ruolo ADMIN",
    #     message=f"<h2>Suggeriamo di cambiare subito le credenziali appena effettuato il primo login!</h2><p><strong>Username:</strong> {user_obj.username}<br><strong>Email:</strong> {user_obj.email}<br><strong>Password:</strong> {password}</p>"
    # )       