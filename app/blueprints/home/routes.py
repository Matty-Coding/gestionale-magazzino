from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .forms import FornitoreForm, ProdottoForm, UtenteForm
from app.models.fornitore_crud import FornitoreCRUD
from app.models.prodotti_crud import ProdottoCrud
from app.models.user_crud import UserCRUD
from app.models.database import Prodotto
from app.utils.decorators import admin_required


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

            prodotti_fornitore = fornitore_obj.prodotti
            totale_prodotti = len(prodotti_fornitore)
            totale_pezzi = sum(fornitore_prodotto.prodotto.quantita for fornitore_prodotto in prodotti_fornitore)

            return render_template(
                "fornitore_dashboard.html", 
                form=form, 
                prodotti=prodotti_fornitore,
                totale_prodotti=totale_prodotti, 
                totale_pezzi=totale_pezzi
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


@home_bp.route("/prodotti")
def prodotti():
    pagina = request.args.get("page", 1, type=int)
    prodotti = Prodotto.query.paginate(page=pagina, per_page=5)

    if request.headers.get("Accept") == "application/json":
        return jsonify({
        "html": render_template("blocco-prodotti.html", prodotti=prodotti),
        "pagina_attuale": prodotti.page,
        "totale_pagine": prodotti.pages,
        "precedente": prodotti.prev_num,
        "successiva": prodotti.next_num 
    })

    return render_template("prodotti.html", prodotti=prodotti)


MANAGEMENT_CONFIG = {
    "prodotti": {
        "crud_get": prodottocrud.get_all_prodotti,
        "form_class": ProdottoForm,
        "template_table": "tabella-prodotti.html",
        "api_endpoint": "prodotto"
    },
    "utenti": {
        "crud_get": usercrud.get_all_users,
        "form_class": UtenteForm,
        "template_table": "tabella-utenti.html",
        "api_endpoint": "utente"    
    }
}

@home_bp.route("/admin/api/load/<resource_type>", methods=["GET"])
@login_required
@admin_required
def get_resource_data(resource_type):
    config = MANAGEMENT_CONFIG.get(resource_type)
    if not config:
        return jsonify({"status": "error", "message": "Risorsa non trovata"}), 404

    items = config["crud_get"]()
    
    form = config["form_class"]()

    table_html = render_template(config["template_table"], items=items)
    
    form_html = render_template("base-form.html", form=form)

    return jsonify({
        "status": "success",
        "table_html": table_html,
        "form_html": form_html,
        "endpoint": config["api_endpoint"] 
    })

@home_bp.route("/admin/management")
@login_required
@admin_required
def admin_management():
    return render_template("management.html")


# ==========================================
# =============  PRODOTTI  =================
# ==========================================
@home_bp.route("/admin/management/prodotto/aggiungi", methods=["POST"])
@login_required
@admin_required
def aggiungi_prodotto():
    data = request.get_json()
    form_prodotto = ProdottoForm(data=data)
    
    if form_prodotto.validate():
        if prodottocrud.get_prodotto(data.get("codice")):
            return jsonify({
                "status": "error", 
                "message": "Prodotto già presente"
                })
        
        prodottocrud.create_prodotto(
            codice=data.get("codice"),
            nome=data.get("nome"),
            descrizione=data.get("descrizione") or "Nessuna descrizione per questo prodotto",
            prezzo=float(data.get("prezzo")),
            quantita=int(data.get("quantita"))
        )
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": form_prodotto.errors})


@home_bp.route("/admin/management/prodotto/modifica/<int:prodotto_id>", methods=["POST"])
@login_required
@admin_required
def modifica_prodotto(prodotto_id):
    data = request.get_json()
    form_prodotto = ProdottoForm(data=data)
    
    if form_prodotto.validate():
        prodotto_obj = prodottocrud.get_prodotto_by_id(prodotto_id)
        prodottocrud.update_prodotto(
            prodotto=prodotto_obj,
            codice=data.get("codice"),
            nome=data.get("nome"),
            descrizione=data.get("descrizione") or "Nessuna descrizione per questo prodotto",
            prezzo=float(data.get("prezzo")),
            quantita=int(data.get("quantita"))
        )
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": form_prodotto.errors})
    

@home_bp.route("/admin/management/prodotto/elimina/<int:prodotto_id>", methods=["POST", "DELETE"])
@login_required
@admin_required
def elimina_prodotto(prodotto_id):
    prodotto_obj = prodottocrud.get_prodotto_by_id(prodotto_id)
    prodottocrud.delete_prodotto(prodotto=prodotto_obj)
    return jsonify({"status": "success"})



# ==========================================
# ==============  UTENTI  ==================
# ==========================================
