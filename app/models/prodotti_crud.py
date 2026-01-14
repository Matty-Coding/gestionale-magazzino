from .database import Prodotto
from app.extensions import db
from app.utils.decorators import db_commiter

class ProdottoCrud:
    def __init__(self):
        self.session = db.session

    @db_commiter
    def create_prodotto(self, **kwargs) -> Prodotto:
        """
        Crea un nuovo prodotto nel db e restituisce l'oggetto `Prodotto`.
        """
        prodotto_obj = Prodotto(**kwargs, categoria_id=4)
        self.session.add(prodotto_obj)
        return prodotto_obj
    
    def get_prodotto(self, codice: str) -> Prodotto:
        """
        Restituisce il prodotto con il codice specificato.
        """
        return self.session.query(Prodotto).filter_by(codice=codice).first()
    
    def get_prodotto_by_id(self, id: int) -> Prodotto:
        """
        Restituisce il prodotto con l'id specificato.
        """
        return self.session.query(Prodotto).filter_by(id=id).first()

    def get_all_prodotti(self) -> list[Prodotto]:
        """
        Restituisce tutti i prodotti presenti nel db.
        """
        return self.session.query(Prodotto).all()

    @db_commiter
    def update_prodotto(self, prodotto: Prodotto, **kwargs) -> Prodotto:
        """
        Aggiorna il prodotto nel db.
        """
        
        for key, value in kwargs.items():
            setattr(prodotto, key, value)
        
        return prodotto

    @db_commiter
    def delete_prodotto(self, prodotto: Prodotto):
        """
        Elimina il prodotto dal db.
        """
        
        self.session.delete(prodotto)
   

    # ================================================
    # ================= UTILITY ======================
    # ================================================
    def prodotti_in_esaurimento(self) -> list[Prodotto]:
        """
        Restituisce tutti i prodotti in esaurimento.
        """
        return self.session.query(Prodotto).where(Prodotto.quantita < 20).all()