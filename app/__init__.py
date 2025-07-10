import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# inicializace DB

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'db.sqlite3')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# vytvoření adresáře instance a DB při prvním spuštění
try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    pass

from . import routes, models

with app.app_context():
    db.create_all()
    models.create_test_data()
