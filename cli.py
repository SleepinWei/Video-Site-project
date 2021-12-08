import logging
import click
from app.models import User
from app import db

def register(app):
    @app.cli.command("create_user")
    @click.argument("username")
    def create_user(username):
        user = User(name=username)
        db.session.add(user)
        db.session.commit()