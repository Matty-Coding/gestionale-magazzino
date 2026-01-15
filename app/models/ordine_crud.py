from .database import Ordine, OrdineDettaglio
from app.extensions import db
from app.utils.decorators import db_commiter
from decimal import Decimal
from .prodotti_crud import ProdottoCrud

class OrdineCrud:
    def __init__(self):
        self.session = db.session

    @db_commiter
    def create_ordine(self, cliente_id:int) -> Ordine:
        """
        Crea un nuovo ordine nel db e restituisce l'oggetto `Ordine`.
        """
        ordine_obj = Ordine(cliente_id=cliente_id)

        self.session.add(ordine_obj)
        self.session.flush()
        return ordine_obj
    
    def get_ordini_by_cliente_id(self, cliente_id:int) -> Ordine:
        """
        Restituisce tutti gli ordini nel db associato ad un utente.
        """
        return self.session.query(Ordine).filter_by(cliente_id=cliente_id).order_by(Ordine.id.desc()).all()


    def get_all_ordini(self) -> list[Ordine]:
        """
        Restituisce tutti gli ordini nel db.
        """
        return self.session.query(Ordine).order_by(Ordine.id.desc()).all()

    def get_ordine_by_id(self, ordine_id:int) -> Ordine:
        """
        Restituisce l'ordine con l'id specificato.
        """
        return self.session.query(Ordine).filter_by(id=ordine_id).first()

    @db_commiter
    def update_stato(self, ordine_id:int, stato:str) -> Ordine:
        """
        Aggiorna lo stato di un ordine nel db.
        """

        ordine = self.session.query(Ordine).filter_by(id=ordine_id).first()
        ordine.stato = stato
        return ordine
    
    @db_commiter
    def update_ordine(self, ordine:Ordine, **kwargs) -> Ordine:
        for key, value in kwargs.items():
            setattr(ordine, key, value)
        return ordine

    @db_commiter
    def elimina_ordine(self, ordine_id:int) -> None:
        """
        Elimina un ordine dal db.
        """
        ordine = self.get_ordine_by_id(ordine_id)
        self.session.delete(ordine)

    @db_commiter
    def create_dettagli_ordine(self, ordine_id:int, prodotto_id:int, quantita:int, prezzo_unitario:Decimal) -> OrdineDettaglio:
        """
        Crea un nuovo dettaglio di ordine nel db e restituisce l'oggetto `OrdineDettaglio`.
        """
        # Aggiorna disponibilità prodotti
        prodotti_crud = ProdottoCrud()
        prodotto = prodotti_crud.get_prodotto_by_id(prodotto_id)
        if prodotto:
            quantita_aggiornata = prodotto.quantita - quantita
            prodotti_crud.update_prodotto(prodotto, quantita=quantita_aggiornata)

        dettaglio_obj = OrdineDettaglio(
            ordine_id=ordine_id, 
            prodotto_id=prodotto_id, 
            quantita=quantita, 
            prezzo_unitario=Decimal(prezzo_unitario)
            )
        
        self.session.add(dettaglio_obj)
        return dettaglio_obj
    
    def get_dettagli_ordine_by_ordine_id(self, ordine_id:int) -> list[OrdineDettaglio]:
        """
        Restituisce tutti i dettagli di un ordine nel db.
        """
        return self.session.query(OrdineDettaglio).filter_by(ordine_id=ordine_id).all()