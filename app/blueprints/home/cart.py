from flask import session
from app.models.database import Prodotto
from app.models.prodotti_crud import ProdottoCrud

class Cart:
    def __init__(self):
        if "cart" not in session:
            session["cart"] = {}

        self.cart = session["cart"]

    def save(self):
        session.modified = True

    def aggiungi(self, prodotto_id: int, quantita=1):
        """
        Aggiunge un prodotto al carrello
        """
        prodotto_id = str(prodotto_id)
        if prodotto_id not in self.cart:
            self.cart[prodotto_id] = quantita
        else:
            self.cart[prodotto_id] += quantita

        self.save()

    def rimuovi(self, prodotto_id: int):
        """
        Rimuove un prodotto dal carrello
        """
        prodotto_id = str(prodotto_id)
        if prodotto_id in self.cart:
            del self.cart[prodotto_id]
            self.save()

    def modifica_quantita(self, prodotto_id: int, quantita: int):
        """
        Modifica la quantita di un prodotto nel carrello
        """
        prodotto_id = str(prodotto_id)
        if quantita <= 0:
            self.rimuovi(prodotto_id)
        elif ProdottoCrud().get_prodotto_by_id(prodotto_id).quantita > quantita: 
            self.cart[prodotto_id] = quantita
        else:
            self.cart[prodotto_id] = quantita
        
        self.save()
    
    
    def svuota(self):
        """
        Svuota il carrello
        """
        self.cart.clear()
        self.save()


    def totale(self, prodotti: list[Prodotto]) -> float:
        """
        Restituisce il totale del carrello
        """
        totale = 0
        for prodotto in prodotti:
            quantita = self.cart.get(str(prodotto.id), 0)
            totale += prodotto.prezzo * quantita

        return totale
    
    def __len__(self):
        return sum(self.cart.values())
    
    def clear(self):
        session.pop("cart", None)