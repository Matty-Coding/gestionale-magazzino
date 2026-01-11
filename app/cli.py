import click
from flask_migrate import downgrade, upgrade

# comando per creare l'admin
@click.command("create-admin")
def create_admin_command():
    from app.services.user import create_admin
    create_admin()

# comando per generare dati fittizi
@click.command("fake-data")
def fake_data_command():
    from app.test.fake_data import generate_fake_data
    generate_fake_data()  

# comando per resettare il database e generare dati fittizi
@click.command("reset-db")
def reset_db_command():
    downgrade(revision="base")
    upgrade(revision="head")

    from app.test.fake_data import generate_fake_data
    generate_fake_data()