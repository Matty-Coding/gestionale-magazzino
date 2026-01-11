import click

@click.command("create-admin")
def create_admin_command():
    from app.services.user import create_admin
    create_admin()