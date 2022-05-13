# views/url endpoints
from flask import Blueprint, render_template, request

# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("dashboard.html")


@views.route('/namirnice', methods=['GET', 'POST'])
def namirnice():
    if request.method == 'POST':
        ime_namirnice = request.form.get('imeNamirnice')
        print(ime_namirnice)
    return render_template("namirnice.html")
