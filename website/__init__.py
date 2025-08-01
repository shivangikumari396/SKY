from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, random

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    random.seed(0)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Better to set it False for performance
    db.init_app(app)

    from .views import views
    from .prediction import prediction
    from .messages import messages

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(prediction, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')

    from .models import Messages

    create_database(app)

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):   # <-- remove 'website/' from the path
        with app.app_context():
            db.create_all()
        print('✅ Database created successfully!')
