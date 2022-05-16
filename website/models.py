# storage of database models
from pony.orm import Database, Required, Optional

db = Database()


class Namirnica(db.Entity):
    ime_namirnice = Required(str, unique=True)
    stanje_namirnice = Required(float)
    mjerna_jedinica = Required(str)
