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

## Pasi

1. **Citeste lista de surse** din `surse-horeca-retail.md` (in radacina proiectului).
   Fisierul e editabil de utilizator — foloseste orice sursa e listata acolo, in
   ordinea in care apare.

2. **Pentru fiecare sursa**, acceseaza pagina principala sau sectiunea relevanta
   (HoReCa / food / economic local) si identifica articolele publicate in
   ultimele 7 zile (de luni trecuta pana azi).

3. **Filtreaza** doar articolele relevante pentru HoReCa sau food (restaurante,
   cafenele, catering, food delivery, productie/distributie alimentara,
   tendinte de consum culinar) — ignora stiri de retail general (supermarketuri,
   FMCG, mall-uri) si orice stire generalista fara legatura (politica, sport,
   fapt divers etc.), chiar daca vin de pe un site de presa locala generalista.

4. **Pentru fiecare stire retinuta**, scrie:
   - Titlu (tradus/reformulat clar, in romana, daca sursa e deja in romana pastreaza-l)
   - Sursa si data publicarii
   - Un rezumat de 2-3 propozitii, in cuvinte proprii (nu copia paragrafe din articol)
   - Un **scor de importanta 1-10**, din perspectiva unui Sales Executive Glovo care
     vrea sa inteleaga miscarile din piata pe care le poate folosi in prospectare,
     negociere sau pozitionare. Scoreaza mai sus:
       - deschideri/extinderi de restaurante, cafenele sau lanturi HoReCa (potentiali parteneri noi)
       - miscari ale concurentei directe (Tazz, Bolt Food, Foodpanda)
       - schimbari legislative/fiscale care afecteaza marjele HoReCa (TVA, taxe)
       - date agregate despre piata (cifra de afaceri HoReCa, numar de unitati)
     Scoreaza mai jos:
       - stiri de opinie/interviu fara informatie noua
       - evenimente/gale fara impact direct de business
       - stiri deja acoperite saptamana trecuta fara noutate

5. **Sorteaza** stirile descrescator dupa scor si scrie raportul intr-un fisier
   nou: `rapoarte/digest-YYYY-MM-DD.md` (data = data rularii).

6. **Structura raportului**:
   ```
   # Digest HoReCa & Food — [data]

   ## Pe scurt (top 3)
   [1-2 propozitii per stire, doar cele cu scor >= 8, daca exista]

   ## Toate stirile (sortate dupa scor)
   ### [Scor]/10 — [Titlu]
   Sursa: [nume] — [data]
   [rezumat]
   [link]
   ```

7. Daca o sursa nu raspunde sau pagina nu se poate accesa, sari peste ea si
   mentioneaza la finalul raportului ce surse au esuat, ca utilizatorul sa stie
   sa le verifice manual.

## Note

- Nu reproduce paragrafe intregi din articole — rezumatul trebuie sa fie in
  cuvinte proprii, mult mai scurt decat originalul.
- Daca intr-o saptamana nu exista nicio stire relevanta pe o sursa, e ok sa
  lipseasca din raport — nu inventa continut.
