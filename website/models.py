# storage of database models
from decimal import Decimal
from pony.orm import Database, Required, Optional, Set

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


class Normativ(db.Entity):
    jelo_id = Required(Jelo)
    namirnica_id = Required(Namirnica, unique=True)
    kolicina_nam = Required(Decimal)
