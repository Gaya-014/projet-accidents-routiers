# Fiche de révision : projet « Gravité des accidents de la route »

À lire avant d'envoyer ce projet à quelqu'un ou de passer un entretien. Chaque point : **ce que j'ai fait, pourquoi, et comment le dire simplement.**

## L'histoire du projet en 30 secondes
« J'ai pris les données ouvertes des accidents corporels de la route en France (fichier BAAC, 4 fichiers CSV par année). J'ai relié les 4 fichiers, nettoyé les données, regardé quelles circonstances sont liées aux accidents graves, puis entraîné et comparé plusieurs modèles pour prédire si une personne est gravement blessée. Comme les cas graves sont rares (environ 18 %), j'ai évalué avec la precision, le recall et le F1, et pas seulement l'accuracy. »

## Les idées à savoir expliquer

| # | Idée | Pourquoi |
|---|---|---|
| 1 | **4 fichiers reliés par `Num_Acc`** (et `id_vehicule`) | Les infos sont réparties : l'accident, le lieu, les véhicules, les personnes. Je les joins comme en SQL pour avoir une ligne par personne. |
| 2 | **Un seul lieu par accident** | `lieux` a plus de lignes que d'accidents (carrefours). Sans correction, la jointure dupliquerait des accidents. Je garde la ligne à la vitesse autorisée la plus élevée (hypothèse, à citer comme limite). |
| 3 | **`validate="many_to_one"`** | Sécurité : pandas s'arrête si la jointure crée des doublons. |
| 4 | **`-1` = valeur manquante déguisée** | Pandas ne le voit pas comme vide. Je le traite à part : catégorie « non renseigné » pour les codes, valeur manquante pour les nombres. |
| 5 | **Valeurs aberrantes** | Âge hors de 0-100, vitesse hors de 5-130, etc. : impossibles, donc remplacées par une valeur manquante. |
| 6 | **Colonnes supprimées** | Identifiants (inutiles pour prédire), colonnes presque vides, localisations trop précises. |
| 7 | **Label binaire « grave »** | Tué + hospitalisé contre indemne + blessé léger. Les « tués » (2,7 %) sont trop rares pour un modèle à 4 classes. Limite : on mélange deux gravités. |
| 8 | **Supervisé + classification** | J'ai le label (supervisé), et je prédis une catégorie (classification). Pas une série temporelle : chaque personne est un exemple indépendant. |
| 9 | **Séparation par accident** (`GroupShuffleSplit`) | Les personnes d'un même accident se ressemblent. Si elles sont des deux côtés, le modèle « reconnaît » l'accident et le score est trop optimiste. |
| 10 | **Séparer AVANT de standardiser** | Sinon la moyenne et l'écart-type utilisent le test : fuite d'information (*data leakage*). |
| 11 | **Standardisation et one-hot** | Standardiser : moyenne 0, écart-type 1, pour que les grandes valeurs (vitesse) ne dominent pas. One-hot : une colonne 0/1 par catégorie, sinon le modèle croit que le code 5 est « plus grand » que le code 1. |
| 12 | **L'accuracy ne suffit pas** | Un modèle qui répond toujours « pas grave » a environ 82 % d'accuracy. |
| 13 | **Precision, recall, F1, PR-AUC** | Precision : parmi ceux appelés « graves », combien le sont vraiment. Recall : parmi les vrais graves, combien sont trouvés. F1 : compromis entre les deux. PR-AUC : qualité du classement, sans choisir de seuil. |
| 14 | **Déséquilibre** | `class_weight` (plus de poids aux graves), sous-échantillonnage, sur-échantillonnage, SMOTE (exemples synthétiques). Toujours **sur le train seulement**. |
| 15 | **Hyperparamètres** | Réglages choisis avant l'entraînement (profondeur, nombre d'arbres...). Recherche aléatoire avec validation croisée **en groupes** (`GroupKFold`). |
| 16 | **Courbe de validation / sur-apprentissage** | Si le score du train monte mais pas celui de la validation, le modèle apprend par cœur. |
| 17 | **Seuil de décision** | Par défaut 0,5, mais pas optimal quand les graves sont rares. Je le choisis sur la validation (max du F1), jamais sur le test. |
| 18 | **Le test n'est ouvert qu'à la fin** | C'est le seul score honnête. Je ne règle rien avec. |
| 19 | **Pipeline sauvegardé** | Préparation + modèle dans un seul objet (`joblib`) : mêmes transformations en production. |
| 20 | **Parquet plutôt que CSV** | Plus petit, plus rapide, garde les types des colonnes. |

## Questions d'entretien probables
- **« Explique-moi ton projet. »** → l'histoire en 30 secondes ci-dessus.
- **« Quelle a été la partie la plus difficile ? »** → la jointure des fichiers (doublons dans `lieux`) et le choix d'évaluation avec des classes déséquilibrées.
- **« Pourquoi pas de deep learning ? »** → données tabulaires avec des catégories : les modèles à base d'arbres sont en général très performants et plus faciles à expliquer.
- **« Comment sais-tu que ton modèle ne triche pas ? »** → séparation par accident, standardisation apprise sur le train, test ouvert une seule fois à la fin.
- **« Quelles sont les limites ? »** → regroupement tué/hospitalisé, hypothèse sur la ligne de lieu gardée, localisation non exploitée, données d'une seule année au départ, définition de « hospitalisé » modifiée en 2018.
- **« Comment l'améliorer ? »** → plus d'années, localisation, XGBoost/LightGBM, seuil selon le coût réel d'une erreur.
- **« Qu'est-ce qui t'a aidée à faire ce projet ? »** → réponds franchement (documentation, outils d'IA pour écrire du code, etc.) et montre que tu sais **expliquer chaque choix**. C'est ça qu'on vérifie.

## Mini-glossaire
- **Label / cible** : ce qu'on veut prédire (`grave`).
- **Variables / features** : les informations données au modèle.
- **Train / validation / test** : apprendre / choisir et régler / évaluer une seule fois à la fin.
- **Sur-apprentissage** : le modèle apprend le train par cœur et généralise mal.
- **Hyperparamètre** : réglage fait avant l'entraînement.
- **Pipeline** : enchaînement préparation des données → modèle, dans un seul objet.
