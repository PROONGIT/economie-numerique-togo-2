"""
Prépare les données consolidées pour le dashboard télécom Togo.
Sources : agences opérateurs (Moov, Togocom, Télécom=fusion, CANAL+),
datacenters, agents mobile money, population par préfecture (RGPH-5, 2022).
"""
import csv
import json
import re
from collections import defaultdict

DATA = "data/"
OUT = "data/processed/"
import os
os.makedirs(OUT, exist_ok=True)


def parse_point(geom):
    if not geom:
        return None, None
    m = re.match(r"POINT\s*\(([-\d.]+)\s+([-\d.]+)\)", geom.strip())
    if not m:
        return None, None
    lon, lat = float(m.group(1)), float(m.group(2))
    return lat, lon


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------- 1. Agences opérateurs (Moov + Togocom, source "Télécom" = fusion) ----------
moov = load_csv(DATA + "file-Agences_-_Moov-07-09-2026_22_21_35.csv")
togocom = load_csv(DATA + "file-Agences_-_Togocom-07-09-2026_22_24_17.csv")
canal = load_csv(DATA + "file-Agences_-_CANAL_-07-09-2026_22_25_42.csv")

agences = []
for row, operateur in [(r, "Moov") for r in moov] + [(r, "Togocom") for r in togocom]:
    lat, lon = parse_point(row["geometry"])
    agences.append({
        "operateur": operateur,
        "region": row["region_nom_bdd"],
        "prefecture": row["prefecture_nom_bdd"],
        "commune": row["commune_nom_bdd"],
        "canton": row["canton_nom_bdd"],
        "localite": row["nom_localite"],
        "nom": row["etab_nom"],
        "adresse": row["etab_adresse"],
        "annee_creation": row["etab_creation_date"],
        "lat": lat, "lon": lon,
    })

