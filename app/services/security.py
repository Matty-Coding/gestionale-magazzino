from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from datetime import timedelta
from config import Config

class TokenService:
    """
    Gestisce la creazione e la validazione dei token per autenticazione e reset password.
    """
    
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        self.autentication_salt = Config.AUTHENTICATION_SALT
        self.reset_password_salt = Config.RESET_PASSWORD_SALT

    def generate_token(self, email:str, salt:str) -> str:
        """
        Genera un token per l'utente e con il salt specificati.
        """
        return self.serializer.dumps(email, salt=salt)

    def check_token(self, token:str, salt:str, expiration:timedelta) -> str | bool:
        """
        Controlla la validità del token con il salt e l'expiration specificati.

        Restituisce l'email se il token è valido, altrimenti restituisce False.
        """
        try:
            email = self.serializer.loads(
                token,
                salt=salt,
                max_age=expiration
            )

            return email

        except (SignatureExpired, BadTimeSignature):
            return False

    def get_auth_token(self, email:str) -> str:
        """
        Genera un token di autenticazione per l'utente con l'email specificata.
        """    
        return self.generate_token(
            email=email,
            salt=self.autentication_salt
        )

    def check_auth_token(self, token:str, expiration=timedelta(hours=1)) -> str | bool:
        """
        Verifica il token di autenticazione.
        """
        return self.check_token(
            token=token,
            salt=self.autentication_salt,
            expiration=expiration
        )
    
    def get_reset_password_token(self, email:str) -> str:
        """
        Genera un token per il reset password per l'utente con l'email specificata.
        """
        return self.generate_token(
            email=email,
            salt=self.reset_password_salt
        )
    
    def check_reset_password_token(self, token:str, expiration=timedelta(minutes=10)) -> str | bool:
        """
        Verifica token per il reset password.
        """
        return self.check_token(
            token=token,
            salt=self.reset_password_salt,
            expiration=expiration
        )