# Dashboard — Accès aux Télécoms & Services Numériques au Togo

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```
L'application s'ouvre sur `http://localhost:8501`.

## Contenu
- `app.py` — application principale (navigation, pages, filtres)
- `i18n.py` — traductions FR/EN
- `theme.py` — palettes clair/sombre et styles CSS
- `data_loader.py` — chargement + agrégation dynamique des données (région/préfecture/commune/canton), mise en cache
- `prepare_data.py` — script d'agrégation des 7 sources brutes → `data/processed/`
- `data/` — données sources (6 CSV du challenge + population RGPH-5) et données traitées
- `assets/sceau_togo.png` — sceau officiel de la République Togolaise (icône + en-tête)

## Interactivité
- **Filtres** (barre latérale) : région(s), opérateur(s) (Moov/Togocom, y compris sur le mobile
  money), et **granularité géographique** (région / préfecture / commune / canton) — ces filtres
  recalculent en direct les tableaux, graphiques et cartes de chaque page.
- **Analyses dynamiques** : sous les graphiques principaux, un encadré recalcule des constats
  chiffrés selon la sélection en cours et les relie explicitement à l'objectif du brief concerné
  (Objectifs 1 à 4).
- **Cartes 100% autonomes** : les cartes (agences/datacenters, couverture) sont tracées en
  longitude/latitude avec des contours de région calculés directement à partir des données
  (enveloppe convexe des points), sans tuile ni fichier de frontières externe — le dashboard
  fonctionne donc même sans accès internet ou derrière un pare-feu restrictif.
- **Langue et thème** : deux switchs en barre latérale (FR ⇄ EN, Clair ⇄ Sombre).

## Sources de données
1. Agences Moov, Togocom, Télécom (fusion), CANAL+ — géodonnées ouvertes 2026
2. Établissements Datacenter — géodonnées ouvertes 2026
3. Agents mobile money — géodonnées ouvertes 2026 (19 788 points, niveau canton)
4. Population des préfectures par sexe — RGPH-5, INSEED, résultats définitifs, novembre 2022

## Note méthodologique
Aucune donnée ouverte de couverture radio cellulaire (2G/3G/4G) n'existe à ce jour pour le Togo
(la carte nPerf citée dans le brief est une carte interactive sans export de données brutes).
L'onglet « Couverture & Zones blanches » construit donc un **indicateur proxy**, fondé sur la
présence de points de service (agences + agents mobile money) par canton — explicité dans le
dashboard et le rapport.

## Régénérer les données
Si les fichiers sources changent, relancer :
```bash
python3 prepare_data.py
```
