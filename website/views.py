# views/url endpoints
# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati
from flask import Blueprint, redirect, render_template, request, make_response, jsonify, url_for
from .models import *
from .procedures import get_jela, get_jelo_by_id
from pony import orm
import json
from decimal import Decimal

views = Blueprint('views', __name__)


@views.route('/chartJs')
def chart_js():
    # testiram vizualizaciju iz chartjs-a
    x = ['assigned', 'closed', 'new']
    y = [4, 7, 11]
    z = 69
    return render_template("chart-js.html", x=x, y=y, z=z)


@views.route('/')
def home():
    # za sada koristim za testiranje
    return render_template("dashboard.html")


@views.route('/namirnice', methods=['GET'])
def namirnice():
    # prikaz namirnica. sortirano abecedno po imenu
    # Jelo(ime_jela="rizoto")
    namirnica_db = orm.select(x for x in Namirnica).order_by(
        Namirnica.ime_namirnice)[:]
    return render_template("namirnice.html", namirnice=namirnica_db)


@views.route('/namirnice/dodaj-nam', methods=['POST'])
def dodaj_nam():
    if request.method == 'POST':
        ime_nam = request.form.get('imeNamirnice')
        stanje_nam = request.form.get('stanjeNam')
        mjerna_jed = request.form.get('mjernaJed')
        Namirnica(ime_namirnice=ime_nam, stanje_namirnice=stanje_nam,
                  mjerna_jedinica=mjerna_jed)
    return redirect(url_for(".namirnice"))


@views.route('/namirnice/izbrisi-nam', methods=['DELETE'])
def izbrisi_nam():
    # iz js funkcije dobio json string kojeg moram prvo dekodirati kako bih ga mogao spremiti u varijablu i koristiti
    namirnica = json.loads(request.data)
    nam_id = namirnica["namId"]

    # provjera ako id postoji u db
    if Namirnica[nam_id]:
        Namirnica[nam_id].delete()
    return jsonify({})


@views.route('/namirnice/update-nam/<int:nam_id>', methods=['POST'])
def update_nam(nam_id):
    dodaj_na_zal = request.form.get('novoStanje')
    Namirnica[nam_id].stanje_namirnice += Decimal(dodaj_na_zal)
    return redirect(url_for(".namirnice"))


@views.route('/normativi', methods=['GET'])
def normativi():
    jela = get_jela()
    return render_template("normativi.html", jela=jela)


@views.route('/dodaj-jelo', methods=['POST'])
def dodaj_jelo():
    ime_jela = request.form.get('imeJela')
    is_jelo = Jelo.select(lambda x: x.ime_jela == ime_jela)[:]
    if not is_jelo:
        Jelo(ime_jela=ime_jela)
    id_jela = Jelo.select(lambda x: x.ime_jela == ime_jela)[:][0].id
    return redirect(f'/normativi/jelo/{id_jela}')


@views.route('/normativi/jelo/<int:jelo_id>', methods=['GET'])
def normativ_form(jelo_id):
    # prikaz "dinamicke" forme

    namirnica_db = orm.select(x for x in Namirnica).order_by(
        Namirnica.ime_namirnice)[:]
    trazeni_el = get_jelo_by_id(jelo_id)
    return render_template("normativi-dodaj.html", namirnice=namirnica_db, jelo=trazeni_el)


@views.route("/normativi/dodaj/<int:jelo_id>", methods=['POST'])
def dodaj_normativ(jelo_id):
    # preko imena dohvacam id namirnice
    ime_nam = request.form.get('imeNam')
    kol_nam = request.form.get('kolNam')
    id_nam = db.get(
        "select id from Namirnica where ime_namirnice = $ime_nam")
    Normativ(jelo_id=jelo_id, namirnica_id=id_nam, kolicina_nam=kol_nam)
    return redirect(f'/normativi/jelo/{jelo_id}')
