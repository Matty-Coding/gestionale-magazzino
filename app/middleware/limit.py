from flask import request, redirect, url_for
from datetime import datetime, timezone, timedelta
from flask_limiter.util import get_remote_address
from app.models.database import IpBloccati
from app.extensions import db

class MiddleWare:
    @property
    def get_ip(self):
        return request.headers.get("X-Forwarded-For", get_remote_address())
    
    def check_ip(self):
        ip = self.get_ip
        blocked = IpBloccati.query.filter_by(ip=ip).first()
        
        if not blocked:
            return None

        if blocked.is_blocked():
            timer = int(blocked.blocked_until - datetime.now(timezone.utc).total_seconds())
            return redirect(url_for("auth.block", timer=timer))

        db.session.delete(blocked)
        db.session.commit()
        return None


    def limit_handler(self, e):
        ip = self.get_ip
        block_time = datetime.now(timezone.utc) + timedelta(minutes=5)

        blocked = IpBloccati.query.filter_by(ip=ip).first()

        if blocked:
            blocked.blocked_until = block_time
        
        else:
            blocked = self.block_model(ip=ip, blocked_until=block_time)
            db.session.add(blocked)

        db.session.commit()
        timer = int(block_time - datetime.now(timezone.utc).total_seconds())
        return redirect(url_for("auth.block", timer=timer))