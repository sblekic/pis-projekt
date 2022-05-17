# views/url endpoints
# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati
from flask import Blueprint, render_template, request, make_response, jsonify
from .models import Namirnica
from pony import orm
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("dashboard.html")


@views.route('/namirnice', methods=['GET', 'POST'])
def namirnice():
    if request.method == 'POST':
        ime_nam = request.form.get('imeNamirnice')
        stanje_nam = request.form.get('stanjeNam')
        mjerna_jed = request.form.get('mjernaJed')
        Namirnica(ime_namirnice=ime_nam, stanje_namirnice=stanje_nam,
                  mjerna_jedinica=mjerna_jed)

    # prikaz namirnica. sortirano abecedno po imenu
    namirnica_db = orm.select(x for x in Namirnica).order_by(
        Namirnica.ime_namirnice)[:]
    # print(test.ime_namirnice)
    return render_template("namirnice.html", namirnice=namirnica_db)


@views.route('/izbrisi-nam', methods=['DELETE'])
def izbrisi_nam():
    # iz js funkcije dobio json string kojeg moram prvo dekodirati kako bih ga mogao spremiti u varijablu i koristiti
    namirnica = json.loads(request.data)
    nam_id = namirnica["namId"]

    # provjera ako id postoji u db
    if Namirnica[nam_id]:
        Namirnica[nam_id].delete()
    return jsonify({})
