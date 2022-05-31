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
    jela = get_jela()
    trazeni_el = [element for element in jela if element["id"] == jelo_id][0]
    return trazeni_el


def get_narudzbe():
    # view za prikaz narudzbi na front
    # 1 of 2 views za stvaranje nabavne liste
    narudzbe = orm.select(x for x in Narudzba)
    narudzbe = [narudzba.to_dict(with_collections=True,
                                 related_objects=True) for narudzba in narudzbe]
    for narudzba in narudzbe:
        narudzba["stavke"] = [stavka.to_dict(only=["jelo_id", "kolicina"], with_collections=True, related_objects=True
                                             ) for stavka in narudzba["stavke"]]
    for narudzba in narudzbe:
        for stavka in narudzba["stavke"]:
            jelo_det = stavka["jelo_id"].to_dict()
            stavka["jelo_id"] = jelo_det["id"]
            stavka["ime_jela"] = jelo_det["ime_jela"]
    return narudzbe


def get_narudzba_by_id(narudzba_id):
    narudzbe = get_narudzbe()
    narudzba = [element for element in narudzbe if element["id"]
                == narudzba_id][0]
    return narudzba


def nabavna_lista_by_narudzba(narudzba):
    # trenutno je ovako radi testing, kasnije stavi parametar u funkciji
    # narudzba = narudzbe[0]
    # lista normativa kao lista dictionary-a, lakse mi je za hendlat
    normativi_db = orm.select(x for x in Normativ)[:]
    lista_normativa = [normativ.to_dict(with_collections=True,
                                        related_objects=True) for normativ in normativi_db]

    nabava = []
    # cilj ovoga je spremiti u var nabava popis potrebnih namirnica za izvrsenje narudzbe
    # ovo je zamisljeno da racuna kolicinu namirnica za samo jednu narudzbu
    # da narudzba ima status tek kada je status nesto u stilu approved bi se namirnice makle sa skladista
    for stavka in narudzba["stavke"]:
        for normativ in lista_normativa:
            nd = {}
            if stavka["jelo_id"] == normativ["jelo_id"].id:
                nd["nam_id"] = normativ["namirnica_id"].id
                nd["ime_nam"] = normativ["namirnica_id"].ime_namirnice
                nd["kolicina"] = normativ["kolicina_nam"] * stavka["kolicina"]
                nd["zaliha"] = normativ["namirnica_id"].stanje_namirnice
                nd["mj_jedinica"] = normativ["namirnica_id"].mjerna_jedinica
                dict_index = next((index for (index, d) in enumerate(
                    nabava) if d["nam_id"] == normativ["namirnica_id"].id), None)
                if next((item for item in nabava if item['nam_id'] == normativ["namirnica_id"].id), None) is not None:
                    # ako je pronadena namirnica u dictionary, dodaj kolicinu
                    nabava[dict_index]["kolicina"] += normativ["kolicina_nam"] * \
                        stavka["kolicina"]
                else:
                    nabava.append(nd)
    return nabava


def find_nabava_el(nam_id):
    found = orm.select(x for x in Nabava if x.nam_id.id == nam_id)[:]
    if found:
        return True
    else:
        return False
