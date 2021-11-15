from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/app.db"
    
    db.init_app(app)
    migrate.init_app(app, db)
    from .models import Task
    with app.app_context():
        db.create_all()
    
    from application.models import Task

    from application.task import task_api_bp

    app.register_blueprint(task_api_bp, url_prefix="/task")

    return app