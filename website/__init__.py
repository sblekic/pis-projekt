# this file makes the website folder a python package = i can use the import syntax
# every time i import the website folder it will run whatever is defined here
from flask import Flask
from .models import db
from pony.flask import Pony


def create_app():
    app = Flask(__name__)  # __name__ references this file
    # flask integration. ako ovo napravim ne moram wrappat views u @db_session
    Pony(app)
    # registriram routes. podijelio sam rute u vise python datoteka pa ih moram negdje spajati
    # .views je shortcut za full path website.views. tocka oznacava current dir
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    db.bind(provider='sqlite', filename='baza_podataka.sqlite', create_db=True)
    # orm.set_sql_debug(True)
    db.generate_mapping(create_tables=True)
    return app
