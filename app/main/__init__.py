
from flask import Blueprint


main_routes = Blueprint('main_routes', __name__, template_folder = 'templates')  
                                                                                                                        # Blueprint-Object namens 'main_routes' erstellt
                                                                                                                        # der zusatz template_folder = "templates" war elementar, da sonst imemr nach dem ordenr app/tempaltes gesucht wurde und die datei niocht gefunden wurde


from app.main import routes