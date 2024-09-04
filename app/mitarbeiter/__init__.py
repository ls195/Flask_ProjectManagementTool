from flask import Blueprint


mitarbeiter_routes = Blueprint('mitarbeiter_routes', __name__, template_folder = 'templates')                                        # Blueprint-Object namens 'main_routes' erstellt   
from app.mitarbeiter import routes