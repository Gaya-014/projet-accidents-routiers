"""Textes, HTML et styles de la page (projet notebook). Aucune dépendance à Streamlit."""

BLEU, JAUNE, ROUGE, NOIR, GRIS, PISTE = "#1148B8", "#FFC400", "#E63B2E", "#111827", "#D3DAE5", "#DCE2EC"
FIN = " "  # espace fine insécable
ETATS = ["La réalité", "Les alertes du modèle", "Les deux ensemble"]


def nb(n):
    return f"{int(round(n)):,}".replace(",", FIN)


def dec(x, d=3):
    return f"{x:.{d}f}".replace(".", ",")


def pct(x):
    return f"{round(x * 100)}{FIN}%"


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Archivo+Black&display=swap');
[data-testid="stAppDeployButton"], #MainMenu, footer {display:none !important;}
.stApp, div[data-testid="stMarkdownContainer"] p, label, .stSelectbox, .stSlider {font-family: 'Archivo', 'Helvetica Neue', Arial, sans-serif;}
.block-container {max-width: 1000px !important; padding-top: 2.2rem !important; padding-bottom: 6rem !important;}
div[data-testid="stMarkdownContainer"] h1, div[data-testid="stMarkdownContainer"] h2 {
  font-family: 'Archivo Black', 'Arial Black', Impact, sans-serif !important; font-weight: 400 !important; color: #111827; letter-spacing: -0.01em;}
div[data-testid="stMarkdownContainer"] h2 {font-size: 2.3rem !important; line-height: 1.08 !important; margin: 4.6rem 0 1rem 0 !important; padding: 0 !important; max-width: 17em;}
div[data-testid="stMarkdownContainer"] p {font-size: 1.15rem; line-height: 1.65; max-width: 38em; color: #1F2937;}
div[data-testid="stMarkdownContainer"] p.legende {font-size: 1rem !important; color: #4B5563; line-height: 1.55 !important;}

/* bandeau d'ouverture */
.hero {background:#1148B8; padding: 3.2rem 2.8rem 2.8rem 2.8rem; margin-bottom: 2.6rem;}
div[data-testid="stMarkdownContainer"] .hero h1 {font-family:'Archivo Black', Impact, sans-serif !important; font-weight:400 !important; color:#fff !important;
  font-size: 3.5rem !important; line-height: 1.03 !important; margin: 0 0 1.4rem 0 !important; padding:0 !important; max-width: 14em;}
div[data-testid="stMarkdownContainer"] .hero p {color:#fff !important; font-size: 1.3rem !important; line-height:1.55 !important; max-width: 31em !important; margin:0;}
div[data-testid="stMarkdownContainer"] .hero p.etiquette {font-size:1rem !important; color:#FFC400 !important; margin-top: 1.6rem; font-weight:600;}
div[role="radiogroup"] label p {font-size: 1.05rem !important; font-weight: 500;}
div[data-testid="stMarkdownContainer"] p.etat {font-family:'Archivo Black', sans-serif; font-weight:400; font-size: 1.55rem !important; line-height:1.2 !important; margin: 1.2rem 0 1.2rem 0; color:#111827;}

/* grille de 100 carrés : 1 carré = 1 personne sur 100 */
.carres {display:grid; grid-template-columns: repeat(10, 1fr); gap: 6px; max-width: 470px;}
.carres i {display:block; aspect-ratio:1; border-radius:3px; background:#D3DAE5; opacity:0; animation: apparait .35s ease forwards; animation-delay: calc(var(--i) * 9ms);}
.carres i.tp {background: var(--tp);} .carres i.fn {background: var(--fn);}
.carres i.fp {background: var(--fp); box-shadow: inset 0 0 0 3px var(--fpb);} .carres i.tn {background:#D3DAE5;}
.carres.e0 {--tp:#E63B2E; --fn:#E63B2E; --fp:#D3DAE5; --fpb:#D3DAE5;}
.carres.e1 {--tp:#FFC400; --fn:#D3DAE5; --fp:#FFC400; --fpb:#FFC400;}
.carres.e2 {--tp:#FFC400; --fn:#E63B2E; --fp:#fff; --fpb:#111827;}
@keyframes apparait {to {opacity:1;}}
@media (prefers-reduced-motion: reduce) {.carres i {animation:none; opacity:1;}}
.cles {display:flex; flex-direction:column; gap:.55rem; font-size:1.08rem; color:#111827; margin: .4rem 0 0 0;}
.cles span {display:flex; align-items:center; gap:.7rem;}
.cles b {display:inline-block; width:1.15rem; height:1.15rem; border-radius:3px; flex:none;}

/* gros chiffres : deux aplats */
.bloc {padding: 1.8rem 2rem 1.6rem 2rem; height: 100%;}
.bloc.jaune {background:#FFC400; color:#111827;} .bloc.noir {background:#111827; color:#fff;}
.bloc .n {font-family:'Archivo Black', Impact, sans-serif; font-size: 5.6rem; line-height: .95; margin: 0 0 .8rem 0;}
div[data-testid="stMarkdownContainer"] .bloc p {font-size:1.12rem; line-height:1.55; margin:0; color:inherit;}

/* barres de comparaison */
.cmp {margin: 1.4rem 0 .4rem 0; max-width: 42rem;}
.cmp .metrique {font-weight:600; font-size:1.1rem; margin: 0 0 .5rem 0;}
.cmp .ligne {display:grid; grid-template-columns: 13rem 1fr 3.8rem; align-items:center; gap:.9rem; margin:.55rem 0; font-size:1.05rem;}
.cmp .piste {height:1.5rem; background:#DCE2EC;}
.cmp .piste span {display:block; height:100%;}
.cmp .val {text-align:right; font-variant-numeric: tabular-nums; font-weight:600;}

/* estimation : le bloc change de couleur selon l'alerte */
.panneau {padding: 1.8rem 1.9rem 1.5rem 1.9rem; color:#fff;}
.panneau.alerte {background:#E63B2E;} .panneau.calme {background:#1148B8;}
.panneau .score {font-family:'Archivo Black', Impact, sans-serif; font-size:5.2rem; line-height:.95; margin:0;}
.panneau .verdict {font-weight:600; font-size:1.35rem; line-height:1.25; margin:.6rem 0 0 0;}
.route {position:relative; height: 1.9rem; background: rgba(0,0,0,.28); margin: 2.2rem 0 3.4rem 0;}
.route::before {content:""; position:absolute; left:0; right:0; top:calc(50% - 2px); height:4px;
  background: repeating-linear-gradient(90deg, #fff 0 18px, transparent 18px 36px); opacity:.9;}
.route .vehicule {position:absolute; top:50%; width:1.7rem; height:1.7rem; border-radius:50%; transform:translate(-50%,-50%); background:#FFC400; border:3px solid #111827;}
.route .seuil {position:absolute; top:-.7rem; bottom:-.7rem; width:3px; background:#fff;}
.route .seuil span {position:absolute; top:100%; left:50%; transform:translateX(-50%); font-size:.95rem; white-space:nowrap; margin-top:.2rem; color:#fff;}
div[data-testid="stMarkdownContainer"] .panneau p {color:#fff; font-size:1rem; line-height:1.5;}
div[data-testid="stMarkdownContainer"] .panneau p.score {font-size:5.2rem; line-height:.95;}
div[data-testid="stMarkdownContainer"] .panneau p.verdict {font-size:1.35rem; line-height:1.25;}

@media (max-width: 760px) {
  .hero {padding: 2rem 1.4rem;} div[data-testid="stMarkdownContainer"] .hero h1 {font-size: 2.3rem !important;}
  div[data-testid="stMarkdownContainer"] h2 {font-size: 1.8rem !important; margin-top: 3.2rem !important;}
  .bloc .n {font-size: 4.2rem;} .cmp .ligne {grid-template-columns: 8rem 1fr 3.4rem;}
}
</style>
"""


def repartition(t, total=100):
    """Ramène les 4 cases de la matrice de confusion à `total` carrés (méthode du plus fort reste)."""
    vals = {k: t[k] for k in ("tp", "fn", "fp", "tn")}
    s = sum(vals.values())
    brut = {k: v * total / s for k, v in vals.items()}
    base = {k: int(b) for k, b in brut.items()}
    for k in sorted(brut, key=lambda k: brut[k] - base[k], reverse=True)[: total - sum(base.values())]:
        base[k] += 1
    return base


def carres(c, etat):
    ordre = {0: ["tp", "fn", "fp", "tn"], 1: ["tp", "fp", "fn", "tn"], 2: ["tp", "fn", "fp", "tn"]}[etat]
    tuiles = "".join(f'<i class="{k}" style="--i:{i}"></i>' for i, k in enumerate(k for k in ordre for _ in range(c[k])))
    return f'<div class="carres e{etat}" role="img" aria-label="100 carrés représentant 100 personnes">{tuiles}</div>'


def cles(c, etat):
    def p(style, texte):
        return f'<span><b style="{style}"></b>{texte}</span>'
    if etat == 0:
        e = [p(f"background:{ROUGE}", f"{c['tp'] + c['fn']} tuées ou hospitalisées"), p(f"background:{GRIS}", f"{c['fp'] + c['tn']} indemnes ou légèrement blessées")]
    elif etat == 1:
        e = [p(f"background:{JAUNE}", f"{c['tp'] + c['fp']} alertes du modèle"), p(f"background:{GRIS}", f"{c['fn'] + c['tn']} personnes sans alerte")]
    else:
        e = [p(f"background:{JAUNE}", f"{c['tp']} cas graves détectés"), p(f"background:{ROUGE}", f"{c['fn']} cas graves manqués"),
             p(f"background:#fff;box-shadow:inset 0 0 0 3px {NOIR}", f"{c['fp']} fausses alertes"), p(f"background:{GRIS}", f"{c['tn']} personnes justement écartées")]
    return '<div class="cles">' + "".join(e) + "</div>"


def phrase_etat(c, etat):
    return [
        f"{c['tp'] + c['fn']} personnes sur 100 ont été tuées ou hospitalisées.",
        f"Le modèle a déclenché {c['tp'] + c['fp']} alertes sur ces 100 personnes.",
        f"Sur {c['tp'] + c['fn']} cas graves, il en voit {c['tp']} et en rate {c['fn']}, et il se trompe sur {c['fp']} personnes.",
    ][etat]


def textes(R, c):
    """Textes de la page, calculés à partir des résultats du notebook (dictionnaire R)."""
    graves = R["tp"] + R["fn"]
    return {
        "titre": f"Sur 100 personnes impliquées dans un accident, {c['tp'] + c['fn']} sont tuées ou hospitalisées",
        "chapo": (f"Données 2023 de l'ONISR. Un modèle a été entraîné pour retrouver ces cas graves, puis testé sur {nb(R['personnes'])} personnes "
                  f"mises de côté (20{FIN}% des données, séparées par accident). Voici ce qu'il voit, et ce qu'il rate."),
        "echelle": f"Un carré représente environ {nb(R['personnes'] / 100)} personnes du jeu de test.",
        "h_bilan": "Ce que le modèle trouve, ce qu'il signale à tort",
        "rappel": pct(R["recall"]),
        "t_rappel": f"des cas graves sont détectés : {nb(R['tp'])} sur {nb(graves)}. Les {nb(R['fn'])} autres passent sous le radar.",
        "juste": pct(R["precision"]),
        "t_juste": (f"des alertes sont justes. Autrement dit, environ une alerte sur deux est fausse. Le seuil de décision ({dec(R['seuil'], 2)}) "
                    f"a été choisi sur un jeu de validation, jamais sur le test."),
        "accuracy": (f"Le taux de bonnes réponses ({pct(R['accuracy'])}) ne dit presque rien ici : un modèle qui répondrait toujours « pas grave » "
                     f"en obtiendrait {pct(R['accuracy_toujours_pas_grave'])}, parce que seulement {pct(R['taux_de_graves'])} des cas sont graves."),
        "h_robuste": "Sans l'équipement de sécurité, le modèle garde l'essentiel de son score",
        "p_robuste": (f"L'équipement de sécurité (ceinture, casque) est la variable la plus utilisée par le modèle, et ses cases « non renseigné » "
                      f"sont presque toujours associées à des cas non graves. Pour vérifier que le modèle ne se limite pas à elles, il a été réentraîné sans ces variables : "
                      f"la PR-AUC passe de {dec(R['pr_auc'])} à {dec(R['pr_auc_sans_secu'])}. Ce test ne permet pas de séparer l'effet réel de l'équipement "
                      f"de la façon dont la fiche est remplie. Pour la PR-AUC, le hasard donnerait {dec(R['taux_de_graves'], 2)}."),
    }


def robustesse(R):
    lignes = [("Avec toutes les variables", R["pr_auc"], BLEU), ("Sans l'équipement de sécurité", R["pr_auc_sans_secu"], JAUNE),
              ("Hasard", R["taux_de_graves"], "#9AA6B8")]
    blocs = "".join(
        f'<div class="ligne"><span>{n}</span><span class="piste"><span style="width:{v * 100:.1f}%;background:{col}"></span></span>'
        f'<span class="val">{dec(v)}</span></div>' for n, v, col in lignes)
    return f'<div class="cmp"><div class="metrique">PR-AUC sur le jeu de test</div>{blocs}</div>'


def route(score, seuil):
    return (f'<div class="route" role="img" aria-label="Score {dec(score, 2)}, seuil {dec(seuil, 2)}">'
            f'<div class="seuil" style="left:{min(seuil, 1) * 100:.1f}%"><span>seuil {dec(seuil, 2)}</span></div>'
            f'<div class="vehicule" style="left:{min(max(score, 0.02), 0.98) * 100:.1f}%"></div></div>')


def panneau(score, seuil):
    alerte = score >= seuil
    verdict = "Le modèle déclenche une alerte" if alerte else "Le modèle ne déclenche pas d'alerte"
    return (f'<div class="panneau {"alerte" if alerte else "calme"}"><p class="score">{dec(score, 2)}</p>'
            f'<p class="verdict">{verdict}</p>{route(score, seuil)}'
            f'<p style="margin:0">Le score n\'est pas une probabilité : le modèle donne plus de poids aux cas graves à l\'entraînement. '
            f'Il sert à classer les profils entre eux.</p></div>')
