from app.models.database import db, Categoria, Prodotto, Fornitore, FornitoreProdotto
from decimal import Decimal
from faker import Faker

fake = Faker(locale="it_IT")

def generate_fake_data():
    """
    Genera dati fittizi e li inserisce nel database
    """

    # ===================== CATEGORIE =====================
    nomi_categorie = ["informatica", "ufficio", "elettronica", "sconosciuto"]
    categorie = [Categoria(nome=nome) for nome in nomi_categorie]
    db.session.add_all(categorie)
    db.session.commit()

    # ===================== PRODOTTI =====================
    prodotti = []
    for _ in range(20):
        prodotto = Prodotto(
            codice = fake.unique.bothify(text="PROD-####"),
            nome = fake.word().title(),
            descrizione = fake.sentence(),
            prezzo = Decimal(fake.pydecimal(min_value=10, max_value=1000, right_digits=2, positive=True)),
            quantita = fake.random_int(min=0, max=100),
            categoria = fake.random_element(categorie)
        )

        prodotti.append(prodotto)

    db.session.add_all(prodotti)    
    db.session.commit()

    # ===================== RELAZIONI =====================
    fornitori = Fornitore.query.all()

    if not fornitori:
        return
    
    inseriti = set()   
    for _ in range(30):
        fornitore = fake.random_element(fornitori)
        prodotto = fake.random_element(prodotti)

        keys = (fornitore.id, prodotto.id)
        if keys not in inseriti:
            fornitore_prodotto = FornitoreProdotto(fornitore=fornitore, prodotto=prodotto)
            db.session.add(fornitore_prodotto)
            inseriti.add(keys)

    db.session.commit()