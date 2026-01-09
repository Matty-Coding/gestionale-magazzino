from .database import User
from app.extensions import db
from app.utils.decorators import db_commiter

class UserCRUD:
    def __init__(self):
        self.session = db.session

    @db_commiter
    def create_user(
        self, username: str, email: str, password: str, ruolo: str | None
        ) -> User:
        """
        Crea un nuovo utente nel db e restituisce l'oggetto `User`.
        """

        user_obj = User(
            username=username,
            email=email.lower(),
            ruolo=ruolo
        )

        user_obj.set_password(password)

        self.session.add(user_obj)
        return user_obj
    

    def get_user(self, id: int) -> User:
        """
        Restituisce l'utente con l'id specificato.
        """
        return self.session.query(User).get(id)
    

    def get_user_by_email(self, email: str) -> User:
        """
        Restituisce l'utente con l'email specificata.
        """
        return self.session.query(User).filter_by(email=email.lower()).first()
    

    @db_commiter
    def update_username(self, user: User, username: str) -> User:
        """
        Aggiorna l'username dell'utente.
        """
        setattr(user, "username", username)
        return user
    

    @db_commiter
    def reset_password(self, user: User, password: str) -> None:
        """
        Resetta la password dell'utente nel db.
        """
        user.set_password(password)


    @db_commiter
    def delete_user(self, user: User) -> None:
        """
        Elimina l'utente dal db.
        """
        self.session.delete(user)