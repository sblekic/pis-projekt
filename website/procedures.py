from .models import *
from pony import orm


def get_jela():
    # putem to dict raspakiram m:m tablica kako bih imao vrijednosti umjesto fk
    jela = orm.select(x for x in Jelo)
    jela = [jelo.to_dict(with_collections=True, related_objects=True)
            for jelo in jela]

    for jelo in jela:
        jelo["normativ"] = [normativ.to_dict(
            only=["id", "namirnica_id", "kolicina_nam"], with_collections=True, related_objects=True) for normativ in jelo["normativ"]]

    for jelo in jela:
        for normativ in jelo["normativ"]:
            nam_details = normativ["namirnica_id"].to_dict()
            normativ["namirnica_id"] = nam_details["id"]
            normativ["mjerna_jedinica"] = nam_details["mjerna_jedinica"]
            normativ["ime_namirnice"] = nam_details["ime_namirnice"]
    return jela


def get_jelo_by_id(jelo_id):
    jela = orm.select(x for x in Jelo)
    jela = [jelo.to_dict(with_collections=True, related_objects=True)
            for jelo in jela]

    for jelo in jela:
        jelo["normativ"] = [normativ.to_dict(
            only=["id", "namirnica_id", "kolicina_nam"], with_collections=True, related_objects=True) for normativ in jelo["normativ"]]

    for jelo in jela:
        for normativ in jelo["normativ"]:
            # print(normativ["namirnica_id"])
            nam_details = normativ["namirnica_id"].to_dict()
            # print(nam_details)
            normativ["namirnica_id"] = nam_details["id"]
            normativ["mjerna_jedinica"] = nam_details["mjerna_jedinica"]
            normativ["ime_namirnice"] = nam_details["ime_namirnice"]

    trazeni_el = [element for element in jela if element["id"] == jelo_id]
    return trazeni_el