with open(OUT + "agences.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(agences[0].keys()))
    w.writeheader()
    w.writerows(agences)

print(f"Agences opérateurs : {len(agences)} (Moov={len(moov)}, Togocom={len(togocom)}, CANAL+={len(canal)})")

# ---------- 2. Datacenters ----------
dc = load_csv(DATA + "file-Datacenter_-_Établissements-07-09-2026_22_26_21.csv")
datacenters = []
for row in dc:
    lat, lon = parse_point(row["geometry"])
    datacenters.append({
        "nom": row["etab_nom"], "region": row["region_nom_bdd"],
        "prefecture": row["prefecture_nom_bdd"], "commune": row["commune_nom_bdd"],
        "canton": row["canton_nom_bdd"], "localite": row["nom_localite"],
        "annee_creation": row["etab_creation_date"], "statut": row["activite_statut"],
        "lat": lat, "lon": lon,
    })
with open(OUT + "datacenters.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(datacenters[0].keys()))
    w.writeheader()
    w.writerows(datacenters)
print(f"Datacenters : {len(datacenters)}")

# ---------- 3. Agents mobile money ----------
mm = load_csv(DATA + "file-Agents_mobile_money-07-09-2026_22_27_08.csv")
mm_clean = []
for row in mm:
    lat, lon = parse_point(row["geometry"])
    op = row["operateur"].strip()
    mm_clean.append({
        "region": row["region_nom_bdd"], "prefecture": row["prefecture_nom_bdd"],
        "commune": row["commune_nom_bdd"], "canton": row["canton_nom_bdd"],
        "operateur": op, "lat": lat, "lon": lon,
    })
with open(OUT + "mobile_money.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(mm_clean[0].keys()))
    w.writeheader()
    w.writerows(mm_clean)
print(f"Agents mobile money : {len(mm_clean)}")

# ---------- 4. Population ----------
pop = load_csv(DATA + "population_prefectures_rgph5.csv")
pop_by_pref = {r["prefecture_nom_bdd"]: r for r in pop}
pop_by_region = defaultdict(lambda: {"population_masculin": 0, "population_feminin": 0, "population_totale": 0})
for r in pop:
    reg = pop_by_region[r["region_nom_bdd"]]
    reg["population_masculin"] += int(r["population_masculin"])
    reg["population_feminin"] += int(r["population_feminin"])
    reg["population_totale"] += int(r["population_totale"])

# ---------- 5. Agrégation par préfecture (niveau où la population est connue) ----------
def count_by(items, key):
    c = defaultdict(int)
    for it in items:
        c[it[key]] += 1
    return c

ag_by_pref = count_by(agences, "prefecture")
ag_moov_by_pref = count_by([a for a in agences if a["operateur"] == "Moov"], "prefecture")
ag_togocom_by_pref = count_by([a for a in agences if a["operateur"] == "Togocom"], "prefecture")
mm_by_pref = count_by(mm_clean, "prefecture")
dc_by_pref = count_by(datacenters, "prefecture")

# cantons/communes distincts couverts (au moins 1 agence / 1 agent)
cantons_avec_agence = set(a["canton"] for a in agences)
cantons_avec_mm = set(m["canton"] for m in mm_clean)
communes_avec_agence = set(a["commune"] for a in agences)
communes_avec_mm = set(m["commune"] for m in mm_clean)
tous_cantons = set(m["canton"] for m in mm_clean) | set(a["canton"] for a in agences)
tous_communes = set(m["commune"] for m in mm_clean) | set(a["commune"] for a in agences)

rows_out = []
for pref, prow in pop_by_pref.items():
    pop_tot = int(prow["population_totale"])
    n_ag = ag_by_pref.get(pref, 0)
    n_mm = mm_by_pref.get(pref, 0)
    n_dc = dc_by_pref.get(pref, 0)
    rows_out.append({
        "region": prow["region_nom_bdd"],
        "prefecture": pref,
        "population": pop_tot,
        "nb_agences": n_ag,
        "nb_agences_moov": ag_moov_by_pref.get(pref, 0),
        "nb_agences_togocom": ag_togocom_by_pref.get(pref, 0),
        "nb_datacenters": n_dc,
        "nb_agents_mobile_money": n_mm,
        "population_par_agence": round(pop_tot / n_ag) if n_ag else None,
        "population_par_agent_mm": round(pop_tot / n_mm) if n_mm else None,
        "agences_pour_100k_hab": round(n_ag / pop_tot * 100000, 2) if pop_tot else 0,
        "agents_mm_pour_10k_hab": round(n_mm / pop_tot * 10000, 2) if pop_tot else 0,
    })

with open(OUT + "synthese_prefecture.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
    w.writeheader()
    w.writerows(rows_out)

# ---------- 6. Synthèse région ----------
rows_region = []
for reg, pd_ in pop_by_region.items():
    pop_tot = pd_["population_totale"]
    n_ag = sum(1 for a in agences if a["region"] == reg)
    n_mm = sum(1 for m in mm_clean if m["region"] == reg)
    n_dc = sum(1 for d in datacenters if d["region"] == reg)
    rows_region.append({
        "region": reg, "population": pop_tot,
        "nb_agences": n_ag, "nb_datacenters": n_dc, "nb_agents_mobile_money": n_mm,
        "agences_pour_100k_hab": round(n_ag / pop_tot * 100000, 2) if pop_tot else 0,
        "agents_mm_pour_10k_hab": round(n_mm / pop_tot * 10000, 2) if pop_tot else 0,
    })
with open(OUT + "synthese_region.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_region[0].keys()))
    w.writeheader()
    w.writerows(rows_region)

# ---------- 7. Zones blanches proxy (cantons sans aucune agence, cantons sans agent mobile money) ----------
print("\n--- Constats clés ---")
print(f"Cantons total (union agences+mm) : {len(tous_cantons)}")
print(f"Cantons AVEC au moins une agence opérateur : {len(cantons_avec_agence)} ({len(cantons_avec_agence)/len(tous_cantons)*100:.1f}%)")
print(f"Cantons SANS aucune agence opérateur : {len(tous_cantons - cantons_avec_agence)} ({len(tous_cantons - cantons_avec_agence)/len(tous_cantons)*100:.1f}%)")
print(f"Cantons AVEC au moins un agent mobile money : {len(cantons_avec_mm)} ({len(cantons_avec_mm)/len(tous_cantons)*100:.1f}%)")
print(f"Cantons SANS aucun agent mobile money (zone blanche numérique) : {len(tous_cantons - cantons_avec_mm)}")
print(f"Communes total : {len(tous_communes)} | avec agence : {len(communes_avec_agence)} | avec mm : {len(communes_avec_mm)}")

zones_blanches_mm = sorted(tous_cantons - cantons_avec_mm)
with open(OUT + "cantons_sans_mobile_money.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["canton"])
    for c in zones_blanches_mm:
        w.writerow([c])

# ---------- 8. National KPIs JSON ----------
kpis = {
    "population_totale": sum(int(r["population_totale"]) for r in pop),
    "nb_agences_total": len(agences),
    "nb_agences_moov": len(moov),
    "nb_agences_togocom": len(togocom),
    "nb_agences_canal": len(canal),
    "nb_datacenters": len(datacenters),
    "nb_datacenters_lome": sum(1 for d in datacenters if d["prefecture"] == "Golfe" or d["commune"].startswith("Golfe")),
    "nb_agents_mobile_money": len(mm_clean),
    "nb_cantons_total": len(tous_cantons),
    "nb_cantons_sans_agence": len(tous_cantons - cantons_avec_agence),
    "nb_cantons_sans_mobile_money": len(tous_cantons - cantons_avec_mm),
    "nb_communes_total": len(tous_communes),
    "nb_communes_sans_agence": len(tous_communes - communes_avec_agence),
    "nb_prefectures": len(pop_by_pref),
}
with open(OUT + "kpis_nationaux.json", "w", encoding="utf-8") as f:
    json.dump(kpis, f, ensure_ascii=False, indent=2)

print("\nKPIs nationaux:", json.dumps(kpis, ensure_ascii=False, indent=2))
print("\nTerminé. Fichiers écrits dans", OUT)
