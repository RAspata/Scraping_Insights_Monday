# Surse pentru digest-ul săptămânal HoReCa & Food

Acesta e un fișier simplu de editat. Adaugă/șterge rânduri oricând — skill-ul citește
acest fișier la fiecare rulare, deci nu trebuie să modifici nimic altceva.

Format:

```
- [Nume sursă](URL homepage) — categorie — oraș/acoperire
  - Feed: URL                   ← feed RSS citit integral (surse dedicate HoReCa/food)
  - Feed (filtrat): URL         ← feed RSS al unei surse generaliste; se păstrează doar
                                  titlurile cu cuvinte-cheie HoReCa/food
  - Pagină HoReCa/food: URL     ← secțiune/tag dedicat, citit direct din pagină
```

Pentru site-urile care refuză cererile venite din servere (Wall-Street, BZI), feed-ul
e o căutare Google News limitată la acel site și la cuvinte HoReCa. Linkurile din el
trec prin news.google.com și duc la articolul original.

Ordinea de lucru a skill-ului: întâi feed-urile (au data exactă a publicării), apoi
paginile HoReCa/food, iar homepage-ul doar ca rezervă. Rândurile `Feed` și `Pagină`
sunt opționale — o sursă nouă poate avea doar linia principală.

## Publicații naționale HoReCa / food service

- [TrendsHRB](https://trendshrb.ro) — HoReCa/ospitalitate — național
  - Feed: https://www.trendshrb.ro/feed/
  - Pagină HoReCa/food: https://www.trendshrb.ro/stiri/
- [Retail-FMCG — Food Service](https://www.retail-fmcg.ro/food-service/) — food service — național
  - Feed: https://www.retail-fmcg.ro/food-service/feed
- [Revista Biz — secțiunea HoReCa](https://www.revistabiz.ro) — business/HoReCa — național
  - Feed (filtrat): https://www.revistabiz.ro/feed/
- [ȘtirileProTV — HoReCa](https://stirileprotv.ro/stiri-despre/horeca/) — HoReCa — național
  - Feed (filtrat): https://stirileprotv.ro/rss

## Publicații naționale business/economic (doar secțiunile HoReCa / food / consum)

Sunt surse generaliste — skill-ul trebuie să filtreze din ele doar știrile
legate de HoReCa/food, nu orice altă știre de business.

- [Ziarul Financiar](https://www.zf.ro) — business — național
  - Feed (filtrat): https://www.zf.ro/rss
  - Pagină HoReCa/food: https://www.zf.ro/companii/retail-agrobusiness/ (include și retail general — de filtrat)
- [Profit.ro](https://www.profit.ro) — business — național
  - Feed (filtrat): https://www.profit.ro/rss
- [Wall-Street.ro](https://www.wall-street.ro) — business — național
  - Feed (filtrat): https://news.google.com/rss/search?q=site%3Awall-street.ro%20%28restaurant%20OR%20restaurante%20OR%20cafenea%20OR%20cafenele%20OR%20horeca%20OR%20bistro%20OR%20%22street%20food%22%20OR%20festival%20OR%20%22fast%20food%22%20OR%20livrare%20OR%20gastronomic%29%20when%3A14d&hl=ro&gl=RO&ceid=RO:ro
  - Pagină HoReCa/food: https://www.wall-street.ro/articol/horeca/index.html
  - Pagină HoReCa/food: https://www.wall-street.ro/tag/restaurante.html
- [Economica.net](https://www.economica.net) — business — național
  - Feed: https://www.economica.net/tag/horeca/feed
  - Feed (filtrat): https://www.economica.net/rss
- [Capital.ro](https://www.capital.ro) — business — național
  - Pagină HoReCa/food: https://www.capital.ro/tag/horeca
- [StartupCafe.ro](https://www.startupcafe.ro) — antreprenoriat — național
  - Feed (filtrat): https://startupcafe.ro/rss

## Presă locală pe orașe (acolo unde Glovo e prezent)

Sunt surse generaliste locale — skill-ul filtrează din ele doar știrile HoReCa/food
(deschideri de restaurante/cafenele, lanțuri locale, evenimente gastronomice etc.).

- [Actual de Cluj](https://actualdecluj.ro) — economic local — Cluj-Napoca
  - Feed (filtrat): https://actualdecluj.ro/feed/
- [BZI.ro](https://www.bzi.ro) — general/economic local — Iași
  - Feed (filtrat): https://www.bzi.ro/rss
  - Feed (filtrat): https://news.google.com/rss/search?q=site%3Abzi.ro%20%28restaurant%20OR%20restaurante%20OR%20cafenea%20OR%20cafenele%20OR%20horeca%20OR%20bistro%20OR%20%22street%20food%22%20OR%20festival%20OR%20%22fast%20food%22%20OR%20livrare%20OR%20gastronomic%29%20when%3A14d&hl=ro&gl=RO&ceid=RO:ro
- [Turnul Sfatului](https://www.turnulsfatului.ro) — general local — Sibiu
  - Feed (filtrat): https://www.turnulsfatului.ro/feed/
  - Pagină HoReCa/food: https://www.turnulsfatului.ro/timp-liber/cronica-de-restaurant/
- [Ziua de Constanța](https://www.ziuaconstanta.ro) — general local — Constanța
- [Sibiu100](https://www.sibiu100.ro) — general local — Sibiu
  - Feed: https://www.sibiu100.ro/tag/horeca/feed/
  - Feed (filtrat): https://www.sibiu100.ro/feed/
- [Tion.ro](https://www.tion.ro) — general local — Timișoara
  - Feed (filtrat): https://www.tion.ro/feed/

> Notă: lista de presă locală e un punct de plecare, nu una verificată exhaustiv —
> unele publicații locale mici își schimbă des domeniul sau frecvența de postare.
> Complet liber să adaugi orice altă sursă locală pe care o urmărești deja
> (ex. pentru Brașov, Craiova, Oradea, Ploiești, Galați, Brăila, Arad,
> Târgu Mureș, Baia Mare, Suceava, Pitești — orașe mari/medii unde Glovo
> operează și pentru care nu am inclus încă o sursă locală dedicată).

## Concurență din food delivery (opțional, dar relevant pentru Glovo)

- Adaugă aici orice sursă specifică despre Wolt (care preia Tazz), Bolt Food sau alți
  jucători din livrări, dacă vrei să-i urmărești separat
