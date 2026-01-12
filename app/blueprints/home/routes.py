from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login import current_user, login_required
from .forms import FornitoreForm
from app.models.fornitore_crud import FornitoreCRUD
from app.models.prodotti_crud import ProdottoCrud
from app.models.user_crud import UserCRUD


home_bp = Blueprint(
    name="home",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/home/static",
    url_prefix="/"
)

usercrud = UserCRUD()
fornitorecrud = FornitoreCRUD()
prodottocrud = ProdottoCrud()

@home_bp.route("/")
def index():
    return render_template("index.html")


@home_bp.route("/dashboard")
@login_required
def dashboard():
    match current_user.ruolo:
        case "FORNITORE":
            fornitore_obj = fornitorecrud.get_fornitore(user_id=current_user.id)
            form = FornitoreForm(obj=fornitore_obj)
            prodotti = fornitore_obj.prodotti
            # totale_pezzi = sum(f for prodotto in prodotti)
            return render_template(
                "fornitore_dashboard.html", 
                form=form, 
                prodotti=prodotti, 
                # totale_pezzi=totale_pezzi
                )
        
        case "CLIENTE":
            prodotti = prodottocrud.get_all_prodotti()
            return render_template("cliente_dashboard.html", prodotti=prodotti)
        
        case "ADMIN":
            totale_utenti_per_ruolo = usercrud.get_users_by_role()
            ultimi_utenti = usercrud.last_users()
            prodotti_in_esaurimento = prodottocrud.prodotti_in_esaurimento()

            return render_template(
                "admin_dashboard.html", 
                totale_utenti_per_ruolo=totale_utenti_per_ruolo, 
                ultimi_utenti=ultimi_utenti, 
                prodotti_in_esaurimento=prodotti_in_esaurimento
                )


@home_bp.post("/update-fornitore-data")
@login_required
def update_fornitore_data():
    data = request.get_json()
    form = FornitoreForm(data=data)
    
    if not form.validate():
        return jsonify({"status": "error"})
    
    fornitore_obj = fornitorecrud.get_fornitore(user_id=current_user.id)
    
    if not fornitore_obj:
        fornitore_obj = fornitorecrud.create_fornitore(
            user=current_user,
            ragione_sociale=data.get("ragione_sociale"),
            partita_iva=data.get("partita_iva"),
            telefono=data.get("telefono")
        )
    
    else:
        fornitorecrud.update_fornitore(
            user_id=current_user.id,
            ragione_sociale=data.get("ragione_sociale"),
            partita_iva=data.get("partita_iva"),
            telefono=data.get("telefono")
        )
    
    return jsonify({"status": "success"})