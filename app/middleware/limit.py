from flask import request, redirect, url_for, jsonify
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

        if blocked.is_blocked:
            timer_fuso = blocked.blocked_until  
            if timer_fuso.tzinfo is None:
                timer_fuso = timer_fuso.replace(tzinfo=timezone.utc)

            delta = timer_fuso - datetime.now(timezone.utc)
            timer = max(0, int(delta.total_seconds()))
            
            # RIVEDERE
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.headers.get("Accept") == "application/json":
                return jsonify({
                "status": "error",
                "redirect": url_for("auth.block", timer=timer)
                }), 429
            
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
            blocked = IpBloccati(ip=ip, blocked_until=block_time)
            db.session.add(blocked)

        db.session.commit()
        
        return jsonify({
        "status": "error",
        "message": "Troppi tentativi, sei stato bloccato.",
        "redirect": url_for("auth.block", timer=300)
        }), 429