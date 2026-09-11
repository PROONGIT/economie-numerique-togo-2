# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import re

from i18n import t
from theme import THEMES, inject_css
from data_loader import load_all, aggregate_table, with_population, aggregate_geo, region_hulls, LEVEL_COLS

st.set_page_config(
    page_title="Télécoms & Numérique — Togo",
    page_icon="assets/sceau_togo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Session state defaults ----------------
if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "theme" not in st.session_state:
    st.session_state.theme = "clair"

agences, datacenters, mm, synth_pref, synth_region, kpis = load_all()

OP_COLORS = {"Moov": "#0072CE", "Togocom": "#F5A300", "Datacenter": "#D21034"}
GRAN_LEVELS = ["region", "prefecture", "commune", "canton"]

with open("assets/sceau_togo.png", "rb") as _f:
    SEAL_B64 = base64.b64encode(_f.read()).decode()

# ==================== SIDEBAR ====================
with st.sidebar:
    lang_is_en = st.toggle("🇫🇷 FR  ⇄  🇬🇧 EN", value=(st.session_state.lang == "en"), key="lang_toggle")
    st.session_state.lang = "en" if lang_is_en else "fr"
    lang = st.session_state.lang

    theme_is_dark = st.toggle(f"☀️ {t('theme_light', lang)}  ⇄  🌙 {t('theme_dark', lang)}",
                               value=(st.session_state.theme == "sombre"), key="theme_toggle")
    st.session_state.theme = "sombre" if theme_is_dark else "clair"
    theme = st.session_state.theme
    T = THEMES[theme]
    
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("assets/sceau_togo.png", width=90)
    st.markdown(
        f"<div style='text-align: center;'><strong>{t('republic_name', lang)}</strong></div>", 
        unsafe_allow_html=True
    )
    # st.image("assets/sceau_togo.png", width=90)
    # st.markdown(f"**{t('republic_name', lang)}**")
    # st.markdown("### République Togolaise" if st.session_state.lang == "fr" else "### Republic of Togo")
    st.markdown("---")

    st.markdown(f"**{t('nav_title', lang)}**")
    page = st.radio(
        t("nav_title", lang),
        options=["overview", "map", "mm", "density", "coverage", "reco"],
        format_func=lambda k: {
            "overview": t("nav_overview", lang), "map": t("nav_map", lang),
            "mm": t("nav_mm", lang), "density": t("nav_density", lang),
            "coverage": t("nav_coverage", lang), "reco": t("nav_reco", lang),
        }[k],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"**{t('filters', lang)}**")
    all_regions = sorted(synth_pref["region"].unique())
    sel_regions = st.multiselect(t("region_filter", lang), all_regions, default=all_regions)
    sel_operators = st.multiselect(t("operator_filter", lang), ["Moov", "Togocom"], default=["Moov", "Togocom"])

    GRAN_LABEL_KEYS = {"region": "gran_region", "prefecture": "gran_prefecture", "commune": "gran_commune", "canton": "gran_canton"}
    sel_gran = st.select_slider(
        t("granularity", lang), options=GRAN_LEVELS,
        value="prefecture", format_func=lambda k: t(GRAN_LABEL_KEYS[k], lang),
    )
    _ops_summary = (", ".join(sel_operators) if sel_operators else "—")
    st.caption(f"🗺️ {t(GRAN_LABEL_KEYS[sel_gran], lang)} · 📡 {_ops_summary} · 🌍 {len(sel_regions)}/{len(all_regions)}")

    st.markdown("---")
    st.caption(t("source_note", lang))

    st.caption(t("author", lang))

st.markdown(inject_css(theme), unsafe_allow_html=True)

# ==================== FILTRAGE (région + opérateur) ====================
sel_regions_eff = sel_regions if sel_regions else []
sel_operators_eff = sel_operators if sel_operators else []

ag_f = agences[agences["region"].isin(sel_regions_eff) & agences["operateur"].isin(sel_operators_eff)]
dc_f = datacenters[datacenters["region"].isin(sel_regions_eff)]

if set(sel_operators_eff) >= {"Moov", "Togocom"}:
    mm_f = mm[mm["region"].isin(sel_regions_eff)]
elif sel_operators_eff:
    mask = mm["operateur"].apply(lambda x: any(op in x for op in sel_operators_eff))
    mm_f = mm[mm["region"].isin(sel_regions_eff) & mask]
else:
    mm_f = mm.iloc[0:0]

GRAN_LABEL = t(GRAN_LABEL_KEYS[sel_gran], lang)
OPS_LABEL = ", ".join(sel_operators_eff) if sel_operators_eff and len(sel_operators_eff) < 2 else t("operators_all", lang)
REGIONS_LABEL = ", ".join(sel_regions_eff) if sel_regions_eff and len(sel_regions_eff) < len(all_regions) else t("all", lang)

# Agrégation au niveau de granularité choisi (pages Carte, Mobile Money, Couverture)
agg = with_population(aggregate_table(ag_f, mm_f, dc_f, sel_gran), sel_gran, synth_pref, synth_region)
# Agrégation fixe au niveau préfecture (seul niveau où la population est connue) — page Densité
agg_pref = with_population(aggregate_table(ag_f, mm_f, dc_f, "prefecture"), "prefecture", synth_pref, synth_region)
agg_region = with_population(aggregate_table(ag_f, mm_f, dc_f, "region"), "region", synth_pref, synth_region)
# Agrégation géographique (centroïdes) pour la carte de couverture
geo_f = aggregate_geo(mm_f, ag_f, sel_gran)
HULLS = region_hulls(mm)
REGION_COLORS = {"Maritime": "#006A4E", "Plateaux": "#FFCE00", "Centrale": "#D21034", "Kara": "#0B3D2E", "Savanes": "#7E57C2"}

PLOT_KW = dict(template=T["plot_template"], paper_bgcolor=T["bg"], plot_bgcolor=T["bg"], font_color=T["text"])

def md_to_html(text):
    # Remplace **texte** par <b>texte</b>
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    
def region_context_traces():
    """Traces de contour de région (enveloppe convexe) à insérer en fond de carte —
    calculées à partir de nos propres données, aucune dépendance réseau/fichier externe."""
    traces = []
    for region, (lons, lats) in HULLS.items():
        color = REGION_COLORS.get(region, "#999999")
        traces.append(go.Scatter(
            x=lons, y=lats, mode="lines", fill="toself",
            fillcolor=color + "1F", line=dict(color=color, width=1.2),
            name=region, hoverinfo="skip", showlegend=False,
        ))
    return traces


def plain_map_layout(fig, height):
    fig.update_layout(
        height=height, margin=dict(l=0, r=0, t=10, b=0), **PLOT_KW,
        legend=dict(orientation="h", y=1.06),
        xaxis=dict(title="Longitude", showgrid=True, gridcolor=T["grid"], zeroline=False),
        yaxis=dict(title="Latitude", showgrid=True, gridcolor=T["grid"], zeroline=False,
                    scaleanchor="x", scaleratio=1),
    )
    return fig


def kpi_card(col, value, label):
    with col:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div></div>""", unsafe_allow_html=True)


def header(title, subtitle=None):
    st.markdown(f"""<div class="header-band">
        <img src="data:image/png;base64,{SEAL_B64}" style="height:56px;margin-right:16px;border-radius:6px;">
        <div><h2 style="margin:0;">{title}</h2>{f'<p style="margin:0;opacity:0.9;">{subtitle}</p>' if subtitle else ''}</div>
        </div>""", unsafe_allow_html=True)


def how_to_read(what, shows, source=None):
    with st.expander(t("how_to_read", lang)):
        st.markdown(f"**{t('what_it_is', lang)}** — {what}")
        st.markdown(f"**{t('what_it_shows', lang)}** — {shows}")
        if source:
            st.markdown(f"**{t('source', lang)}** — {source}")


def analysis_box(md_text):
    html_text = md_to_html(md_text)
    st.markdown(f'<div class="insight-card">{html_text}</div>', unsafe_allow_html=True)


# ==================== PAGE: OVERVIEW ====================
if page == "overview":
    header(t("app_title", lang), t("app_subtitle", lang))
    st.markdown(t("ov_welcome", lang))
    st.caption("ℹ️ " + ("Les chiffres ci-dessous sont des totaux nationaux issus des données ouvertes et ne varient pas avec les filtres. Les données ouvertes ne présentent aucune agence CANAL+ — Utilisez les autres pages pour explorer par région/opérateur/granularité." if lang == "fr" else "The numbers below are national totals got from the open data and do not change with the filters. The open  data don't present any CANAL+ agency — Use the other pages to explore by region/operator/granularity."))
    st.markdown("###")

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, f"{kpis['population_totale']:,.0f}".replace(",", " "), t("kpi_population", lang))
    kpi_card(c2, kpis["nb_agences_total"], t("kpi_agences", lang))
    kpi_card(c3, kpis["nb_datacenters"], t("kpi_datacenters", lang))
    kpi_card(c4, f"{kpis['nb_agents_mobile_money']:,.0f}".replace(",", " "), t("kpi_mm", lang))

    c5, c6 = st.columns(2)
    kpi_card(c5, f"{kpis['nb_cantons_sans_agence']} / {kpis['nb_cantons_total']}", t("kpi_cantons_sans_agence", lang))
    kpi_card(c6, f"{kpis['nb_communes_sans_agence']} / {kpis['nb_communes_total']}", t("kpi_communes_sans_agence", lang))

    st.markdown("###")
    st.subheader(t("ov_findings_title", lang))
    for k in ["ov_f1", "ov_f2", "ov_f3", "ov_f4", "ov_f5"]:
        st.markdown(f'<div class="insight-card">{t(k, lang)}</div>', unsafe_allow_html=True)

# ==================== PAGE: MAP (agences + datacenters) ====================
elif page == "map":
    header(t("nav_map", lang))
    st.markdown(t("map_intro", lang))

    st.markdown(f"#### 🗺️ {t('map_title', lang)}")
    if ag_f.empty and dc_f.empty:
        st.warning(t("all", lang))
    else:
        fig = go.Figure()
        for op, color in [("Moov", OP_COLORS["Moov"]), ("Togocom", OP_COLORS["Togocom"])]:
            d = ag_f[ag_f["operateur"] == op]
            fig.add_trace(go.Scattermap(lat=d["lat"], lon=d["lon"], mode="markers",
                                         marker=dict(size=9, color=color), name=op,
                                         text=d["nom"], hoverinfo="text"))
        fig.add_trace(go.Scattermap(lat=datacenters["lat"], lon=datacenters["lon"], mode="markers",
                                     marker=dict(size=16, color=OP_COLORS["Datacenter"], symbol="star"),
                                     name="Datacenter", text=datacenters["nom"], hoverinfo="text"))
        fig.update_layout(map=dict(style=T["map_style"], center=dict(lat=8.6, lon=1.0), zoom=6.2),
                           height=560, margin=dict(l=0, r=0, t=0, b=0), **PLOT_KW,
                           legend=dict(orientation="h", y=1.02))
        st.plotly_chart(fig, width='stretch')
    how_to_read(t("map_how_what", lang), t("map_how_shows", lang))

    # ---- Analyse dynamique liée à l'objectif 1 ----
    nb_ag, nb_moov, nb_togocom, nb_dc = len(ag_f), (ag_f["operateur"] == "Moov").sum(), (ag_f["operateur"] == "Togocom").sum(), len(dc_f)
    n_units = agg[LEVEL_COLS[sel_gran][-1]].nunique() if not agg.empty else 0
    concentration = ""
    if not ag_f.empty:
        rc = ag_f.groupby("region").size().sort_values(ascending=False)
        top_region, top_count = rc.index[0], rc.iloc[0]
        top_pct = round(top_count / nb_ag * 100)
        concentration = t("map_concentration_txt", lang).format(top_region=top_region, top_pct=top_pct)
    analysis_box(t("map_dynamic_insight", lang).format(
        regions=REGIONS_LABEL, ops=OPS_LABEL, nb_ag=nb_ag, nb_moov=nb_moov, nb_togocom=nb_togocom,
        nb_dc=nb_dc, n_units=n_units, level=GRAN_LABEL.lower(), concentration=concentration,
    ))

    st.markdown("###")
    st.subheader(t("table_title_dynamic", lang).format(level=GRAN_LABEL))
    show_cols = LEVEL_COLS[sel_gran] + ["nb_agences_moov", "nb_agences_togocom", "nb_agences", "nb_datacenters"]
    if agg["population"].notna().any():
        show_cols += ["population"]
    st.dataframe(agg[show_cols] if not agg.empty else agg, width='stretch', hide_index=True)

# ==================== PAGE: MOBILE MONEY ====================
elif page == "mm":
    header(t("nav_mm", lang))
    st.markdown(t("mm_intro", lang))

    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown(f"##### {t('mm_by_operator', lang)}")
        if mm_f.empty:
            st.warning(t("all", lang))
        else:
            op_counts = mm_f["operateur"].value_counts().reset_index()
            op_counts.columns = ["operateur", "count"]
            fig = px.pie(op_counts, names="operateur", values="count", hole=0.5,
                         color_discrete_sequence=[T["green"], T["yellow"], T["red"], "#7E57C2"])
            fig.update_layout(**PLOT_KW, height=380)
            st.plotly_chart(fig, width='stretch')
    with c2:
        has_pop = sel_gran in ("region", "prefecture") and agg["population"].notna().any()
        if has_pop:
            st.markdown(f"##### {t('mm_rate_title', lang)}")
            d = agg.sort_values("agents_mm_pour_10k_hab")
            ylab = LEVEL_COLS[sel_gran][-1]
            fig = px.bar(d, x="agents_mm_pour_10k_hab", y=ylab, orientation="h",
                         color="agents_mm_pour_10k_hab", color_continuous_scale=["#D21034", T["yellow"], T["green"]])
            fig.update_layout(**PLOT_KW, height=max(380, 24 * len(d)), coloraxis_showscale=False,
                               yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig, width='stretch')
        else:
            st.info(t("mm_no_pop_note", lang).format(level=GRAN_LABEL.lower()))
            ylab = LEVEL_COLS[sel_gran][-1]
            d = agg.sort_values("nb_agents_mobile_money", ascending=False).head(20)
            st.markdown(f"##### {t('mm_raw_count_title', lang).format(level=GRAN_LABEL.lower())}")
            fig = px.bar(d.sort_values("nb_agents_mobile_money"), x="nb_agents_mobile_money", y=ylab, orientation="h",
                         color_discrete_sequence=[T["green"]])
            fig.update_layout(**PLOT_KW, height=max(380, 24 * len(d)))
            st.plotly_chart(fig, width='stretch')
    how_to_read(t("mm_how_what", lang), t("mm_how_shows", lang))

    # ---- Analyse dynamique liée à l'objectif 2 ----
    nb_mm = len(mm_f)
    tot_pop_sel = agg_region["population"].sum() if not agg_region.empty else 0
    rate = round(nb_mm / tot_pop_sel * 10000, 1) if tot_pop_sel else 0
    national_rate = round(kpis["nb_agents_mobile_money"] / kpis["population_totale"] * 10000, 1)
    gap_txt = ""
    above_national_txt = ""
    if sel_gran in ("region", "prefecture") and agg["population"].notna().any():
        namecol = LEVEL_COLS[sel_gran][-1]
        r = agg.dropna(subset=["agents_mm_pour_10k_hab"]).sort_values("agents_mm_pour_10k_hab")
        if len(r) > 1:
            gap_txt = t("mm_gap_txt", lang).format(
                min_reg=r.iloc[0][namecol], min_rate=r.iloc[0]["agents_mm_pour_10k_hab"],
                max_reg=r.iloc[-1][namecol], max_rate=r.iloc[-1]["agents_mm_pour_10k_hab"],
            )
        if len(r) > 0:
            n_above = (r["agents_mm_pour_10k_hab"] >= national_rate).sum()
            pct_above = round(n_above / len(r) * 100)
            above_national_txt = t("mm_above_national_txt", lang).format(
                pct=pct_above, level=GRAN_LABEL.lower(), national_rate=national_rate,
            )
    analysis_box(t("mm_dynamic_insight", lang).format(
        rate=rate, national_rate=national_rate, nb_mm=nb_mm, gap_txt=gap_txt, above_national_txt=above_national_txt,
    ))

# ==================== PAGE: DENSITY ====================
elif page == "density":
    header(t("nav_density", lang))
    st.markdown(t("density_intro", lang))
    st.info(t("density_gran_note", lang))

    no_ag_df = agg_pref[agg_pref["nb_agences"] == 0]
    no_ag = no_ag_df["population"].sum()
    c1, c2 = st.columns(2)
    kpi_card(c1, f"{no_ag:,.0f}".replace(",", " "), t("no_agency_pop", lang))
    kpi_card(c2, len(no_ag_df), t("gran_prefecture", lang) + " — 0 " + t("kpi_agences", lang))

    st.markdown("###")
    st.markdown(f"##### {t('scatter_title', lang)}")
    if agg_pref.empty:
        st.warning(t("all", lang))
    else:
        fig = px.scatter(agg_pref, x="population", y="nb_agences", size="nb_agents_mobile_money",
                          color="region", hover_name="prefecture", size_max=45,
                          color_discrete_sequence=[T["green"], T["yellow"], T["red"], "#1E88E5", "#7E57C2"])
        fig.update_layout(**PLOT_KW, height=520)
        st.plotly_chart(fig, width='stretch')
    how_to_read(t("scatter_how_what", lang), t("scatter_how_shows", lang))

    # ---- Analyse dynamique liée à l'objectif 3 ----
    n_pref = len(agg_pref)
    n_zero = len(no_ag_df)
    tot_pop = agg_pref["population"].sum() if not agg_pref.empty else 0
    pct_zero = round(no_ag / tot_pop * 100) if tot_pop else 0
    analysis_box(t("density_dynamic_insight", lang).format(
        n_pref=n_pref, n_zero=n_zero, pop_zero=f"{no_ag:,.0f}".replace(",", " "), pct_zero=pct_zero,
    ))

    st.subheader(t("table_density", lang))
    st.dataframe(agg_pref.sort_values("population", ascending=False), width='stretch', hide_index=True)

# ==================== PAGE: COVERAGE ====================
elif page == "coverage":
    header(t("nav_coverage", lang))
    st.info(t("coverage_disclaimer", lang))

    n_units = len(geo_f)
    n_zero_ag = int((geo_f["nb_agences"] == 0).sum()) if not geo_f.empty else 0
    pct_covered = round((geo_f["nb_agents_mm"] > 0).sum() / n_units * 100) if n_units else 0

    c1, c2 = st.columns(2)
    kpi_card(c1, f"{n_zero_ag} / {n_units}", t("coverage_kpi_gran", lang).format(
        level=GRAN_LABEL.lower()))
    kpi_card(c2, f"{pct_covered}%", t("coverage_kpi_mm_pct", lang))

    st.markdown("###")
    st.markdown(f"##### {t('coverage_map_title', lang)}")
    
    if geo_f.empty:
        st.warning(t("all", lang))
    else:
        # Colonne de nom selon la granularité choisie
        namecol = LEVEL_COLS[sel_gran][-1]
    
        # Création de la figure avec scatter_mapbox pour bénéficier du fond cartographique SIG
        fig = px.scatter_map(
            geo_f,
            lat="lat",
            lon="lon",
            color="nb_agents_mm",
            size="nb_agents_mm",
            hover_name=namecol,
            hover_data={"nb_agences": True, "lat": False, "lon": False},
            color_continuous_scale=["#D21034", T["yellow"], T["green"]],
            size_max=22,
            zoom=5.8
        )
    
        # Mise en forme du fond cartographique standard
        fig.update_layout(
            map=dict(
                style=T["map_style"],   # style défini dans vos paramètres (ex: "carto-positron", "open-street-map")
                center=dict(lat=8.6, lon=1.0)  # centre du Togo
            ),
            height=580,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            **PLOT_KW
        )
    
        # Affichage dans Streamlit
        st.plotly_chart(fig, width='stretch')

    how_to_read(t("coverage_how_what", lang), t("coverage_how_shows", lang))

    # ---- Analyse dynamique liée à l'objectif 4 ----
    analysis_box(t("coverage_dynamic_insight", lang).format(
        level=GRAN_LABEL.lower(), pct_covered=pct_covered, n_units=n_units, n_zero_ag=n_zero_ag,
    ))

# ==================== PAGE: RECOMMENDATIONS ====================
elif page == "reco":
    header(t("nav_reco", lang))
    st.markdown(t("reco_intro", lang))
    st.markdown("###")

    """
    cols = st.columns(2)
    recos = [(f"reco{i}_title", f"reco{i}_body") for i in range(1, 8)]
    for i, (title_k, body_k) in enumerate(recos):
        with cols[i % 2]:
            st.markdown(f"""<div class="reco-card"><h4>{t(title_k, lang)}</h4><p>{t(body_k, lang)}</p></div>""",
                        unsafe_allow_html=True)
    """

    recos = [(f"reco{i}_title", f"reco{i}_body") for i in range(1, 8)]
    for i, (title_k, body_k) in enumerate(recos):
        st.markdown(f"""<div class="reco-card"><h4>{t(title_k, lang)}</h4><p>{t(body_k, lang)}</p></div>""",
                    unsafe_allow_html=True)

st.markdown("---")
st.caption(t("footer_note", lang))
