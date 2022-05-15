# views/url endpoints
# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati
from flask import Blueprint, render_template, request, make_response
from .models import Namirnica
from pony import orm


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("dashboard.html")


@views.route('/namirnice', methods=['GET', 'POST'])
def namirnice():
    if request.method == 'POST':
        ime_namirnice = request.form.get('imeNamirnice')
        Namirnica(ime_namirnice=ime_namirnice)

    namirnica_db = orm.select(x for x in Namirnica)[:]
    # print(test.ime_namirnice)
    return render_template("namirnice.html", data=namirnica_db)
