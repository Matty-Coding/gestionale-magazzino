from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from decimal import Decimal

db = SQLAlchemy()

# =============================================================================
# =======================   Modello Categoria  ================================
# =============================================================================
class Categoria(db.Model):

    __tablename__ = "categorie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    descrizione: Mapped[str] = mapped_column(Text, nullable=True, default="Nessuna descrizione per questa categoria.")
    attiva: Mapped[bool] = mapped_column(Boolean, default=True)

    # relazione con la tabella prodotti
    prodotti = relationship("Prodotto", back_populates="categoria")

    def __str__(self):
        return self.nome
    

# =============================================================================
# =======================   Modello Prodotto   ================================
# =============================================================================
class Prodotto(db.Model):

    __tablename__ = "prodotti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codice: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    descrizione: Mapped[str] = mapped_column(Text, nullable=True, default="Nessuna descrizione per questo prodotto.")
    prezzo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantita: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attivo: Mapped[bool] = mapped_column(Boolean, default=True)

    # relazione con la tabella categorie
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorie.id"))
    categoria = relationship("Categoria", back_populates="prodotti")

    # relazione con la tabella fornitori
    fornitori = relationship("FornitoreProdotto", back_populates="prodotto", cascade="all, delete-orphan")


    def __str__(self):
        return self.nome



# =============================================================================
# =======================   Modello Fornitore  ================================
# =============================================================================
class Fornitore(db.Model):

    __tablename__ = "fornitori"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ragione_sociale: Mapped[str] = mapped_column(String(200), nullable=False)
    partita_iva: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)

    # relazione con la tabella prodotti
    prodotti = relationship("FornitoreProdotto", back_populates="fornitore", cascade="all, delete-orphan")

    def __str__(self):
        return self.ragione_sociale
    


# =============================================================================
# ===================   Modello FornitoreProdotto   ===========================
# =============================================================================
class FornitoreProdotto(db.Model):
    """
    Tabella di collegamento tra fornitore e prodotto
    """

    __tablename__ = "fornitore_prodotto"

    fornitore_id: Mapped[int] = mapped_column(ForeignKey("fornitori.id"), primary_key=True)
    prodotto_id: Mapped[int] = mapped_column(ForeignKey("prodotti.id"), primary_key=True)

    fornitore = relationship("Fornitore", back_populates="prodotti")
    prodotto = relationship("Prodotto", back_populates="fornitori")

    def __str__(self):
        return f"{self.fornitore} - {self.prodotto}"
    
