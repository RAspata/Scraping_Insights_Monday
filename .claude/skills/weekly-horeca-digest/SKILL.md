---
name: weekly-horeca-digest
description: Genereaza digestul saptamanal de stiri HoReCa si food din Romania, cu scor de relevanta 1-10 pentru un Sales Executive Glovo. Ruleaza in fiecare luni dimineata.
---

# Weekly HoReCa & Food Digest

## Context

Utilizatorul este Sales Executive la Glovo, in Bucuresti. Treaba lui e sa semneze
contracte cu restaurante partenere noi. Raportul nu e o revista a pietei, ci o
**lista de oportunitati de vanzare**: fiecare stire trebuie sa raspunda la
intrebarea „pot merge acolo, sau pot suna pe cineva, ca sa semnez un restaurant
nou pe Glovo?”.

Il intereseaza: restaurante, cafenele, fast-food-uri, dark kitchens care se
deschid sau urmeaza sa se deschida, lanturi care intra in orase noi, food halls si
food courts noi (multi chiriasi intr-un singur loc), festivaluri de street food si
targuri gastronomice (multi operatori de mancare adunati intr-un loc), restaurante
care parasesc alte platforme de livrare sau care nu livreaza inca.

Nu il intereseaza informatia generala despre piata: statistici, cifre de afaceri
agregate, studii, numiri de personal, premii, gale, cronici de restaurant, retailul
general (supermarketuri, FMCG, mall-uri fara componenta food). Acestea nu intra in
raport, chiar daca sunt stiri HoReCa corecte.

**Regula de baza: fiecare stire apare intr-un singur raport.** Ce a fost publicat
intr-un digest anterior nu mai apare niciodata, nici de pe alta sursa.

## Fisiere

- `surse-horeca-retail.md` — lista de surse, cu feed-uri RSS si pagini HoReCa/food.
- `rapoarte/digest-YYYY-MM-DD.md` — rapoartele saptamanale.
- `rapoarte/linkuri-procesate.txt` — registrul stirilor deja publicate
  (`data<TAB>link<TAB>titlu`, cate un rand per link). Il actualizeaza scriptul.
- `.claude/skills/weekly-horeca-digest/scripts/colecteaza.py` — colecteaza feed-urile.

## Pasi

1. **Porneste de la colectarea facuta de GitHub.** Un workflow GitHub Actions
   ruleaza luni la 05:00 UTC colectorul in modul complet si salveaza rezultatul in
   `colectare/colectare.md`. GitHub poate citi si site-urile care refuza cererile
   din mediul cloud (Wall-Street, Capital, BZI), iar fisierul contine pentru
   fiecare articol si descrierea lui (randul `>` de sub titlu).

   Fa `git pull origin main`, apoi citeste primul rand din `colectare/colectare.md`
   (`# Fereastra: ... -> YYYY-MM-DD HH:MM`).
   - **Daca data de dupa `->` e azi** (ora Romaniei), foloseste fisierul ca lista
     de articole si **nu mai rula colectorul**. Sari peste pasul 3 pentru sursele
     marcate acolo cu `citite paginile HoReCa/food` sau `completat din paginile
     HoReCa/food` — paginile lor sunt deja incluse.
   - **Altfel** (fisierul lipseste sau e vechi, de ex. la o rulare manuala in
     mijlocul saptamanii), ruleaza colectorul tu din radacina repo-ului:

     ```
     python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py
     ```

   In ambele cazuri primesti fereastra de timp (de la data ultimului raport pana
   acum; 7 zile daca nu exista niciun raport) si:
   - un tabel cu starea fiecarei surse (ok / blocat / eroare / fara feed) si daca
     feed-ul acopera toata fereastra;
   - articolele din fereastra, cu data exacta, **deja fara** cele publicate in
     rapoartele anterioare. La feed-urile `(filtrat)` si la pagini trec doar
     titlurile cu cuvinte-cheie HoReCa/food, deci lista e o preselectie — tot tu
     decizi relevanta.

   Pentru rezumat si randul `Oportunitate`, deschide articolul. Daca site-ul
   refuza cererea din cloud, foloseste descrierea din `colectare/colectare.md`
   si scrie doar ce reiese sigur din ea. Articolele venite prin Google News
   (linkuri `news.google.com/...`, la Wall-Street si BZI) au doar titlu si data:
   daca nu poti deschide articolul, scrie rezumatul si randul `Oportunitate` doar
   din titlu, fara sa completezi detalii care nu apar acolo. Pastreaza linkul
   Google News in raport — duce la articolul original.

   **Daca scriptul iese cu codul 3 (toate feed-urile blocate de retea), opreste-te.**
   Nu scrie raport, nu rula `--mark`, nu face commit sau push: un raport gol ar fi
   trimis pe email si ar muta inceputul ferestrei urmatoare, pierzand stirile
   saptamanii. Incheie cu un mesaj clar ca mediul cloud nu are acces la internet si
   ca setarea de retea a mediului trebuie schimbata. La fel procedeaza daca, dupa
   pasii 3–5, nu ai putut confirma nicio stire din cauza blocajelor de retea.

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

