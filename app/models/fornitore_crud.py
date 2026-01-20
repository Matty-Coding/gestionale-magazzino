from app.models.database import User, Fornitore
from app.extensions import db
from app.utils.decorators import db_commiter


class FornitoreCRUD:
    def __init__(self):
        self.session = db.session

    @db_commiter
    def create_fornitore(
        self, user: User, ragione_sociale: str = None, partita_iva: str = None, telefono: str = None
    ) -> Fornitore:
        """
        Crea un fornitore associato a un utente esistente.
        """

        if user.fornitore:
            raise ValueError("L'utente ha già un fornitore associato")

        fornitore_obj = Fornitore(
            ragione_sociale=ragione_sociale,
            partita_iva=partita_iva,
            telefono=telefono,
            user_id=user.id,
        )

        self.session.add(fornitore_obj)
        return fornitore_obj

    def get_fornitore(self, user_id: int) -> Fornitore:
        """
        Restituisce il fornitore associato ad un utente esistente.
        """
        return self.session.query(Fornitore).filter_by(user_id=user_id).first()

    @db_commiter
    def update_fornitore(self, user_id: int, **kwargs) -> Fornitore:
        """
        Aggiorna un fornitore associato ad un utente esistente.
        """

        fornitore_obj = self.session.query(Fornitore).filter_by(user_id=user_id).first()

        for key, value in kwargs.items():
            setattr(fornitore_obj, key, value)

        return fornitore_obj
