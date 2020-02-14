from flask import Flask, render_template, request, redirect, url_for, session

from .function import *

app = Flask(__name__, static_url_path='', static_folder='static')

app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/', methods=["GET"])
def home():
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    conn_db = get_db()

    # Les quatre lignes suivantes pourrait être mise dans une fonction plutard
    ensemble_recent = conn_db.get_articles_recents()
    liste_champs['nb_article_recent'] = len(ensemble_recent)
    if liste_champs['nb_article_recent'] == 0:
        liste_validation['aucun_article_recent'] = True
    # Fin du bloque des 4 lignes

    liste_validation = situation_erreur(liste_validation)
    liste_champs['messages'] = message_erreur(liste_validation)
    return render_template('home.html', titre="Présentation", liste_validation=liste_validation,
                           ensemble_recent=ensemble_recent, liste_champs=liste_champs)


@app.route('/recherche', methods=["POST"])
def recherche_article():
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    liste_champs = remplissage_champs(request.form, liste_champs)
    liste_validation = validation_champs(liste_champs, liste_validation)
    conn_db = get_db()
    ensemble_trouve = {}
    if not liste_validation['champ_recher_article_vide']:
        ensemble_trouve = conn_db.get_articles_trouvees(liste_champs['recher_article'])
        liste_champs['nb_article_trouve'] = len(ensemble_trouve)

        if liste_champs['nb_article_trouve'] == 0:
            liste_validation['aucun_article_trouve'] = True

    liste_validation = situation_erreur(liste_validation)
    if liste_validation['situation_erreur']:
        # Les quatre lignes suivantes pourrait être mise dans une fonction plutard
        ensemble_recent = conn_db.get_articles_recents()
        liste_champs['nb_article_recent'] = len(ensemble_recent)
        if liste_champs['nb_article_recent'] == 0:
            liste_validation['aucun_article_recent'] = True
        # Fin du bloque des 4 lignes

        liste_champs['messages'] = message_erreur(liste_validation)
        return render_template("home.html", titre="Problème avec la recherche", ensemble_recent=ensemble_recent,
                               liste_validation=liste_validation, liste_champs=liste_champs)
    else:
        session['titre'] = "Recherche réussi !"
        session['ensemble_trouve'] = ensemble_trouve
        session['liste_champs'] = liste_champs
        return redirect(
            url_for('.recherche_article_trouve'))


@app.route('/recherche_article_trouve/')
def recherche_article_trouve():
    titre = session['titre']
    ensemble_trouve = session['ensemble_trouve']
    liste_champs = session['liste_champs']
    return render_template("recherche_trouve.html", titre=titre, ensemble_trouve=ensemble_trouve,
                           liste_champs=liste_champs)
