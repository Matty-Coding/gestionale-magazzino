from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, current_app, Response
from flask_login import current_user, login_required
from .forms import FornitoreForm, ProdottoForm, UtenteForm, OrdineForm
from app.models.fornitore_crud import FornitoreCRUD
from app.models.prodotti_crud import ProdottoCrud
from app.models.user_crud import UserCRUD
from app.models.ordine_crud import OrdineCrud
from app.models.database import Prodotto, Categoria
from app.utils.decorators import admin_required
from app.services.mail_sender import send_email
from .cart import Cart
from stripe import PaymentIntent, StripeError, Webhook
from stripe.checkout import Session
from app.extensions import csrf


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
ordinecrud = OrdineCrud()

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
            
            cart = Cart()
            cart_data = session.get("cart", {})
            
            cart_items = []
            for prodotto_id, quantita in cart_data.items():
                prodotto = prodottocrud.get_prodotto_by_id(int(prodotto_id))
                cart_items.append({"prodotto": prodotto, "quantita": quantita})

            totale = cart.totale(item["prodotto"] for item in cart_items)

            return render_template("cliente_dashboard.html", prodotti=prodotti, cart=cart_items, totale=totale, numero_prodotti=len(cart))
        
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
    },
    "ordini": {
        "crud_get": ordinecrud.get_all_ordini,
        "form_class": OrdineForm,
        "template_table": "tabella-ordini.html",
        "api_endpoint": "ordine"
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
    categorie = Categoria.query.all()
    ordini = ("PENDING", "SHIPPED", "DELIVERED", "CANCELLED", "CONFIRMED")
    return render_template("management.html", categorie=categorie, ordini=ordini)


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
    

@home_bp.route("/admin/management/prodotto/elimina/<int:prodotto_id>", methods=["DELETE"])
@login_required
@admin_required
def elimina_prodotto(prodotto_id):
    prodotto_obj = prodottocrud.get_prodotto_by_id(prodotto_id)
    prodottocrud.delete_prodotto(prodotto=prodotto_obj)
    return jsonify({"status": "success"})

# ==========================================
# ==============  UTENTI  ==================
# ==========================================
@home_bp.route("/admin/management/utente/aggiungi", methods=["POST"])
@login_required
@admin_required
def aggiungi_utente():
    data = request.get_json()
    form_utente = UtenteForm(data=data)
    
    if form_utente.validate():
        user_obj = usercrud.get_user_by_email(data.get("email"))
        if user_obj:
            return jsonify({
                "status": "error",
                "message": "Utente già presente"
            })
        
        usercrud.create_user(
            username = data.get("username"),
            email = data.get("email"),
            password = data.get("password"),
            ruolo = data.get("ruolo"),
            verificato = bool(data.get("verificato"))
        )

        send_email(
            email=data.get("email"),
            subject=f"Il tuo account è stato creato da un amministratore con il ruolo {data.get('ruolo')}!",
            message=f"<h2>Suggeriamo di cambiare subito le credenziali appena effettuato il primo login!</h2><p><strong>Username:</strong> {data.get('username')}<br><strong>Email:</strong> {data.get('email')}<br><strong>Password:</strong> {data.get('password')}</p>"
        )       

        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": form_utente.errors})

@home_bp.route("/admin/management/utente/modifica/<int:id>", methods=["POST"])
@login_required
@admin_required
def modifica_utente(id):
    data = request.get_json()
    
    user_obj = usercrud.get_user(id)
    usercrud.toggle_verification(user=user_obj, verificato=bool(data.get("verificato")))
    
    if bool(data.get("verificato")):
        send_email(
            email=data.get("email"),
            subject="Richiesta autenticazione account completata",
            message=f"<h2>La richiesta di autenticazione per il tuo account è stata completata!</h2><br><p>Ora sei verificato e puoi quindi accedere al tuo account.</p>"
        )

    return jsonify({"status": "success"})

@home_bp.route("/admin/management/utente/elimina/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def elimina_utente(id):
    user_obj = usercrud.get_user(id)
    
    send_email(
        email=user_obj.email,
        subject="Richiesta di eliminazione account completata",
        message=f"<h2>La richiesta di eliminazione per il tuo account è stata completata!</h2><br><p>Il tuo account è stato eliminato.</p>"
    )
    usercrud.delete_user(user=user_obj)

    return jsonify({"status": "success"})


# ==========================================
# =============  CARRELLO  =================
# ==========================================
def get_cart_render_data():
    """
    Restituisce rendering del carrello e la quantita di prodotti presenti
    """
    cart = Cart()
    cart_data = session.get("cart", {})
    cart_items = []
    for prodotto_id, quantita in cart_data.items():
        prodotto = prodottocrud.get_prodotto_by_id(int(prodotto_id))
        if prodotto: 
            cart_items.append({"prodotto": prodotto, "quantita": quantita})

    lista_prodotti = [item["prodotto"] for item in cart_items]
    totale = cart.totale(lista_prodotti)
    html = render_template("blocco-carrello.html", cart=cart_items, totale=totale)
    return html, len(cart)


@home_bp.route("/carrello/aggiungi/<int:prodotto_id>", methods=["POST"])
@login_required
def aggiungi_al_carrello(prodotto_id):
    cart = Cart()
    cart.aggiungi(prodotto_id=prodotto_id)
    html, conta_prodotti = get_cart_render_data()

    return jsonify({
        "status": "success",
        "html": html,
        "conta_prodotti": conta_prodotti
    })


@home_bp.route("/carrello/elimina/<int:prodotto_id>", methods=["POST"])
@login_required
def rimuovi_dal_carrello(prodotto_id):
    cart = Cart()
    cart.rimuovi(prodotto_id=prodotto_id)
    html, conta_prodotti = get_cart_render_data()

    return jsonify({
        "status": "success",
        "html": html,
        "conta_prodotti": conta_prodotti
    })


@home_bp.route("/carrello/modifica/<int:prodotto_id>", methods=["POST"])
@login_required
def modifica_quantita(prodotto_id):
    cart = Cart()
    data = request.get_json()
    cart.modifica_quantita(prodotto_id=prodotto_id, quantita=int(data.get("quantita")))
    html, conta_prodotti = get_cart_render_data()

    return jsonify({
        "status": "success",
        "html": html,
        "conta_prodotti": conta_prodotti
    })


@home_bp.route("/carrello/svuota", methods=["POST"])
@login_required
def svuota_carrello():
    cart = Cart()
    cart.svuota()
    html, conta_prodotti = get_cart_render_data()

    return jsonify({
        "status": "success",
        "html": html,
        "conta_prodotti": conta_prodotti
    })  


@home_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = Cart()
    cart_data = session.get("cart", {})

    nuovo_ordine = ordinecrud.create_ordine(cliente_id=current_user.id)
    
    cart_items = []
    
    prodotti_html = "<ul>" 
    
    for prodotto_id, quantita in cart_data.items():
        prodotto = prodottocrud.get_prodotto_by_id(int(prodotto_id))
        if prodotto: 
            cart_items.append(prodotto)
            
            ordinecrud.create_dettagli_ordine(
                ordine_id=nuovo_ordine.id,
                prodotto_id=prodotto.id,
                quantita=quantita,
                prezzo_unitario=prodotto.prezzo
            )

            prodotti_html += f"<li>{prodotto.nome} - Quantità: {quantita} - Prezzo: {prodotto.prezzo}€</li>"

    prodotti_html += "</ul>" 

    ordine_totale = cart.totale(cart_items)
    ordinecrud.update_ordine(ordine=nuovo_ordine, totale=ordine_totale)

    send_email(
        email = current_user.email,
        subject ="Il tuo ordine è stato registrato correttamente",
        message = f"""
            <h2>Il tuo ordine #{nuovo_ordine.id} è stato registrato correttamente.</h2>
            <p>Riceverai ulteriori email di aggiornamento sullo stato del tuo ordine.</p>
            <br>
            <h3>Riepilogo prodotti:</h3>
            {prodotti_html}
            <br>
            <p><strong>Stato:</strong> {nuovo_ordine.stato}</p>
            <p><strong>Totale pagato:</strong> {ordine_totale}€</p>
        """
    )

    cart.svuota()
    html, conta_prodotti = get_cart_render_data()

    return jsonify({
        "status": "success", 
        "message": f"Ordine {nuovo_ordine.id} creato con successo",
        "html": html,
        "conta_prodotti": conta_prodotti,
        "ordine_id": nuovo_ordine.id
    })    

@home_bp.route("/miei-ordini")
@login_required
def miei_ordini():
    ordini = ordinecrud.get_ordini_by_cliente_id(cliente_id=current_user.id)
    return render_template("miei-ordini.html", ordini=ordini)


# ===============================================
# ===========  ADMIN PANEL ORDINI  ==============
# ===============================================

def genera_riepilogo_ordine(ordine):
    """
    Genera un riepilogo dell'ordine in HTML leggibile, 
    iterando su tutti i prodotti presenti nei dettagli.
    """
    
    html_segments = [
        f"<h3>Dettagli Ordine #{ordine.id}</h3>",
        "<table style='width: 100%; border-collapse: collapse;'>",
        "<thead>",
        "<tr style='border-bottom: 1px solid #ddd; text-align: left;'>",
        "<th style='padding: 8px;'>Prodotto</th>",
        "<th style='padding: 8px;'>Quantità</th>",
        "<th style='padding: 8px;'>Prezzo Unitario</th>",
        "</tr>",
        "</thead>",
        "<tbody>"
    ]

    for item in ordine.dettagli:
        row = f"""
            <tr style='border-bottom: 1px solid #eee;'>
                <td style='padding: 8px;'><strong>{item.prodotto.nome}</strong></td>
                <td style='padding: 8px;'>{item.quantita}</td>
                <td style='padding: 8px;'>{item.prezzo_unitario}€</td>
            </tr>
        """
        html_segments.append(row)

    html_segments.append("</tbody></table>")
    html_segments.append(f"<p style='font-size: 18px;'><strong>Totale complessivo: {ordine.totale}€</strong></p>")

    return "".join(html_segments)

@home_bp.route("/admin/management/ordine/modifica/<int:id>", methods=["POST"])
@login_required
@admin_required
def modifica_ordine(id):
    data = request.get_json()
    ordine = ordinecrud.get_ordine_by_id(ordine_id=id)

    nuovo_stato = data.get("stato")
    nuovo_ordine = ordinecrud.update_stato(ordine_id=id, stato=nuovo_stato)

    riepilogo = genera_riepilogo_ordine(ordine=nuovo_ordine)

    send_email(
        email = ordine.cliente.email,
        subject = f"Aggiornamento Ordine #{ordine.id}: {ordine.stato}",
        message = f"""
            <h2>Il tuo ordine è stato aggiornato!</h2>
            <p>Il nuovo stato è: <strong>{ordine.stato}</strong></p>
            <hr>
            {riepilogo}
            <p>Grazie per aver scelto il nostro servizio.</p>
        """
        )
    return jsonify({"status": "success"})


@home_bp.route("/admin/management/ordine/elimina/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def elimina_ordine(id):
    ordine = ordinecrud.get_ordine_by_id(ordine_id=id)

    riepilogo = genera_riepilogo_ordine(ordine=ordine)

    send_email(
        email = ordine.cliente.email,
        subject = f"Aggiornamento Ordine #{ordine.id}: Annullato",
        message = f"""
            <h2>Il tuo ordine è stato aggiornato!</h2>
            <p>Il nuovo stato è: <strong>ANNULLATO</strong></p>
            <hr>
            {riepilogo}
            <p>Grazie per aver scelto il nostro servizio.</p>
        """
        )
    
    ordinecrud.elimina_ordine(ordine_id=id)
    return jsonify({"status": "success"})

# ===========================================
# ===========  Stripe Checkout  =============                                      
# ===========================================
@home_bp.route("/test-stripe")
def test_stripe():
    try:
        intent = PaymentIntent.create(
            amount=1000,
            currency="eur"
        )

        return jsonify({"status": "success", "client_secret": intent.client_secret})
    
    except StripeError as e:
        return jsonify({"status": "error", "message": str(e)})
    

@home_bp.route("pagamento/<int:ordine_id>")
@login_required
def pagamento(ordine_id):
    ordine = ordinecrud.get_ordine_by_id(ordine_id=ordine_id)
    if ordine.cliente.id != current_user.id:
        return redirect(url_for("home.index"))

    if ordine.stato != "PENDING":
        return redirect(url_for("home.miei_ordini"))

    line_items = []
    for dettaglio in ordine.dettagli:
        line_items.append({
            "price_data": {
                "currency": "eur",
                "unit_amount": int(dettaglio.prezzo_unitario * 100),
                "product_data": {"name": dettaglio.prodotto.nome}
            },
            "quantity": dettaglio.quantita
        })

    session = Session.create(
        payment_method_types = ["card"],
        line_items = line_items,
        mode = "payment",
        success_url = url_for("home.pagamento_accettato", ordine_id=ordine_id, _external=True),
        cancel_url = url_for("home.pagamento_rifiutato", ordine_id=ordine_id, _external=True),
        metadata={"ordine_id": ordine.id}
    )

    return redirect(session.url)

@home_bp.route("/pagamento-accettato/<int:ordine_id>")
@login_required
def pagamento_accettato(ordine_id):
    ordine = ordinecrud.get_ordine_by_id(ordine_id=ordine_id)
    if ordine.cliente.id != current_user.id:
        return redirect(url_for("home.index"))
    
    flash("Pagamento completato con successo! Stiamo elaborando il tuo ordine.", "success")
    return redirect(url_for("home.miei_ordini"))

@home_bp.route("/pagamento-rifiutato/<int:ordine_id>")
@login_required
def pagamento_rifiutato(ordine_id):
    ordine = ordinecrud.get_ordine_by_id(ordine_id=ordine_id)
    if ordine.cliente.id != current_user.id:
        return redirect(url_for("home.index"))
    
    flash("Pagamento rifiutato! Riprova più tardi.", "error")
    return redirect(url_for("home.miei_ordini"))

@csrf.exempt
@home_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    signature_header = request.headers.get("Stripe-Signature")
    endpoint_secret = current_app.config["STRIPE_WEBHOOK_SECRET"]

    try:
        event = Webhook.construct_event(
            payload=payload,
            sig_header=signature_header,
            secret=endpoint_secret
        )

    except:
        return jsonify({"status": "error", "message": "Invalid signature"}), 

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        ordine_id = session["metadata"]["ordine_id"]

        if ordine_id:
            ordine = ordinecrud.update_stato(ordine_id=ordine_id, stato="COMPLETATO")

            html = genera_riepilogo_ordine(ordine=ordine)
            send_email(
                email = ordinecrud.get_ordine_by_id(ordine_id=ordine_id).cliente.email,
                subject = f"Aggiornamento Ordine #{ordine_id}: Completato",
                message = f"""
                    <h2>Il tuo ordine è stato aggiornato!</h2>
                    {html}
                    <br>
                    <p>Riceverai ulteriori informazioni riguardo la spedizione e la consegna.</p>
                    <p>Grazie per aver scelto il nostro servizio.</p>
                """
                )

    return Response(status=200)