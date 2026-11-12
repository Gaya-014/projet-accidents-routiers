import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gravité d'un accident de la route", page_icon="🚗")


@st.cache_resource
def charger():
    return joblib.load("modele/modele_gravite.joblib")


paquet = charger()
modele = paquet["pipeline"]
seuil = paquet["seuil"]
colonnes = paquet["colonnes"]
defauts = paquet["defauts"]

# codes d'après la documentation ONISR (BAAC) : à confirmer dans le PDF de description des bases
CATU = {"Conducteur": "1", "Passager": "2", "Piéton": "3"}
SEXE = {"Masculin": "1", "Féminin": "2"}
CATV = {"Voiture (VL)": "7", "Vélo": "1", "Cyclomoteur": "2", "Utilitaire (VU)": "10", "Scooter < 50 cm3": "30",
        "Moto 50-125 cm3": "31", "Moto > 125 cm3": "33", "Poids lourd > 7,5 t": "14", "Autobus": "37",
        "Trottinette à moteur": "50", "Vélo à assistance électrique": "80"}
LUM = {"Plein jour": "1", "Crépuscule ou aube": "2", "Nuit sans éclairage public": "3",
       "Nuit, éclairage public éteint": "4", "Nuit, éclairage public allumé": "5"}
ATM = {"Normale": "1", "Pluie légère": "2", "Pluie forte": "3", "Neige - grêle": "4", "Brouillard - fumée": "5",
       "Vent fort - tempête": "6", "Temps couvert": "8"}
SURF = {"Normale": "1", "Mouillée": "2", "Flaques": "3", "Enneigée": "5", "Verglacée": "7"}
CATR = {"Autoroute": "1", "Route nationale": "2", "Route départementale": "3", "Voie communale": "4",
        "Route de métropole urbaine": "7"}
AGG = {"En agglomération": "2", "Hors agglomération": "1"}
SECU1 = {"Ceinture": "1", "Casque": "2", "Aucun équipement": "0", "Dispositif enfants": "3", "Gilet réfléchissant": "4"}
JOURS = {"Lundi": "0", "Mardi": "1", "Mercredi": "2", "Jeudi": "3", "Vendredi": "4", "Samedi": "5", "Dimanche": "6"}

st.title("Prédire la gravité d'un accident de la route")
st.write("Projet réalisé avec les données BAAC 2023 (data.gouv.fr). Renseigne quelques informations : "
         "le modèle estime un **score de risque** que la personne soit gravement blessée (hospitalisée ou tuée).")
st.warning("Projet pédagogique : ce n'est pas un outil de décision. Les autres informations sont remplies "
           "avec des valeurs courantes.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("La personne")
    age = st.slider("Âge", 0, 100, 35)
    sexe = st.selectbox("Sexe", list(SEXE))
    catu = st.selectbox("Catégorie d'usager", list(CATU))
    secu1 = st.selectbox("Équipement de sécurité", list(SECU1))
    st.subheader("Le véhicule")
    catv = st.selectbox("Type de véhicule", list(CATV))
with col2:
    st.subheader("Les circonstances")
    heure = st.slider("Heure de l'accident", 0, 23, 12)
    jour = st.selectbox("Jour de la semaine", list(JOURS))
    lum = st.selectbox("Luminosité", list(LUM))
    atm = st.selectbox("Météo", list(ATM))
    st.subheader("La route")
    catr = st.selectbox("Catégorie de route", list(CATR), index=2)
    vma = st.selectbox("Vitesse maximale autorisée (km/h)", [20, 30, 50, 70, 80, 90, 110, 130], index=2)
    surf = st.selectbox("État de la chaussée", list(SURF))
    agg = st.selectbox("Localisation", list(AGG))

if st.button("Estimer la gravité"):
    ligne = dict(defauts)
    ligne.update({
        "age": float(age), "heure": float(heure), "vma": float(vma),
        "sexe": SEXE[sexe], "catu": CATU[catu], "secu1": SECU1[secu1], "catv": CATV[catv],
        "jour_semaine": JOURS[jour], "lum": LUM[lum], "atm": ATM[atm],
        "catr": CATR[catr], "surf": SURF[surf], "agg": AGG[agg],
    })
    X = pd.DataFrame([ligne], columns=colonnes)
    score = float(modele.predict_proba(X)[0, 1])

    st.metric("Score de risque (0 à 1)", f"{score:.2f}")
    st.progress(min(max(score, 0.0), 1.0))
    if score >= seuil:
        st.error("Le modèle classe cette situation comme GRAVE (hospitalisation ou décès).")
    else:
        st.success("Le modèle classe cette situation comme PAS GRAVE.")
    st.caption(f"Seuil de décision du modèle : {seuil:.2f}. Le score n'est pas une probabilité exacte : "
               "le modèle a été entraîné en donnant plus de poids aux cas graves, qui sont rares.")
