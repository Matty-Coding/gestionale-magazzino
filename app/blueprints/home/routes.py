from flask import Blueprint, render_template

home_bp = Blueprint(
    name="home",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/"
)


@home_bp.route("/")
def home():
    return render_template("home.html")