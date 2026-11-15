"""Application Streamlit : résultats du notebook et estimation d'un profil."""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

import rapport as r

st.set_page_config(page_title="Gravité des accidents de la route", layout="centered")
st.markdown(r.CSS, unsafe_allow_html=True)

CHEMIN_MODELE = Path("modele/modele_gravite.joblib")
if not CHEMIN_MODELE.exists():
    st.error("Modèle introuvable. Exécute d'abord le notebook (Run All Cells) : il enregistre modele/modele_gravite.joblib.")
    st.stop()

# Résultats mesurés dans le notebook sur le jeu de test (24 997 personnes, dont 4 499 graves).
# Les faux positifs et les vrais négatifs sont déduits de la précision et de l'effectif : ils servent au dessin, pas aux textes.
TP, FN, PERSONNES, PRECISION = 3040, 1459, 24997, 0.518
FP = round(TP * (1 / PRECISION - 1))
RESULTATS = {
    "tp": TP, "fn": FN, "fp": FP, "tn": PERSONNES - TP - FN - FP, "personnes": PERSONNES,
    "recall": 0.676, "precision": PRECISION, "f1": 0.587, "pr_auc": 0.595, "pr_auc_sans_secu": 0.580,
    "accuracy": 0.829, "accuracy_toujours_pas_grave": 0.820, "taux_de_graves": 0.180, "seuil": 0.64,
}


@st.cache_resource
def charger():
    return joblib.load(CHEMIN_MODELE)


paquet = charger()
modele, seuil, colonnes, defauts = paquet["pipeline"], paquet["seuil"], paquet["colonnes"], paquet["defauts"]
R = dict(RESULTATS, seuil=seuil)
c = r.repartition(R)
txt = r.textes(R, c)

# --- ouverture : 100 personnes -----------------------------------------------------------------
st.markdown(f'<div class="hero"><h1>{txt["titre"]}</h1><p>{txt["chapo"]}</p></div>', unsafe_allow_html=True)
gauche, droite = st.columns([5, 6], gap="large")
with droite:
    vue = st.radio("Vue", r.ETATS, label_visibility="collapsed")
    etat = r.ETATS.index(vue)
    st.markdown(f'<p class="etat">{r.phrase_etat(c, etat)}</p>', unsafe_allow_html=True)
    st.markdown(r.cles(c, etat), unsafe_allow_html=True)
    st.markdown(f'<p class="legende" style="margin-top:1.2rem !important">{txt["echelle"]}</p>', unsafe_allow_html=True)
with gauche:
    st.markdown(r.carres(c, etat), unsafe_allow_html=True)

# --- bilan -------------------------------------------------------------------------------------
st.markdown(f"## {txt['h_bilan']}")
gauche, droite = st.columns(2, gap="medium")
with gauche:
    st.markdown(f'<div class="bloc jaune"><div class="n">{txt["rappel"]}</div><p>{txt["t_rappel"]}</p></div>', unsafe_allow_html=True)
with droite:
    st.markdown(f'<div class="bloc noir"><div class="n">{txt["juste"]}</div><p>{txt["t_juste"]}</p></div>', unsafe_allow_html=True)
st.markdown(f'<p class="legende" style="margin-top:1.6rem !important">{txt["accuracy"]}</p>', unsafe_allow_html=True)

# --- robustesse --------------------------------------------------------------------------------
st.markdown(f"## {txt['h_robuste']}")
st.markdown(txt["p_robuste"])
st.markdown(r.robustesse(R), unsafe_allow_html=True)

# --- estimer un cas ----------------------------------------------------------------------------
# Codes issus de la documentation ONISR (BAAC)
CATU = {"Conducteur": "1", "Passager": "2", "Piéton": "3"}
SEXE = {"Masculin": "1", "Féminin": "2"}
CATV = {"Voiture": "7", "Vélo": "1", "Cyclomoteur": "2", "Utilitaire": "10", "Scooter (moins de 50 cm³)": "30",
        "Moto (50 à 125 cm³)": "31", "Moto (plus de 125 cm³)": "33", "Poids lourd (plus de 7,5 t)": "14", "Autobus": "37",
        "Trottinette à moteur": "50", "Vélo à assistance électrique": "80"}
LUM = {"Plein jour": "1", "Aube ou crépuscule": "2", "Nuit, sans éclairage public": "3",
       "Nuit, éclairage public éteint": "4", "Nuit, éclairage public allumé": "5"}
