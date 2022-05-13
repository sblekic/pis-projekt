# views/url endpoints
from flask import Blueprint, render_template

# blueprint mi omogucava podjelu route-ova u više datoteka, da ne moram sve ovdje natrpati

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("dashboard.html")


@views.route('/namirnice')
def namirnice():
    return render_template("namirnice.html")