6. **Filtreaza pe oportunitati concrete.** Pastreaza doar stirile din care iese o
   actiune de vanzare: un local anume, un operator anume sau un eveniment anume
   unde se poate merge. Elimina tot ce e informatie generala (vezi Context), plus
   faptul divers, politica si sportul, chiar daca titlul contine un cuvant-cheie.

7. **Scorul 1-10 = cat de repede si cat de sigur poate semna contracte noi
   Sales Executive-ul pe baza stirii.** Grila:

   | Scor | Ce fel de stire |
   |---|---|
   | 9-10 | Restaurant, cafenea, fast-food sau dark kitchen **nou deschis sau cu deschidere anuntata**, cu adresa sau zona cunoscuta, in Bucuresti. Food hall / food court nou in Bucuresti (multi chiriasi). Restaurant sau lant care **paraseste Wolt/Tazz/Bolt Food** sau spune ca nu livreaza inca. |
   | 7-8 | Acelasi tip de deschidere in alt oras mare unde e Glovo (Cluj, Timisoara, Iasi, Brasov, Constanta, Sibiu, Craiova etc.). Lant care anunta un plan de extindere cu orase sau numar de unitati (ex. „5 restaurante noi in 2026”). Brand strain care intra in Romania. Festival de street food / targ gastronomic cu multi operatori, cu data si loc cunoscute, inca nedesfasurat — **in Bucuresti primeste minim 8** (orice eveniment care urmeaza si aduna multi operatori HoReCa: food festival, coffee festival, food week, targ de producatori). |
   | 5-6 | Deschidere sau eveniment cu detalii incomplete (fara zona sau fara data). Lant existent care isi schimba conceptul sau lanseaza un brand nou. Relocari si redeschideri. Operator local care creste (investitie, locatie a doua). |
   | 3-4 | Mentiune indirecta a unor operatori care ar putea fi prospectati (ex. lista restaurantelor participante la o saptamana gastronomica deja incheiata). |
   | 1-2 | Nu intra in raport. |

   Criterii de departajare la acelasi tip de stire: Bucuresti inaintea altor
   orase; ceva care urmeaza (deschidere, festival) inaintea a ceva deja trecut;
   operator independent sau lant mic (mai usor de semnat) inaintea unui gigant
   care negociaza central (McDonald's, KFC). Un lant mare care deschide ramane
   totusi o stire buna, dar max 7.

   **Nu intra in raport stirile cu scor sub 3.** Daca intr-o saptamana raman putine
   stiri, e in regula: mai bine 5 oportunitati reale decat 20 de stiri generale.

8. **Pentru fiecare stire retinuta**, scrie:
   - Titlu (in romana; daca sursa e deja in romana pastreaza-l)
   - Sursa si data publicarii
   - Un rezumat de 1-2 propozitii, in cuvinte proprii (nu copia paragrafe). Pentru
     rezumat citeste articolul (feed-ul are de obicei si un fragment in
     `<description>`); daca articolul nu se poate deschide, rezuma doar ce e sigur.
   - Un rand **Oportunitate:** cu ce se poate face concret, luat din articol:
     numele localului sau al operatorului, adresa/zona, data deschiderii sau a
     evenimentului, persoana sau firma mentionata (fondator, francizor,
     organizator). Scrie doar ce apare in articol; daca lipseste, spune „adresa
     nu e mentionata” in loc sa ghicesti.

9. **Sorteaza** stirile descrescator dupa scor si scrie raportul in
   `rapoarte/digest-YYYY-MM-DD.md` (data rularii, ora Romaniei).

10. **Structura raportului**:
   ```
   # Oportunitati HoReCa — [data]

   Perioada acoperita: [inceput fereastra] – [data rularii]

   ## Pe scurt
   [cele mai bune 3 oportunitati (primele 3 din lista de mai jos), cate un rand:
   ce, unde, cand. Daca sunt mai putin de 3 stiri, doar cate sunt.]

   ## Toate stirile (sortate dupa scor)
   ### [Scor]/10 — [Titlu]
   Sursa: [nume] — [data]
   [rezumat]
   Oportunitate: [local/operator, adresa/zona, data, persoana de contact]
   [link]
   ```
   Raportul se opreste dupa ultima stire: fara sectiune despre starea surselor,
   fara note tehnice (raportul e trimis pe email, iar cititorul nu vrea asa ceva).
   Starea surselor (ce a mers, ce a fost blocat, ce a refuzat cererile) o scrii
   doar in mesajul final al sesiunii, nu in raport.

   Linkul fiecarei stiri sta pe propriul rand, sub randul `Oportunitate` —
   scriptul il citeste de acolo in pasul urmator. Nu pune alte linkuri in
   sectiunea `Toate stirile`.

11. **Inregistreaza stirile publicate**:

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
- `blocat (proxy de retea)` in tabelul scriptului inseamna ca mediul cloud nu are
  voie sa iasa spre acel domeniu. Un raspuns HTTP 403 sau 429 de la site inseamna
  altceva: site-ul refuza cererile venite din datacenter — in mesajul final scrie
  „site-ul refuza cererile (HTTP xxx)”, nu „blocat de reteaua mediului”.
