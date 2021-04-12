from flask_app import app
from app.commands.init_db import init_db

with app.app_context():
    init_db()