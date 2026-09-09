import pandas as pd
import streamlit as st
import json
from functools import reduce

D = "data/processed/"

LEVEL_COLS = {
    "region": ["region"],
    "prefecture": ["region", "prefecture"],
    "commune": ["region", "prefecture", "commune"],
    "canton": ["region", "prefecture", "commune", "canton"],
}


@st.cache_data
def load_all():
    agences = pd.read_csv(D + "agences.csv")
    datacenters = pd.read_csv(D + "datacenters.csv")
    mm = pd.read_csv(D + "mobile_money.csv")
    synth_pref = pd.read_csv(D + "synthese_prefecture.csv")
    synth_region = pd.read_csv(D + "synthese_region.csv")
    with open(D + "kpis_nationaux.json", encoding="utf-8") as f:
        kpis = json.load(f)
    return agences, datacenters, mm, synth_pref, synth_region, kpis


def aggregate_table(agences: pd.DataFrame, mm: pd.DataFrame, datacenters: pd.DataFrame, level: str) -> pd.DataFrame:
    """Agrège agences (par opérateur), agents mobile money et datacenters au niveau
    géographique demandé (region/prefecture/commune/canton). Les 3 dataframes en
    entrée doivent déjà être filtrés (région, opérateur) par l'appelant."""
    cols = LEVEL_COLS[level]

    def grp(df, name):
        if df.empty:
            return pd.DataFrame(columns=cols + [name])
        return df.groupby(cols).size().rename(name).reset_index()

    dfs = [
        grp(agences, "nb_agences"),
        grp(agences[agences.get("operateur", pd.Series(dtype=str)) == "Moov"], "nb_agences_moov"),
        grp(agences[agences.get("operateur", pd.Series(dtype=str)) == "Togocom"], "nb_agences_togocom"),
        grp(mm, "nb_agents_mobile_money"),
        grp(datacenters, "nb_datacenters"),
    ]
    out = reduce(lambda l, r: l.merge(r, on=cols, how="outer"), dfs)
    for c in ["nb_agences", "nb_agences_moov", "nb_agences_togocom", "nb_agents_mobile_money", "nb_datacenters"]:
        if c not in out.columns:
            out[c] = 0
        out[c] = out[c].fillna(0).astype(int)
    return out.sort_values("nb_agences", ascending=False).reset_index(drop=True)


def with_population(df: pd.DataFrame, level: str, synth_pref: pd.DataFrame, synth_region: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la population (et les taux pour 100k/10k hab.) si le niveau choisi
    est région ou préfecture — seuls niveaux où le RGPH-5 fournit une population."""
    df = df.copy()
    if level == "prefecture":
        df = df.merge(synth_pref[["region", "prefecture", "population"]], on=["region", "prefecture"], how="left")
    elif level == "region":
        df = df.merge(synth_region[["region", "population"]], on=["region"], how="left")
    else:
        df["population"] = pd.NA
    has_pop = df["population"].notna().any()
    if has_pop:
        df["agences_pour_100k_hab"] = (df["nb_agences"] / df["population"] * 100000).round(2)
        df["agents_mm_pour_10k_hab"] = (df["nb_agents_mobile_money"] / df["population"] * 10000).round(2)
    else:
        df["agences_pour_100k_hab"] = pd.NA
        df["agents_mm_pour_10k_hab"] = pd.NA
    return df


@st.cache_data
def region_hulls(mm: pd.DataFrame) -> dict:
    """Calcule un contour approximatif (enveloppe convexe) de chaque région à partir
    du nuage de points mobile money — 100% dérivé des données, sans fichier de
    frontières externe ni appel réseau (le dashboard doit fonctionner hors-ligne)."""
    from scipy.spatial import ConvexHull
    hulls = {}
    for region, g in mm.groupby("region"):
        pts = g[["lon", "lat"]].dropna().values
        if len(pts) < 3:
            continue
        try:
            hull = ConvexHull(pts)
            order = list(hull.vertices) + [hull.vertices[0]]
            hulls[region] = (pts[order, 0].tolist(), pts[order, 1].tolist())
        except Exception:
            continue
    return hulls


def aggregate_geo(mm: pd.DataFrame, agences: pd.DataFrame, level: str) -> pd.DataFrame:
    """Centroïde géographique (moyenne des points) + comptages, au niveau demandé.
    Utilisé pour la carte de couverture (zones blanches), à n'importe quelle granularité."""
    cols = LEVEL_COLS[level]
    if mm.empty and agences.empty:
        return pd.DataFrame(columns=cols + ["lat", "lon", "nb_agents_mm", "nb_agences"])

    mm_g = (mm.groupby(cols).agg(lat=("lat", "mean"), lon=("lon", "mean"), nb_agents_mm=("lat", "count")).reset_index()
            if not mm.empty else pd.DataFrame(columns=cols + ["lat", "lon", "nb_agents_mm"]))
    ag_count = (agences.groupby(cols).size().rename("nb_agences").reset_index()
                if not agences.empty else pd.DataFrame(columns=cols + ["nb_agences"]))
    out = mm_g.merge(ag_count, on=cols, how="outer")
    out["nb_agents_mm"] = out["nb_agents_mm"].fillna(0).astype(int)
    out["nb_agences"] = out["nb_agences"].fillna(0).astype(int)

    missing = out["lat"].isna() if "lat" in out.columns else pd.Series([], dtype=bool)
    if missing.any() and not agences.empty:
        ag_latlon = agences.groupby(cols).agg(lat=("lat", "mean"), lon=("lon", "mean")).reset_index()
        out = out.merge(ag_latlon, on=cols, how="left", suffixes=("", "_ag"))
        out["lat"] = out["lat"].fillna(out["lat_ag"])
        out["lon"] = out["lon"].fillna(out["lon_ag"])
        out = out.drop(columns=["lat_ag", "lon_ag"])
    return out.dropna(subset=["lat", "lon"])
