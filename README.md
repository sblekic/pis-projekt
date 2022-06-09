# Projektni zadatak iz kolegija poslovni informacijski sustavi - aplikacija za upravljanje namirnicama u catering objektu

U kontekstu catering objekta ova aplikacija služi operativnom osoblju, primjerice šefu kuhinje za praćenje zaliha namirnica odnosno za pravovremeno naručivanje potrebnih namirnica ovisno o narudžbama.

Operativno osoblje koje koristi aplikaciju ima na uvidu stanje zaliha namirnica u formatu stupčastog dijagrama i može:

- zaprimiti i po potrebi unositi nove namirnice
- unositi jela po određenim normativima
- pregledati pristigle narudžbe i po potrebi izdati narudžbenicu

## Postavljanje projekta na lokalnom računalu

### Kreiranje docker image

```powershell
docker build --tag image_name .
```

### Pokretanje image-a

```powershell
docker run -d -p 5000:5000 image_name
```

## Podaci o studentu

Sandi Blekić, 0303075866.
