from .database import IpBloccato
from app.extensions import db
from app.utils.decorators import db_commiter
from datetime import datetime, timezone, timedelta


class IpCRUD:
    def __init__(self):
        self.session = db.session

    @db_commiter
    def create_blocked_ip(self, ip: str) -> IpBloccato:
        """
        Crea un nuovo ip bloccato nel db e restituisce l'oggetto `IpBloccati`.
        """
        blocked = IpBloccato(
            ip=ip, blocked_until=datetime.now(timezone.utc) + timedelta(minutes=5)
        )
        self.session.add(blocked)

        return blocked

    def get_blocked_ip(self, ip: str) -> IpBloccato:
        """
        Restituisce l'ip bloccato.
        """
        return self.session.query(IpBloccato).filter_by(ip=ip).first()

    @db_commiter
    def update_blocked_ip(self, ip: IpBloccato) -> IpBloccato:
        """
        Aggiorna l'ip bloccato nel db.
        """
        setattr(ip, "blocked_until", datetime.now(timezone.utc) + timedelta(minutes=5))

    @db_commiter
    def delete_blocked_ip(self, ip: IpBloccato) -> None:
        """
        Elimina l'ip bloccato dal db.
        """
        self.session.delete(ip)
