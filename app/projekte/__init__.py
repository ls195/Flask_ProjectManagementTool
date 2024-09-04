from flask import Blueprint


projekte_routes = Blueprint('projekte_routes', __name__, template_folder = 'templates')                                        # Blueprint-Object namens 'projekte_routes' erstellt

from app.projekte import routes