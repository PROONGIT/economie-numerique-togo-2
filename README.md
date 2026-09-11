# Dashboard — Accès aux Télécoms & Services Numériques au Togo

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Contenu
- `app.py` — application principale (page d'accueil, navigation, pages, filtres, granularités)
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
  chiffrés selon la sélection en cours conformément aux filtres/granularités.
- **Cartographies** : les cartes (agences/datacenters, couverture) sont tracées avec OpenStreetMap. Pointer la souris sur les éléments de la carte pour afficher plus d'informations.
- **Langue et thème** : deux switchs en barre latérale (FR ⇄ EN, Clair ⇄ Sombre).

## Sources de données
1. Agences Moov, Togocom, Télécom (fusion), CANAL+ — géodonnées ouvertes 2026
2. Établissements Datacenter — géodonnées ouvertes 2026
3. Agents mobile money — géodonnées ouvertes 2026 (19 788 points, niveau canton)
4. Population des préfectures par sexe — RGPH-5, INSEED, résultats définitifs, novembre 2022

## Note méthodologique
Aucune donnée ouverte de couverture radio cellulaire (2G/3G/4G/5G) n'est jointe aux ressources
(la carte nPerf citée dans le brief est une carte interactive sans export de données brutes).
L'onglet « Couverture & Zones blanches » construit donc un **indicateur proxy**, fondé sur la
présence d'agents mobile money par canton — explicité dans le dashboard et le rapport.

## Régénérer les données
Si les fichiers sources changent, relancer :
```bash
python3 prepare_data.py
```
