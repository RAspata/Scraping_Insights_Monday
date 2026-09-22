---
name: weekly-horeca-digest
description: Genereaza digestul saptamanal de stiri HoReCa si food din Romania, cu scor de relevanta 1-10 pentru un Sales Executive Glovo. Ruleaza in fiecare luni dimineata.
---

# Weekly HoReCa & Food Digest

## Context

Utilizatorul este Sales Executive la Glovo, in Bucuresti, si vrea sa fie la curent
in fiecare saptamana cu miscarile importante din piata HoReCa si food din Romania
(deschideri/inchideri de restaurante, cafenele si lanturi HoReCa, extinderi,
parteneriate, schimbari legislative relevante — ex. TVA HoReCa —, miscari ale
concurentei din food delivery, tendinte de consum alimentar).

Exclude explicit stirile de retail general (supermarketuri, hipermarketuri,
FMCG, mall-uri, spatii comerciale) daca nu au legatura directa cu HoReCa sau food —
scopul e strict industria HoReCa/food, nu retail-ul in ansamblu.

**Regula de baza: fiecare stire apare intr-un singur raport.** Ce a fost publicat
intr-un digest anterior nu mai apare niciodata, nici de pe alta sursa.

## Fisiere

- `surse-horeca-retail.md` — lista de surse, cu feed-uri RSS si pagini HoReCa/food.
- `rapoarte/digest-YYYY-MM-DD.md` — rapoartele saptamanale.
- `rapoarte/linkuri-procesate.txt` — registrul stirilor deja publicate
  (`data<TAB>link<TAB>titlu`, cate un rand per link). Il actualizeaza scriptul.
- `.claude/skills/weekly-horeca-digest/scripts/colecteaza.py` — colecteaza feed-urile.

## Pasi

1. **Ruleaza colectorul** din radacina repo-ului:

   ```
   python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py
   ```

   Scriptul stabileste fereastra de timp (de la data ultimului raport pana acum;
   7 zile daca nu exista niciun raport), citeste toate feed-urile din
   `surse-horeca-retail.md` cu paginare si afiseaza:
   - un tabel cu starea fiecarei surse (ok / blocat / eroare / fara feed) si daca
     feed-ul acopera toata fereastra;
   - articolele din fereastra, cu data exacta, **deja fara** cele publicate in
     rapoartele anterioare. La feed-urile `(filtrat)` trec doar titlurile cu
     cuvinte-cheie HoReCa/food, deci lista e o preselectie — tot tu decizi relevanta.

2. **Evita repetarile.** Citeste ultimele ~150 de randuri din
   `rapoarte/linkuri-procesate.txt` (titlurile publicate recent). Elimina orice stire
   care descrie **acelasi eveniment** ca una deja publicata, chiar daca vine de pe
   alt site sau are alt titlu. Exceptie: o evolutie noua si concreta a unui subiect
   vechi (ex. tranzactia anuntata acum s-a finalizat) e o stire noua — atunci
   spune explicit in rezumat ce e nou fata de data trecuta.

3. **Completeaza unde feed-ul nu ajunge.** Pentru sursele marcate in tabel cu
   `fara feed` sau `feed INCOMPLET`, citeste paginile `Pagină HoReCa/food:` din
   `surse-horeca-retail.md` (sau homepage-ul, daca sursa nu are pagini dedicate).
   Citeste paginile cu `curl -sL -A "Mozilla/5.0" <url>` si extrage titlurile,
   linkurile si datele din HTML. Foloseste WebFetch doar daca HTML-ul e greu de
   parcurs.

4. **Data publicarii trebuie confirmata.** O stire intra in raport doar daca data ei
   e in fereastra si e luata din feed sau de pe pagina articolului (meta
   `article:published_time`, data afisata langa titlu, data din URL). Nu estima
   data din rezultate de cautare. Verifica si linkurile venite din pagini (pas 3)
   contra `rapoarte/linkuri-procesate.txt`.

