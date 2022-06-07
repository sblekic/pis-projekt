# views/url endpoints
# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati
from flask import Blueprint, redirect, render_template, request, make_response, jsonify, url_for, flash
from .models import *
from .procedures import *
from pony import orm
import json
from decimal import Decimal

views = Blueprint('views', __name__)


@views.route('/')
def chart_js():
    nam_db = orm.select(x for x in Namirnica)[:]
    labels = []
    values = []
    for nam in nam_db:
        labels.append(nam.ime_namirnice)
        values.append(float(nam.stanje_namirnice))
    return render_template("chart-js.html", labels_db=labels, values_db=values)


@views.route('/namirnice', methods=['GET'])
def namirnice():
    # prikaz namirnica. sortirano abecedno po imenu
    namirnica_db = orm.select(x for x in Namirnica).order_by(
        Namirnica.ime_namirnice)[:]
    mj = mjerne_jedinice
    return render_template("namirnice.html", namirnice=namirnica_db, mj=mj)


@views.route('/namirnice/dodaj-nam', methods=['POST'])
def dodaj_nam():
    if request.method == 'POST':
        ime_nam = request.form.get('imeNamirnice')
        stanje_nam = request.form.get('stanjeNam')
        mjerna_jed = request.form.get('mjernaJed')
        Namirnica(ime_namirnice=ime_nam.lower(), stanje_namirnice=stanje_nam,
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
    ime_jela = ime_jela.capitalize()
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


@views.route("/narudzbe")
def narudzbe():
    narudzbe = get_narudzbe()
    print("\n", narudzbe)
    return render_template("narudzbe.html", narudzbe=narudzbe)


@views.route("/narudzbe/dolazne", methods=['POST'])
def in_narudzbe():
    json_request = request.get_json()
    kupac = json_request["kupac"]
    kontakt = json_request["kontakt"]
    datum = json_request["datum"]
    status = json_request["status"]
    Narudzba(kupac=kupac, kontakt=kontakt,
             datum_kreiranja=datum, status=status)
    return jsonify("Success")


@views.route("/narudzbe/<int:narudzba_id>", methods=['GET', 'POST'])
def detalji_narudzbe(narudzba_id):
    narudzba = get_narudzba_by_id(narudzba_id)
    nabava = nabavna_lista_by_narudzba(narudzba)

    if request.method == 'POST':
        no_nam = False
        for nam in nabava:
            nam_id = nam["nam_id"]
            rez = Namirnica[nam_id].stanje_namirnice - nam["kolicina"]
            # negativan rezultat mi oznacava manjak nam, dakle zaliha se postavlja na nulu
            # a nam koja mi fali se dodaje u listu nam za nabavu
            if rez < 0:
                no_nam = True
                Namirnica[nam_id].stanje_namirnice = Decimal("0")
                if find_nabava_el(nam_id):
                    # zaokruzim na int jer necu kupiti 2.5 komada necega
                    Nabava[nam_id].kolicina += round(abs(rez))
                else:
                    Nabava(nam_id=nam_id, kolicina=round(abs(rez)))
            # ako je rezultat pozitivan oduzmi sa skladista
            else:
                Namirnica[nam_id].stanje_namirnice = rez
        if(no_nam):
            flash("Nedovoljno namirnica na stanju, potreban iznos ",
                  category="warning")
        else:
            flash("Narudzba zaprimljena!", category="success")
        Narudzba[narudzba_id].status = zaprimljeno
        return redirect(f"/narudzbe/{narudzba_id}")
    return render_template("detalji-narudzbe.html", narudzba=narudzba, nabava=nabava)


@views.route("nabava", methods=['GET'])
def get_nabava():
    nabava_nam = orm.select(x for x in Nabava)[:]
    return render_template("nabava.html", nabava_nam=nabava_nam)


@views.route("narudzbenice", methods=['GET'])
def narudzbenice():
    nam = orm.select(x for x in Nabava)[:]
    dobavljaci = orm.select(x for x in Dobavljac)[:]
    return render_template("narudzbenice.html", nam=nam, dob=dobavljaci)


@views.route("narudzbenice/cijena", methods=['POST'])
def get_cijena():
    identifiers = json.loads(request.data)
    nam_id = int(identifiers["namId"])
    dob_id = int(identifiers["dobId"])
    index = identifiers["index"]  # vjerojatno nepotrebno ovdje

    cijena = orm.select(x.cijena for x in Katalog if x.dobavljac.id ==
                        dob_id and x.namirnica.id == nam_id)[:][0]

    return jsonify({'nam': nam_id, "dob": dob_id, "index": index, "cijena": cijena})


@views.route("narudzbenice/pdf", methods=['GET', 'POST'])
def create_pdf():
    # elementi imaju isti name pa mi treba polje sa vrijednostima
    pdf = request.form.to_dict(flat=False)

    lista_stavki = []

    for stavka in range(len(pdf["nam"])):
        nd = {}
        nd["id"] = stavka + 1
        nd["nam"] = pdf["nam"][stavka]
        nd["kol"] = pdf["kolicina"][stavka]
        nd["mj"] = pdf["mj"][stavka]
        nd["dob"] = Dobavljac[pdf["dobavljac"][stavka]].naziv
        nd["cij"] = pdf["cijena"][stavka]
        kol = Decimal(f'{pdf["kolicina"][stavka]}')
        cijena = Decimal(f'{ pdf["cijena"][stavka]}')
        nd["tot"] = round(cijena * kol, 2)
        lista_stavki.append(nd)

    ukupni_iznos = 0
    for stavka in lista_stavki:
        cijena = Decimal(f'{stavka["tot"]}')
        ukupni_iznos += cijena
    return render_template("print-pdf.html", pdf=lista_stavki, tot=ukupni_iznos)
