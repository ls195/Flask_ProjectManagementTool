from flask import Blueprint


tasks_routes = Blueprint('tasks_routes', __name__, template_folder='templates')                                        # Blueprint-Object namens 'projekte_routes' erstellt

from app.tasks import routes