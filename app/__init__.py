from flask import Flask
from app.main import main_routes
from app.projekte import projekte_routes
from app.tasks import tasks_routes
from app.mitarbeiter.routes import mitarbeiter_routes
from app.database import create_database

def create_app():
    app = Flask(__name__)
    create_database()
    app.register_blueprint(main_routes)
    app.register_blueprint(projekte_routes, url_prefix="/projekte")
    app.register_blueprint(tasks_routes, url_prefix = "/tasks")
    app.register_blueprint(mitarbeiter_routes, url_prefix = "/mitarbeiter")
    return app