ATM = {"Normale": "1", "Pluie légère": "2", "Pluie forte": "3", "Neige ou grêle": "4", "Brouillard ou fumée": "5",
       "Vent fort ou tempête": "6", "Temps couvert": "8"}
SURF = {"Normale": "1", "Mouillée": "2", "Flaques": "3", "Enneigée": "5", "Verglacée": "7"}
CATR = {"Autoroute": "1", "Route nationale": "2", "Route départementale": "3", "Voie communale": "4",
        "Route de métropole urbaine": "7"}
AGG = {"En agglomération": "2", "Hors agglomération": "1"}
SECU1 = {"Ceinture": "1", "Casque": "2", "Aucun équipement": "0", "Dispositif enfant": "3", "Gilet réfléchissant": "4"}
JOURS = {"Lundi": "0", "Mardi": "1", "Mercredi": "2", "Jeudi": "3", "Vendredi": "4", "Samedi": "5", "Dimanche": "6"}

st.markdown("## Estimer un cas")
st.markdown("Choisis un profil : le modèle calcule son score. Les variables qui ne sont pas proposées ici prennent leur valeur la plus fréquente.")
gauche, droite = st.columns([5, 6], gap="large")
with gauche:
    age = st.slider("Âge", 0, 100, 35)
    sexe = st.selectbox("Sexe", list(SEXE))
    catu = st.selectbox("Usager", list(CATU))
    secu1 = st.selectbox("Équipement de sécurité", list(SECU1))
    catv = st.selectbox("Véhicule", list(CATV))
with droite:
    zone_resultat = st.empty()
    heure = st.slider("Heure de l'accident", 0, 23, 12)
    jour = st.selectbox("Jour de la semaine", list(JOURS))
    lum = st.selectbox("Luminosité", list(LUM))
    atm = st.selectbox("Météo", list(ATM))
    catr = st.selectbox("Type de route", list(CATR), index=2)
    vma = st.selectbox("Vitesse maximale autorisée (km/h)", [20, 30, 50, 70, 80, 90, 110, 130], index=2)
    surf = st.selectbox("État de la chaussée", list(SURF))
    agg = st.selectbox("Localisation", list(AGG))

ligne = dict(defauts)
ligne.update({
    "age": float(age), "heure": float(heure), "vma": float(vma), "sexe": SEXE[sexe], "catu": CATU[catu],
    "secu1": SECU1[secu1], "catv": CATV[catv], "jour_semaine": JOURS[jour], "lum": LUM[lum], "atm": ATM[atm],
    "catr": CATR[catr], "surf": SURF[surf], "agg": AGG[agg],
})
score = float(modele.predict_proba(pd.DataFrame([ligne], columns=colonnes))[0, 1])
zone_resultat.markdown(r.panneau(score, seuil), unsafe_allow_html=True)

# --- limites -----------------------------------------------------------------------------------
st.markdown("## Ce que ces résultats ne disent pas")
a, b = st.columns(2, gap="large")
with a:
    st.markdown("Plusieurs variables (obstacle heurté, point de choc, type de collision) ne sont connues qu'après l'accident. "
                "Le modèle aide donc à comprendre la gravité d'accidents déjà survenus ; il ne prévoit pas un risque avant qu'il se produise.")
    st.markdown("Le critère « grave » regroupe les personnes tuées et hospitalisées. La définition d'« hospitalisé » a changé en 2018.")
with b:
    st.markdown("Une seule année (2023) et un seul découpage entre apprentissage et test : il n'y a pas d'intervalle de confiance. "
                "Corrélation ne veut pas dire causalité : le casque, par exemple, est associé à plus de cas graves parce qu'il concerne les deux-roues motorisés.")

# --- suite -------------------------------------------------------------------------------------
st.markdown("## Aller plus loin")
st.markdown("Le notebook complet, avec la démarche et les résultats, est dans le dépôt "
            "[projet-accidents-routiers](https://github.com/Gaya-014/projet-accidents-routiers). "
            "La version industrialisée, sur cinq années (PostgreSQL, dbt, Docker), est dans "
            "[pipeline-accidents](https://github.com/Gaya-014/pipeline-accidents).")
st.markdown('<p class="legende">Bases annuelles des accidents corporels de la circulation routière, ONISR / ministère de l\'Intérieur, '
            'licence ouverte (data.gouv.fr).</p>', unsafe_allow_html=True)
