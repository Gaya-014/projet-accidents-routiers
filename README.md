# Prédire la gravité des accidents de la route en France

Projet de data science de bout en bout sur les données ouvertes des accidents corporels de la circulation (fichier BAAC, 2023) : récupération de données brutes, nettoyage, exploration, modélisation et petite application web.

**Objectif** : prédire si une personne impliquée dans un accident est **gravement blessée** (hospitalisée ou tuée) à partir des circonstances de l'accident, du lieu, du véhicule et de la personne.

## Résultats

Évaluation sur un jeu de test de 24 997 personnes (dont 4 499 graves), séparé **par accident** pour éviter qu'un même accident soit à la fois dans le train et dans le test.

| Mesure | Valeur |
|---|---|
| PR-AUC | **0,595** (0,180 pour le hasard) |
| ROC-AUC | 0,869 |
| Recall (graves) | 0,676 : 3 040 graves trouvés sur 4 499 |
| Precision (graves) | 0,518 : environ une alerte sur deux est fausse |
| F1 (graves) | 0,587 |
| Accuracy | 0,829 (0,820 pour un modèle qui répond toujours « pas grave ») |

Le jeu est déséquilibré (18 % de graves) : **l'accuracy est trompeuse**, donc l'évaluation s'appuie sur le recall, la precision, le F1 et la PR-AUC.

**Modèle final** : Gradient Boosting (`HistGradientBoostingClassifier`) avec `class_weight='balanced'` et un seuil de décision de 0,64, choisi sur la validation (jamais sur le test).

**Test de robustesse** : sans les variables d'équipement de sécurité (`secu1` et `secu2`), la PR-AUC passe de 0,595 à 0,580. Le modèle ne dépend donc pas seulement de ces variables.

## Démarche

1. **Données brutes** : 4 fichiers CSV par année (caractéristiques, lieux, véhicules, usagers) à relier. Gestion d'un fichier `lieux` à plusieurs lignes par accident (choix documenté), jointures sécurisées avec `validate="many_to_one"`.
2. **Nettoyage** : valeurs `-1` (non renseigné), colonnes à virgule décimale lues comme du texte, valeurs aberrantes (âge, vitesse), colonnes quasi vides, nouvelles variables (âge, heure, jour de la semaine). Sauvegarde en CSV et Parquet.
3. **EDA** : taux de personnes graves selon le véhicule, l'usager, la route, la luminosité, l'heure, l'âge, la vitesse autorisée, l'équipement de sécurité.
4. **Séparation puis standardisation** : `GroupShuffleSplit` par accident, standardisation et one-hot appris sur le train seulement (pas de fuite d'information).
5. **Déséquilibre** : comparaison de `class_weight`, sous-échantillonnage, sur-échantillonnage aléatoire et SMOTE (uniquement sur le train).
6. **Modèles** : régression logistique, arbre de décision, Random Forest, Gradient Boosting, comparés à un modèle de référence (Dummy).
7. **Réglages** : critère gini/entropie, recherche aléatoire avec validation croisée en groupes (`GroupKFold`), courbe de validation (sur-apprentissage).
8. **Analyse finale** : matrice de confusion, courbe precision-recall, importance des variables par permutation, test de robustesse sans les variables d'équipement de sécurité.
9. **Sauvegarde et application web** : pipeline complet sauvegardé avec `joblib`, application Streamlit.

## Limites

- Plusieurs variables (point de choc, obstacle heurté, type de collision) ne sont connues qu'après l'accident : le modèle **explique** la gravité d'accidents déjà arrivés, il ne prévoit pas le risque avant.
- Les valeurs « non renseigné » sont presque jamais graves (0 % pour le sexe, 2,8 % pour l'équipement de sécurité), et l'équipement de sécurité domine l'importance des variables. Le test de robustesse (PR-AUC de 0,580 sans ces variables) montre que le modèle tient, mais il ne permet pas de séparer l'effet réel de l'équipement de l'effet de la façon dont la fiche est remplie.
- Corrélation n'est pas causalité (par exemple, le casque est associé à plus de cas graves parce qu'il concerne les deux-roues motorisés).
- Le label regroupe « tué » et « hospitalisé » ; la définition de « hospitalisé » a changé en 2018.
- Une seule année (2023) et un seul découpage train/test : pas d'intervalle de confiance.
- Le score de l'application n'est pas une probabilité exacte (le modèle donne plus de poids aux cas graves).

## Structure du dépôt

```
accidents_routiers_final.ipynb   # le notebook complet, avec les résultats
app.py                           # application web Streamlit
requirements.txt                 # bibliothèques utilisées
fiche_revision.md                # explication de chaque choix, en mots simples
modele/modele_gravite.joblib     # modèle sauvegardé (pipeline + seuil)
```

Les données ne sont pas dans le dépôt (fichiers trop lourds) : les 4 fichiers CSV de l'année voulue sont à télécharger sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/53698f4ca3a729239d2036df/) et à placer dans un dossier `donnees_brutes/`.

## Lancer le projet

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter lab                       # ouvrir le notebook et faire Run All Cells
streamlit run app.py              # application web (après avoir exécuté le notebook)
```

## Source des données

Bases de données annuelles des accidents corporels de la circulation routière, ONISR / Ministère de l'Intérieur, licence ouverte (data.gouv.fr).