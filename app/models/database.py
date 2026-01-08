from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime, timezone
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

# =============================================================================
# =======================   Modello Categoria  ================================
# =============================================================================
class Categoria(db.Model):

    __tablename__ = "categorie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    descrizione: Mapped[str] = mapped_column(Text, default="Nessuna descrizione per questa categoria.")
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
    descrizione: Mapped[str] = mapped_column(Text, default="Nessuna descrizione per questo prodotto.")
    prezzo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantita: Mapped[int] = mapped_column(Integer, default=0)
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

    # relazione con la tabella users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="fornitore", uselist=False)

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
    


# =============================================================================
# ==========================   Modello User   =================================
# =============================================================================
class User(db.Model, UserMixin):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    ruolo: Mapped[str] = mapped_column(String(20), default="CLIENTE")
    verificato: Mapped[bool] = mapped_column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.ruolo == "ADMIN"
    
    @property
    def is_verified(self) -> bool:
        return self.verificato == True

    def __str__(self):
        return f"{self.username} - {self.email} - {self.ruolo} - {'Verificato' if self.verificato else 'NonVerificato'}"
    


# =============================================================================
# =======================   Modello IP Bloccati   =============================
# =============================================================================
class IpBloccati(db.Model):

    __tablename__ = "ip_bloccati"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    blocked_until: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    def is_blocked(self):
        return datetime.now(timezone.utc) < self.blocked_until
