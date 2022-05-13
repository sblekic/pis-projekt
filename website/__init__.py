# this file makes the website folder a python package = i can use the import syntax
# every time i import the website folder it will run whatever is defined here
from flask import Flask


def create_app():
    app = Flask(__name__)  # __name__ references this file

    # registriram routes. podijelio sam rute u vise python datoteka pa ih moram negdje spajati
    # .views je shortcut za full path website.views. tocka oznacava current dir
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
