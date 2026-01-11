from app.models.user_crud import UserCRUD
from app.utils.decorators import db_commiter
from secrets import token_hex
from email_validator import validate_email, EmailNotValidError

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

    password = token_hex(8)

    user_obj = usercrud.create_user(
        username=f"admin-{token_hex(5)}",
        email=email,
        password=password,
        ruolo="ADMIN"
    )
    
    setattr(user_obj, "verificato", True)

    print("\nCreazione del profilo ADMIN in corso...")
    print(f"\n>>> Username: {user_obj.username}\n>>> Email: {user_obj.email}\n>>> Password: {password}")
    print("\nTi inviemo un'email con le credenziali per il login! Suggeriamo di cambiare la password dopo il login.") 