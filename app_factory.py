from flask import Flask
from models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Get absolute path for database
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'crops.db'))
    
    # Configure SQLAlchemy with absolute path
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy without creating tables
    db.init_app(app)
    
    return app