5. **Cautarea pe web e doar rezerva.** Foloseste WebSearch numai pentru o sursa
   blocata sau cu erori, maxim 3 cautari per sursa. Stirile gasite asa primesc la
   final mentiunea `(găsit prin căutare)` si respecta aceeasi regula de data.
   Nu folosi servicii intermediare de citire a paginilor (r.jina.ai, cache-uri
   Google etc.).

6. **Filtreaza** doar articolele relevante pentru HoReCa sau food (restaurante,
   cafenele, catering, food delivery, productie/distributie alimentara pentru
   HoReCa, tendinte de consum culinar). Ignora retailul general (supermarketuri,
   FMCG, mall-uri), faptul divers (accidente, infractiuni, scandaluri fara impact
   de business), politica si sportul, chiar daca titlul contine un cuvant-cheie.

7. **Pentru fiecare stire retinuta**, scrie:
   - Titlu (in romana; daca sursa e deja in romana pastreaza-l)
   - Sursa si data publicarii
   - Un rezumat de 2-3 propozitii, in cuvinte proprii (nu copia paragrafe). Pentru
     rezumat citeste articolul (feed-ul are de obicei si un fragment in
     `<description>`); daca articolul nu se poate deschide, rezuma doar ce e sigur.
   - Un **scor de importanta 1-10**, din perspectiva unui Sales Executive Glovo care
     vrea sa inteleaga miscarile din piata pe care le poate folosi in prospectare,
     negociere sau pozitionare. Scoreaza mai sus:
       - deschideri/extinderi de restaurante, cafenele sau lanturi HoReCa (potentiali parteneri noi)
       - miscari ale concurentei din livrari: Wolt (care preia Tazz), Bolt Food,
         alte platforme noi; restaurante care renunta la aplicatiile de livrare sau
         isi fac livrare proprie; ghost kitchens
       - schimbari legislative/fiscale care afecteaza marjele HoReCa (TVA, taxe)
       - date agregate despre piata (cifra de afaceri HoReCa, numar de unitati, inchideri)
     Scoreaza mai jos:
       - stiri de opinie/interviu fara informatie noua
       - evenimente/gale fara impact direct de business
       - numiri de personal fara impact asupra strategiei companiei

8. **Sorteaza** stirile descrescator dupa scor si scrie raportul in
   `rapoarte/digest-YYYY-MM-DD.md` (data rularii, ora Romaniei).

9. **Structura raportului**:
   ```
   # Digest HoReCa & Food — [data]

   Perioada acoperita: [inceput fereastra] – [data rularii]

   ## Pe scurt (top 3)
   [1-2 propozitii per stire, doar cele cu scor >= 8, daca exista]

   ## Toate stirile (sortate dupa scor)
   ### [Scor]/10 — [Titlu]
   Sursa: [nume] — [data]
   [rezumat]
   [link]

   ## Starea surselor
   | Sursa | Stiri incluse | Stare |
   [cate un rand pentru fiecare sursa: ok / fara stiri relevante saptamana asta /
   blocat de reteaua mediului / eroare HTTP xxx / acoperita partial prin cautare]
   ```
   Linkul fiecarei stiri sta pe propriul rand, sub rezumat — scriptul il citeste
   de acolo in pasul urmator. Nu pune alte linkuri in sectiunea `Toate stirile`.

10. **Inregistreaza stirile publicate**:

    ```
    python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py --mark rapoarte/digest-YYYY-MM-DD.md
    ```

    Asta adauga linkurile din raport in `rapoarte/linkuri-procesate.txt`, ca sa nu
    mai apara in rapoartele urmatoare. Raportul si registrul se commit-uiesc impreuna.

## Note

- Nu reproduce paragrafe intregi din articole — rezumatul trebuie sa fie in
  cuvinte proprii, mult mai scurt decat originalul.
- Daca intr-o saptamana nu exista nicio stire relevanta pe o sursa, e ok sa
  lipseasca din raport — nu inventa continut.
- Daca o sursa apare `blocat` in tabel, e o problema de retea a mediului cloud
  (lista de domenii permise), nu a sursei — spune asta in `Starea surselor`.
