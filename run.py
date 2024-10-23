# run.py
from app import create_app
from flask_migrate import Migrate
from app.extensions import db

app = create_app()
migrate = Migrate(app, db)
