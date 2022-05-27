# storage of database models
from decimal import Decimal
from pony.orm import Database, PrimaryKey, Required, Optional, Set
from datetime import datetime
from pony.converting import str2datetime

db = Database()


class Namirnica(db.Entity):
    ime_namirnice = Required(str, unique=True)
    # Decimal jer se onda float racunanje vrsi optimalno;
    # sa decimal 1.1 + 2.2 nece biti 3.3000000000000003 nego 3.3
    stanje_namirnice = Required(Decimal)
    mjerna_jedinica = Required(str)
    normativ = Set('Normativ')


class Jelo(db.Entity):
    ime_jela = Required(str, unique=True)
    normativ = Set('Normativ')
    stavka_narudzbe = Set('Stavka')


class Normativ(db.Entity):
    jelo_id = Required(Jelo)
    namirnica_id = Required(Namirnica)
    kolicina_nam = Required(Decimal)


class Narudzba(db.Entity):
    id = PrimaryKey(int, auto=True)
    datum_kreiranja = Required(datetime)
    stavke = Set('Stavka')


class Stavka(db.Entity):
    # id = PrimaryKey(int, auto=True)
    narudzba_id = Required(Narudzba)
    jelo_id = Required(Jelo)
    kolicina = Required(int)
    PrimaryKey(narudzba_id, jelo_id)
