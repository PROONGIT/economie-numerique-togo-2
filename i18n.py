# -*- coding: utf-8 -*-
"""Dictionnaire de traduction FR/EN. Usage : t("cle", lang)"""

TR = {
    # --- Général / navigation ---
    "republic_name": {"fr": "République Togolaise",
                      "en": "Republic of Togo"},
    "app_title": {"fr": "Accès aux Télécoms & Services Numériques — Togo",
                  "en": "Telecom & Digital Services Access — Togo"},
    "app_subtitle": {"fr": "Diagnostic ouvert des infrastructures télécoms et priorités d'extension de la connectivité",
                      "en": "Open diagnostic of telecom infrastructure and connectivity expansion priorities"},
    "nav_title": {"fr": "Navigation", "en": "Navigation"},
    "nav_overview": {"fr": "🏠 Vue d'ensemble", "en": "🏠 Overview"},
    "nav_map": {"fr": "🗼 Agences & Datacenters", "en": "🗼 Agencies & Datacenters"},
    "nav_mm": {"fr": "📱 Mobile Money", "en": "📱 Mobile Money"},
    "nav_density": {"fr": "👥 Densité vs Infrastructures", "en": "👥 Density vs Infrastructure"},
    "nav_coverage": {"fr": "📶 Couverture & Zones blanches", "en": "📶 Coverage & Dead Zones"},
    "nav_reco": {"fr": "🎯 Recommandations", "en": "🎯 Recommendations"},
    "language": {"fr": "Langue", "en": "Language"},
    "theme": {"fr": "Thème", "en": "Theme"},
    "theme_light": {"fr": "Clair", "en": "Light"},
    "theme_dark": {"fr": "Sombre", "en": "Dark"},
    "filters": {"fr": "Filtres", "en": "Filters"},
    "granularity": {"fr": "Granularité géographique", "en": "Geographic granularity"},
    "gran_region": {"fr": "Région", "en": "Region"},
    "gran_prefecture": {"fr": "Préfecture", "en": "Prefecture"},
    "gran_commune": {"fr": "Commune", "en": "Commune"},
    "gran_canton": {"fr": "Canton", "en": "Canton"},
    "region_filter": {"fr": "Région(s)", "en": "Region(s)"},
    "operator_filter": {"fr": "Opérateur(s)", "en": "Operator(s)"},
    "all": {"fr": "Toutes", "en": "All"},
    "source_note": {"fr": "Sources : géodonnées ouvertes agences/datacenters/agents mobile money (2026) ; population RGPH-5, INSEED, résultats définitifs, novembre 2022.",
                     "en": "Sources: open geodata on agencies/datacenters/mobile money agents (2026); population from RGPH-5 census, INSEED, final results, November 2022."},
    "author": {"fr": "Auteur : AZIAGBEDO KOKOU SODJINE, Ingénieur en Sciences informatiques, Sécurité informatique - Data & IA",
                "en": "Author: AZIAGBEDO KOKOU SODJINE, Engineer in Computer Science, IT Security - Data & AI"},
    "how_to_read": {"fr": "❓ Comment lire ce graphique", "en": "❓ How to read this chart"},
    "what_it_is": {"fr": "De quoi il s'agit", "en": "What this is"},
    "what_it_shows": {"fr": "Ce que ça montre", "en": "What it shows"},
    "source": {"fr": "Source", "en": "Source"},
    "finding": {"fr": "📍 Constat", "en": "📍 Finding"},

    # --- Overview ---
    "ov_welcome": {"fr": "Ce tableau de bord dresse un diagnostic de l'accès aux télécommunications et aux services numériques au Togo, à partir des géodonnées ouvertes sur les agences opérateurs, les datacenters, les agents mobile money et la population par préfecture (RGPH-5, 2022). Utilisez le menu à gauche pour naviguer entre les analyses.",
                    "en": "This dashboard diagnoses access to telecommunications and digital services in Togo, based on open geodata on operator agencies, datacenters, mobile money agents and population by prefecture (RGPH-5, 2022). Use the menu on the left to navigate between analyses."},
    "kpi_population": {"fr": "Population totale (RGPH-5)", "en": "Total population (census)"},
    "kpi_agences": {"fr": "Agences Moov + Togocom", "en": "Moov + Togocom agencies"},
    "kpi_datacenters": {"fr": "Datacenters", "en": "Datacenters"},
    "kpi_mm": {"fr": "Agents mobile money", "en": "Mobile money agents"},
    "kpi_cantons_sans_agence": {"fr": "Cantons sans agence opérateur", "en": "Cantons without an operator agency"},
    "kpi_communes_sans_agence": {"fr": "Communes sans agence opérateur", "en": "Communes without an operator agency"},
    "ov_findings_title": {"fr": "Les 5 constats majeurs", "en": "5 key findings"},
    "ov_f1": {"fr": "**Réseau physique très concentré** : 90 agences Moov + Togocom pour tout le pays (le fichier « Télécom » fourni est la fusion des deux ; CANAL+ n'a pas d'agence géoréférencée dans ce jeu de données ouvert), dont près de 60% (51/90) situées dans la seule région Maritime (Lomé inclus).",
              "en": "**Highly concentrated physical network**: 90 Moov + Togocom agencies nationwide (the supplied \"Télécom\" file is the merge of both; CANAL+ has no geo-referenced agency in this open dataset), nearly 60% (51/90) located in the Maritime region alone (including Lomé)."},
    "ov_f2": {"fr": "**87,6% des cantons togolais (326/372) n'ont aucune agence opérateur physique** — le maillage d'agences ne suit pas la maille administrative fine.",
              "en": "**87.6% of Togolese cantons (326/372) have no physical operator agency** — the agency network does not follow the fine administrative grid."},
    "ov_f3": {"fr": "**Le mobile money comble ce vide** : 100% des 372 cantons disposent d'au moins un agent mobile money (19 788 points au total), un maillage bien plus fin que celui des agences classiques.",
              "en": "**Mobile money fills this gap**: 100% of the 372 cantons have at least one mobile money agent (19,788 points total), a much finer network than traditional agencies."},
    "ov_f4": {"fr": "**Datacenters 100% centralisés à Lomé** : les 3 datacenters recensés sont tous situés dans la préfecture du Golfe — aucune redondance régionale.",
              "en": "**Datacenters 100% centralized in Lomé**: all 3 recorded datacenters are in Golfe prefecture — no regional redundancy."},
    "ov_f5": {"fr": "**CANAL+ absent du jeu de données ouvert, mais présent sur le terrain** : aucune agence CANAL+ ne figure dans les données fournies pour ce challenge. Or le site officiel canalbox.tg recense au moins 7 boutiques dans le Grand-Lomé (Dekon, Wuiti, Agoè, Adidoadin, Adidogomé, Baguida, Sarakawa) — c'est donc un vide de données à combler, pas une absence réelle de CANAL+ sur le marché.",
              "en": "**CANAL+ missing from the open dataset, but present on the ground**: no CANAL+ agency appears in the data supplied for this challenge. Yet the official canalbox.tg website lists at least 7 stores in Greater Lomé (Dekon, Wuiti, Agoè, Adidoadin, Adidogomé, Baguida, Sarakawa) — this is a data gap to fill, not a real absence of CANAL+ from the market."},

    # --- Map tab ---
    "map_title": {"fr": "Répartition spatiale des agences Moov + Togocom et des datacenters", "en": "Spatial distribution of Moov + Togocom agencies and datacenters"},
    "map_intro": {"fr": "Chaque point représente une agence (Moov ou Togocom) ou un datacenter. CANAL+ n'a aucune agence géoréférencée dans ce jeu de données ouvert, bien que le site officiel canalbox.tg recense au moins 7 boutiques dans le Grand-Lomé — un vide de données, pas une absence réelle. Utilisez les filtres pour isoler un opérateur ou une région.",
                  "en": "Each point represents an agency (Moov or Togocom) or a datacenter. CANAL+ has no geo-referenced agency in this open dataset, although the official canalbox.tg website lists at least 7 stores in Greater Lomé — a data gap, not a real absence. Use the filters to isolate an operator or region."},
    "map_how_what": {"fr": "Carte de points géolocalisés des agences Moov (bleu), Togocom (orange) et des datacenters (rouge, triangle).",
                      "en": "Geolocated point map of Moov agencies (blue), Togocom agencies (orange) and datacenters (red triangle)."},
    "map_how_shows": {"fr": "La forte concentration des points autour de Lomé et le long de l'axe Sud, contrastant avec la rareté des points au Nord (Savanes, Kara).",
                       "en": "The strong concentration of points around Lomé and along the southern corridor, contrasting with sparse points in the North (Savanes, Kara)."},
    "table_agences_pref": {"fr": "Agences et datacenters par préfecture", "en": "Agencies and datacenters by prefecture"},

    # --- Mobile money tab ---
    "mm_title": {"fr": "Couverture des agents mobile money et adéquation à la population", "en": "Mobile money agent coverage and population fit"},
    "mm_intro": {"fr": "Le mobile money est le canal d'accès numérique le plus décentralisé du pays. Cette section évalue son adéquation avec la répartition de la population.",
                 "en": "Mobile money is the country's most decentralized digital access channel. This section assesses its fit with population distribution."},
    "mm_by_operator": {"fr": "Répartition des agents par opérateur pris en charge", "en": "Agent breakdown by operator supported"},
    "mm_rate_title": {"fr": "Agents mobile money pour 10 000 habitants, par préfecture", "en": "Mobile money agents per 10,000 inhabitants, by prefecture"},
    "mm_how_what": {"fr": "Graphique en barres du nombre d'agents mobile money rapporté à la population (pour 10 000 habitants), par préfecture.",
                     "en": "Bar chart of mobile money agents per population (per 10,000 inhabitants), by prefecture."},
    "mm_how_shows": {"fr": "Les préfectures où le taux de couverture est le plus faible relativement à leur population — cibles prioritaires pour renforcer le réseau d'agents.",
                      "en": "The prefectures with the lowest coverage rate relative to their population — priority targets to strengthen the agent network."},

    # --- Density tab ---
    "density_title": {"fr": "Densité démographique et adéquation des infrastructures", "en": "Population density and infrastructure fit"},
    "density_intro": {"fr": "Cette analyse croise la population par préfecture (RGPH-5, 2022) avec le nombre d'agences et d'agents mobile money, pour identifier les zones sur- ou sous-équipées relativement à leur poids démographique.",
                       "en": "This analysis cross-references population by prefecture (RGPH-5, 2022) with the number of agencies and mobile money agents, to identify areas over- or under-equipped relative to their population weight."},
    "scatter_title": {"fr": "Population vs nombre d'agences par préfecture", "en": "Population vs number of agencies by prefecture"},
    "scatter_how_what": {"fr": "Nuage de points : population de la préfecture (axe X) contre nombre d'agences opérateurs (axe Y), une bulle par préfecture, taille = agents mobile money.",
                          "en": "Scatter plot: prefecture population (X axis) vs number of operator agencies (Y axis), one bubble per prefecture, size = mobile money agents."},
    "scatter_how_shows": {"fr": "Les préfectures situées en bas à droite (population élevée, peu d'agences) sont prioritaires : elles concentrent beaucoup d'habitants pour très peu de points de service physiques.",
                           "en": "Prefectures in the bottom right (high population, few agencies) are priority areas: they concentrate many inhabitants for very few physical service points."},
    "no_agency_pop": {"fr": "Population vivant dans une préfecture sans aucune agence opérateur", "en": "Population living in a prefecture with no operator agency at all"},
    "table_density": {"fr": "Tableau détaillé par préfecture", "en": "Detailed table by prefecture"},

    # --- Coverage / zones blanches ---
    "coverage_title": {"fr": "Couverture réseau et zones blanches (indicateur proxy)", "en": "Network coverage and dead zones (proxy indicator)"},
    "coverage_disclaimer": {"fr": "⚠️ **Note méthodologique** : aucune donnée brute de couverture radio cellulaire (2G/3G/4G) n'est disponible en open data pour ce challenge. Cet onglet construit un **indicateur proxy** de couverture, fondé sur la présence physique d'agences et d'agents mobile money par canton — l'absence totale de point de service dans un canton est un signal de risque d'exclusion numérique, mais ne prouve pas l'absence de signal radio.",
                            "en": "⚠️ **Methodological note**: no raw cellular radio coverage data (2G/3G/4G) is available as open data for this challenge. This tab builds a **proxy indicator** of coverage, based on the physical presence of agencies and mobile money agents per canton — a canton with no service point at all is a signal of digital exclusion risk, but does not prove the absence of radio signal."},
    "coverage_kpi_cantons": {"fr": "Cantons sans aucune agence opérateur", "en": "Cantons with no operator agency"},
    "coverage_kpi_mm_pct": {"fr": "Cantons couverts par au moins 1 agent mobile money", "en": "Cantons covered by at least 1 mobile money agent"},
    "coverage_map_title": {"fr": "Carte des cantons par niveau d'équipement (proxy)", "en": "Map of cantons by equipment level (proxy)"},
    "coverage_how_what": {"fr": "Carte à points, un point par canton positionné sur son centroïde d'activité, coloré selon le nombre d'agents mobile money (proxy de présence numérique).",
                           "en": "Point map, one point per canton positioned at its activity centroid, colored by the number of mobile money agents (digital presence proxy)."},
    "coverage_how_shows": {"fr": "Les cantons en rouge/orange (faible nombre d'agents) sont les zones les plus fragiles à surveiller en priorité pour une extension de couverture réelle.",
                            "en": "Cantons in red/orange (low agent count) are the most fragile areas to prioritize for actual coverage expansion."},

    # --- Recommendations ---
    "reco_title": {"fr": "Recommandations stratégiques", "en": "Strategic recommendations"},
    "reco_intro": {"fr": "7 recommandations concrètes, organisées autour des 5 objectifs du diagnostic, pour étendre la connectivité et l'inclusion numérique.",
                   "en": "7 concrete recommendations, organized around the diagnostic's 5 objectives, to expand connectivity and digital inclusion."},

    "reco1_title": {"fr": "1. Déployer des agences dans les 12 préfectures à 0 agence", "en": "1. Roll out agencies in the 12 prefectures with zero agencies"},
    "reco1_body": {"fr": "Lacs, Vo, Est-Mono, Tandjoaré… cumulent 1,45M d'habitants sans point de vente. Ouvrir en priorité 1 agence dans les 4 préfectures les plus peuplées (Lacs, Vo, Est-Mono, Tandjoaré, >130k hab. chacune) d'ici 12 à 24 mois, puis les 8 restantes.",
                   "en": "Lacs, Vo, Est-Mono, Tandjoaré… together have 1.45M inhabitants with no sales point. Prioritize opening 1 agency in the 4 most populous prefectures (Lacs, Vo, Est-Mono, Tandjoaré, >130k inhabitants each) within 12-24 months, then the remaining 8."},

    "reco2_title": {"fr": "2. Décentraliser l'infrastructure de données", "en": "2. Decentralize data infrastructure"},
    "reco2_body": {"fr": "Les 3 datacenters du pays sont tous à Lomé. Étudier l'implantation d'un site secondaire à Kara ou Sokodé pour réduire la latence Nord et le risque de coupure nationale en cas d'incident dans la capitale.",
                   "en": "The country's 3 datacenters are all in Lomé. Study a secondary site in Kara or Sokodé to reduce northern latency and the risk of a nationwide outage from an incident in the capital."},

    "reco3_title": {"fr": "3. Renforcer le maillage mobile money là où il est le plus faible", "en": "3. Strengthen the mobile money network where it is weakest"},
    "reco3_body": {"fr": "La région Plateaux (18,8 agents/10 000 hab.) et les préfectures Kpendjal (4,6) et Mô (6,1) sont nettement sous la moyenne nationale (24,4). Objectif : campagne de recrutement d'agents pour les rapprocher de cette moyenne d'ici 18 mois.",
                   "en": "The Plateaux region (18.8 agents/10,000 inhab.) and the Kpendjal (4.6) and Mô (6.1) prefectures are well below the national average (24.4). Goal: an agent recruitment drive to close this gap within 18 months."},

    "reco4_title": {"fr": "4. Certifier les agents mobile money comme relais numériques", "en": "4. Certify mobile money agents as digital relays"},
    "reco4_body": {"fr": "100% des cantons ont un agent mobile money contre 12% pour les agences. Dans les zones sans agence, former ces agents à des services de base (inscription SIM, sensibilisation, support niveau 1) via un kit et une commission incitative.",
                   "en": "100% of cantons have a mobile money agent versus 12% for agencies. In areas without an agency, train these agents on basic services (SIM registration, awareness, level-1 support) via a starter kit and incentive commission."},

    "reco5_title": {"fr": "5. Prioriser les investissements avec un indice objectif", "en": "5. Prioritize investment with an objective index"},
    "reco5_body": {"fr": "Combiner, pour chaque préfecture, population et déficit d'agences/agents en un indice de priorité unique. L'utiliser pour arbitrer, de façon transparente et réplicable, les 10 prochaines implantations plutôt qu'un choix au cas par cas.",
                   "en": "Combine, for each prefecture, population and agency/agent deficit into a single priority index. Use it to arbitrate, transparently and repeatably, the next 10 rollouts rather than case-by-case choices."},

    "reco6_title": {"fr": "6. Lancer une remontée communautaire du signal", "en": "6. Launch community-based signal reporting"},
    "reco6_body": {"fr": "En attendant une donnée de couverture officielle, déployer un dispositif léger (SMS/USSD) dans les 12 préfectures sans agence pour que les usagers signalent la qualité du signal et cartographier les zones blanches réelles à court terme.",
                   "en": "While waiting for official coverage data, deploy a lightweight SMS/USSD tool in the 12 prefectures without an agency so users can report signal quality, mapping actual dead zones in the short term."},

    "reco7_title": {"fr": "7. Publier une carte de couverture réseau ouverte", "en": "7. Publish an open network coverage map"},
    "reco7_body": {"fr": "Nouer un partenariat avec l'ARCEP Togo et les opérateurs pour publier des données réelles de couverture 2G/3G/4G en open data — la condition de fond pour remplacer le proxy agences par une vraie carte des zones blanches.",
                   "en": "Establish a partnership with ARCEP Togo and operators to publish real 2G/3G/4G coverage data as open data — the fundamental condition to replace the agency proxy with a real dead-zone map."},
    "gran_label_of": {"fr": "par {level}", "en": "by {level}"},
    "operators_all": {"fr": "tous", "en": "all"},
    "table_title_dynamic": {"fr": "Agences, agents mobile money et datacenters — {level}", "en": "Agencies, mobile money agents and datacenters — {level}"},
    "objective_tag": {"fr": "🎯 Objectif {n}", "en": "🎯 Objective {n}"},

    "map_dynamic_insight": {
        "fr": "**Analyse de la sélection actuelle** — avec les filtres en cours (régions : {regions} · opérateur(s) : {ops}), on dénombre **{nb_ag} agences** ({nb_moov} Moov + {nb_togocom} Togocom) et **{nb_dc} datacenter(s)**, réparti(e)s sur {n_units} {level}(s) dans le tableau ci-dessous. {concentration} — **Objectif 1** : cartographier la répartition spatiale des agences opérateurs et des centres de données.",
        "en": "**Current selection analysis** — with active filters (regions: {regions} · operator(s): {ops}), there are **{nb_ag} agencies** ({nb_moov} Moov + {nb_togocom} Togocom) and **{nb_dc} datacenter(s)**, spread across {n_units} {level}(s) in the table below. {concentration} — **Objective 1**: map the spatial distribution of operator agencies and data centers.",
    },
    "map_concentration_txt": {
        "fr": "La région {top_region} concentre à elle seule {top_pct}% des agences sélectionnées",
        "en": "The {top_region} region alone accounts for {top_pct}% of selected agencies",
    },

    "mm_dynamic_insight": {
        "fr": "**Analyse de la sélection actuelle** — le taux moyen s'établit à **{rate} agents pour 10 000 habitants** sur la sélection (national : {national_rate}), pour {nb_mm} agents recensés. {gap_txt} — **Objectif 2** : analyser la couverture des services numériques (mobile money) et son adéquation avec la population.",
        "en": "**Current selection analysis** — the average rate is **{rate} agents per 10,000 inhabitants** for the selection (national: {national_rate}), for {nb_mm} recorded agents. {gap_txt} — **Objective 2**: analyze mobile money service coverage and its fit with population.",
    },
    "mm_gap_txt": {
        "fr": "L'écart type entre {min_reg} ({min_rate}) et {max_reg} ({max_rate}) montre un déséquilibre net entre territoires",
        "en": "The gap between {min_reg} ({min_rate}) and {max_reg} ({max_rate}) shows a clear imbalance between territories",
    },
    "mm_no_pop_note": {
        "fr": "ℹ️ La population n'est connue qu'au niveau **préfecture** ou **région** (RGPH-5). Au niveau {level}, le graphique ci-dessous affiche donc un **nombre brut d'agents** plutôt qu'un taux pour 10 000 habitants.",
        "en": "ℹ️ Population is only known at the **prefecture** or **region** level (census). At {level} level, the chart below therefore shows a **raw agent count** rather than a rate per 10,000 inhabitants.",
    },
    "mm_raw_count_title": {"fr": "Nombre d'agents mobile money par {level} (top 20)", "en": "Number of mobile money agents by {level} (top 20)"},

    "density_dynamic_insight": {
        "fr": "**Analyse de la sélection actuelle** — sur les **{n_pref} préfectures sélectionnées**, **{n_zero} n'ont aucune agence** opérateur, ce qui représente **{pop_zero} habitants** sans point de vente physique sur leur territoire ({pct_zero}% de la population sélectionnée). — **Objectif 3** : mettre en regard la localisation des infrastructures et la densité démographique par subdivision.",
        "en": "**Current selection analysis** — of the **{n_pref} selected prefectures**, **{n_zero} have no operator agency at all**, representing **{pop_zero} inhabitants** with no physical point of sale in their territory ({pct_zero}% of the selected population). — **Objective 3**: cross-reference infrastructure location with population density by subdivision.",
    },
    "density_gran_note": {
        "fr": "ℹ️ Cette page utilise toujours le niveau **préfecture**, seul niveau infra-régional où la population (RGPH-5) est connue — le filtre de granularité n'affecte que les pages Carte, Mobile Money et Couverture.",
        "en": "ℹ️ This page always uses the **prefecture** level, the only sub-regional level where population (census) is known — the granularity filter only affects the Map, Mobile Money and Coverage pages.",
    },

    "coverage_dynamic_insight": {
        "fr": "**Analyse de la sélection actuelle** — à la granularité **{level}**, **{pct_covered}%** des {n_units} unités sélectionnées disposent d'au moins un agent mobile money, et **{n_zero_ag} unités sur {n_units} n'ont aucune agence** opérateur physique. **Objectif 4** : évaluer la couverture du réseau et identifier les zones les plus fragiles (proxy, en l'absence de donnée radio ouverte).",
        "en": "**Current selection analysis** — at **{level}** granularity, **{pct_covered}%** of the {n_units} selected units have at least one mobile money agent, and **{n_zero_ag} out of {n_units} units have no** physical operator agency at all. **Objective 4**: assess network coverage and identify the most fragile areas (proxy, in the absence of open radio data).",
    },

    "footer_note": {"fr": "Tableau de bord réalisé dans le cadre du challenge open data — République Togolaise.", "en": "Dashboard produced for the open data challenge — Republic of Togo."},
}


def t(key, lang="fr"):
    entry = TR.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("fr", key))
