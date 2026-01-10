from flask import request, redirect, url_for, jsonify
from datetime import datetime, timezone, timedelta
from flask_limiter.util import get_remote_address
from app.models.ip_crud import IpCRUD

class MiddleWare:
    def __init__(self):
        self.ip_crud = IpCRUD()

    @property
    def get_ip(self):
        return request.headers.get("X-Forwarded-For", get_remote_address())
    
    def check_ip(self):
        if request.endpoint in ["auth.block", "static", "auth.static"]:
            return None
    
        ip = self.get_ip
        
        blocked = self.ip_crud.get_blocked_ip(ip)
        
        if not blocked:
            return None

        if blocked.is_blocked:
            timer_fuso = blocked.blocked_until  
            if timer_fuso.tzinfo is None:
                timer_fuso = timer_fuso.replace(tzinfo=timezone.utc)

            delta = timer_fuso - datetime.now(timezone.utc)
            timer = max(0, int(delta.total_seconds()))
            
            if timer <= 0: 
                self.ip_crud.delete_blocked_ip(blocked)
                return None

            if "application/json" in request.headers.get("Accept"):
                return jsonify({
                "status": "error",
                "message": "Troppi tentativi, sei stato bloccato.",
                "redirect": url_for("auth.block", timer=timer)
                }), 429
            
            return redirect(url_for("auth.block", timer=timer))

        self.ip_crud.delete_blocked_ip(blocked)
        return None


    def limit_handler(self, e):
        ip = self.get_ip
        
        blocked = self.ip_crud.get_blocked_ip(ip)

        if blocked:
            self.ip_crud.update_blocked_ip(blocked)
            
        else:
            blocked = self.ip_crud.create_blocked_ip(ip)
            
        return jsonify({
        "status": "error",
        "message": "Troppi tentativi, sei stato bloccato.",
        "redirect": url_for("auth.block", timer=300)
        }), 429
    
    def validate_block(self):
        """
        Valida se l'ip è bloccato e restituisce il timer in caso positivo.
        """

        ip = self.get_ip
        blocked = self.ip_crud.get_blocked_ip(ip)

        if not blocked or not blocked.is_blocked:
            if blocked:
                self.ip_crud.delete_blocked_ip(blocked)

            return None
        
        timer_fuso = blocked.blocked_until.replace(tzinfo=timezone.utc)
        delta = timer_fuso - datetime.now(timezone.utc)
        return max(0, int(delta.total_seconds()))