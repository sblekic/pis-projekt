# storage of database models
from decimal import Decimal, getcontext
from pony.orm import Database, PrimaryKey, Required, Optional, Set, composite_key, db_session
from datetime import datetime
from pony.converting import str2datetime
import random

db = Database()


class Namirnica(db.Entity):
    ime_namirnice = Required(str, unique=True)
    # Decimal jer se onda float racunanje vrsi optimalno;
    # sa decimal 1.1 + 2.2 nece biti 3.3000000000000003 nego 3.3
    stanje_namirnice = Required(Decimal)
    mjerna_jedinica = Required(str)
    normativ = Set('Normativ')
    nabava = Optional('Nabava')
    katalog = Set('Katalog')


class Jelo(db.Entity):
    ime_jela = Required(str, unique=True)
    normativ = Set('Normativ')
    stavka_narudzbe = Set('Stavka')


class Normativ(db.Entity):
    id = PrimaryKey(int, auto=True)
    jelo_id = Required(Jelo)
    namirnica_id = Required(Namirnica)
    kolicina_nam = Required(Decimal, scale=3)
    # na istom jelu ne smijem imati duplikat namirnice
    composite_key(namirnica_id, jelo_id)


class Narudzba(db.Entity):
    id = PrimaryKey(int, auto=True)
    kupac = Required(str)
    kontakt = Required(str)
    datum_kreiranja = Required(datetime)
    status = Required(str)
    stavke = Set('Stavka')


class Stavka(db.Entity):
    # id = PrimaryKey(int, auto=True)
    narudzba_id = Required(Narudzba)
    jelo_id = Required(Jelo)
    kolicina = Required(int)
    PrimaryKey(narudzba_id, jelo_id)


class Nabava(db.Entity):
    nam_id = PrimaryKey(Namirnica)
    kolicina = Required(Decimal)


class Katalog(db.Entity):
    id = PrimaryKey(int, auto=True)
    dobavljac = Required('Dobavljac')
    namirnica = Required(Namirnica)
    cijena = Required(Decimal)
    composite_key(dobavljac, namirnica)


class Dobavljac(db.Entity):
    id = PrimaryKey(int, auto=True)
    katalog = Set(Katalog)
    naziv = Required(str)


# status narudzbe
novo = 'Novo'
zaprimljeno = 'Zaprimljeno'
izvrseno = 'Izvrseno'
otkazano = 'Otkazano'

mjerne_jedinice = ["kg", "kom", "l"]


@db_session
def populate_database():
    lista_nam = ["teleca prsa", "svinjski but", "teleca lopatica", "celer", "mrkva", "grasak", "riza", "svinjski kare",
                 "svinjska rebra", "sol", "papar", "vegeta", "rajcica", "muskatni orascic", "tuna",
                 "brancin", "parmezan", "svinjsko mljeveno meso", "junece mljeveno meso", "jaja",
                 "maslinovo ulje", "gljiva"]

    for nam in lista_nam:
        Namirnica(ime_namirnice=f"{nam}",
                  stanje_namirnice=Decimal(f'{round(random.uniform(2, 10))}'), mjerna_jedinica=f"{mjerne_jedinice[round(random.uniform(0,2))]}")

    lista_jela = ["Krem juha od gljiva", "Dalmatinska goveda juha", "Lazanje", "Punjena teleca prsa",
                  "Pasta carbonara", "Dagnje na buzaru", "Lignje na zaru", "Tortilje s piletinom",
                  "Svinjski gulas", "Pecena janjetina", "Cokoladni muffini", "Tiramisu"]

    for jelo in lista_jela:
        Jelo(ime_jela=f"{jelo}")

    for jelo in range(1, len(lista_jela)+1):
        nam = list(range(1, len(lista_nam)+1))
        random.shuffle(nam)
        for x in range(8):
            Normativ(jelo_id=Jelo[jelo], namirnica_id=Namirnica[nam.pop()], kolicina_nam=Decimal(
                f'{round(random.uniform(0.04, 1), 3)}'))


# n1 = Narudzba(datum_kreiranja=str2datetime(
#     '2013-03-15 23:15:00'), status=novo)
# s1 = Stavka(narudzba_id=n1, jelo_id=j1, kolicina=2)
# s1 = Stavka(narudzba_id=n1, jelo_id=j2, kolicina=3)
