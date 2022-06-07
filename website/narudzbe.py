# simuliranje narudzba klijenata
from models import *
from pony import orm
import requests
import random
from datetime import datetime, timedelta

db.bind(provider='sqlite', filename='baza_podataka.sqlite')
db.generate_mapping()

poduzeca = [
    'Leuschke, Barrows and Schmitt',
    'Fahey - Predovic',
    'Halvorson - Reynolds',
    'Kirlin Group',
    'Heathcote - Howe',
    'Bashirian, Kuphal and Luettgen',
    'Christiansen - Simonis',
    'Lowe, Feest and Kuvalis',
    'Oberbrunner Inc',
    'Morar - Mosciski',
    'Fisher Group',
    'Hagenes - Moen'
]

emails = [
    'lydia@me.com',
    'andrei@verizon.net',
    'laird@yahoo.com',
    'snunez@att.net',
    'lcheng@verizon.net',
    'bryanw@yahoo.com',
    'daveewart@gmail.com',
    'donev@outlook.com',
    'baveja@msn.com',
    'oevans@mac.com',
    'carcus@sbcglobal.net',
    'webteam@icloud.com']

status = ['Novo', 'Zaprimljeno', 'Izvrseno', 'Otkazano']

for i in range(1, 13):
    req_json = {
        "kupac": poduzeca.pop(),
        "kontakt": emails.pop(),
        "datum": str(datetime.now() + timedelta(days=i*round(random.uniform(1, 10)))),
        "status": status[round(random.uniform(0, 3))]
    }
    r = requests.post("http://127.0.0.1:8080/narudzbe/dolazne", json=req_json)
print(r.json())


@db_session
def create_narudzbe():
    narudzbe = orm.select(x for x in Narudzba)[:]
    for n in range(1, len(narudzbe)+1):
        # ne smijem imati 2 ista jela kao stavka, pa shuffle koristim da donekle random odaberem jela
        jela = list(range(1, 13))
        random.shuffle(jela)
        for x in range(5):
            Stavka(narudzba_id=n, jelo_id=jela.pop(),
                   kolicina=round(random.uniform(2, 7)))


create_narudzbe()
