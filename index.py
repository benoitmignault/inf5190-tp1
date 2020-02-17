from flask import Flask, render_template, request, redirect, url_for, session

from .function import *

app = Flask(__name__, static_url_path='', static_folder='static')

# Déclaration de la secret key pour me permettre utiliser les variables de sessions
app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/', methods=["GET"])
def home():
    # Si indicateur est vrai, on détruit les cookies, sinon on fait rien de spécial
    if session.get('reset_cookie'):
        if session['reset_cookie']:
            session.clear()

    # Initialisation peu importe s'il y a des variabes sessions
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    conn_db = get_db()

    # On vérifi s'il y avait des variables de type session qui aurait été crée part une recherche d'article introuvable
    # On commence par le titre
    if session.get('titre'):
        titre = session['titre']
    else:
        titre = "Présentation"

    # On doit valider si j'ai cette indicateur à True
    if session.get('aucun_article_trouve'):
        liste_validation['aucun_article_trouve'] = True

    # On poursuit pour vérifier s'il y avait un ensemble qu'on avait préalablement récupérer
    if session.get('ensemble_recent'):
        # Et si on a un ensemble trouvé, ce qui veut dire que nous n'avons pas trouvé article
        ensemble_recent = session['ensemble_recent']
        # Comprendre pourquoi il y a un double triage lorsque je reviens d'une recherche qui a rien donnée
    else:
        ensemble_recent = conn_db.get_articles_recents()

    # On peut maintenant calculer le nombre d'articles récents trouvé peu importe d'où vient l'ensemble récent
    liste_champs['nb_article_recent'] = len(ensemble_recent)
    if liste_champs['nb_article_recent'] == 0:
        liste_validation['aucun_article_recent'] = True

    liste_validation = situation_erreur(liste_validation)
    liste_champs['messages'] = message_erreur(liste_validation)

    return render_template('home.html', titre=titre, liste_validation=liste_validation,
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
        ensemble_recent = conn_db.get_articles_recents()
        session['titre'] = "Problème avec la recherche !"
        session['ensemble_recent'] = ensemble_recent
        session['aucun_article_trouve'] = liste_validation['aucun_article_trouve']
        return redirect(url_for('.home'))

    else:
        # Utilisation des variables de sessions pour transporter
        # les données nécessaire dans le traitement de la route /recherche_article_trouve
        session['titre'] = "Recherche réussi !"
        session['ensemble_trouve'] = ensemble_trouve
        session['liste_champs'] = liste_champs
        return redirect(url_for('.recherche_article_trouve'))


@app.route('/recherche_article_trouve', methods=["GET"])
def recherche_article_trouve():
    # On récupère ici les informations sauvegardées dans les sessions de variables
    titre = session['titre']
    ensemble_trouve = session['ensemble_trouve']
    liste_champs = session['liste_champs']
    # Ceci est un indicateur pour détruire les cookies
    # Pour éviter d'avoir de vieux message erreur dans la page accueil
    session['reset_cookie'] = True
    return render_template("recherche_trouve.html", titre=titre, ensemble_trouve=ensemble_trouve,
                           liste_champs=liste_champs)


@app.route('/article/<identifiant>')
def article_selectionner(identifiant):
    conn_db = get_db()
    ensemble_trouve = conn_db.get_articles_selectionner(identifiant)
    session['reset_cookie'] = True  # Si nous revenons à la page d'accueil par cette route, on détruit les cookies

    if len(ensemble_trouve) > 0:
        return render_template("article_selectionner.html", titre="Information sur l'article",
                               ensemble_trouve=ensemble_trouve)
    else:
        return redirect(url_for('.article_inexistante'))


@app.route('/admin', methods=["GET"])
def admin():
    session.clear()  # On delete les cookies pour éviter d'aller consulter le mauvais article
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    conn_db = get_db()
    ensembles = conn_db.get_all_articles()
    liste_champs['nb_article'] = len(ensembles)
    if liste_champs['nb_article'] == 0:
        liste_validation['aucun_article'] = True

    liste_validation = situation_erreur(liste_validation)
    liste_champs['messages'] = message_erreur(liste_validation)

    return render_template("admin.html", titre="Admin", ensembles=ensembles, liste_champs=liste_champs,
                           liste_validation=liste_validation)


@app.route('/admin-modif/<identifiant>', methods=["GET"])
def admin_modif_article(identifiant):
    # On doit toujours revalider si l'identifiant est toujours valide avant de poursuivre
    conn_db = get_db()
    article_a_modifier = conn_db.get_articles_selectionner(identifiant)
    if len(article_a_modifier) > 0:
        validation_erreur = False  # Ça nous indiquera quels types de messages afficher
        titre = ""

        if session.get('situation_erreur') or session.get('modification_reussi'):
            article_a_modifier = session['liste_champs_admin']
            liste_validation_admin = session['liste_validation_admin']

            if session.get('situation_erreur') and session['situation_erreur']:
                titre = "Modification en Erreur !"
                validation_erreur = True

            if session.get('modification_reussi') and session['modification_reussi']:
                titre = "Modification réussi !"

            return render_template("admin_modif_selectionner.html", titre=titre, article_a_modifier=article_a_modifier,
                                   liste_validation_admin=liste_validation_admin,
                                   validation_erreur=validation_erreur)
        # Ce qui veut dire on arrive pour la première sur cette route
        else:

            liste_validation_admin = initial_champ_validation_admin()
            titre = "Modification en cours"
            return render_template("admin_modif_selectionner.html", titre=titre, article_a_modifier=article_a_modifier,
                                   liste_validation_admin=liste_validation_admin,
                                   validation_erreur=validation_erreur)

    else:
        return redirect(url_for('.admin_modif_inexistant'))


@app.route('/admin-modif/article_modification', methods=["POST"])
def admin_modification_article_en_cours():
    liste_champs_admin = initial_champ_admin()  # Création de la liste d'information nécessaire
    liste_validation_admin = initial_champ_validation_admin()
    # On utilise la fonction pour les besoin de l'administrateur
    liste_champs_admin = remplissage_champs_admin(request, liste_champs_admin, "admin_modif")
    liste_validation_admin = validation_champs_admin(liste_champs_admin, liste_validation_admin)
    liste_validation_admin = situation_erreur(liste_validation_admin)

    if liste_validation_admin['situation_erreur'] and liste_validation_admin['aucune_modification']:
        liste_champs_admin['messages'] = message_erreur_admin(liste_validation_admin)
        # On doit mettre la valeur contraire
        # Lorsque nous avons une erreur, on doit mettre à True l'indicateur erreur et à False indicateur réussi
        session['situation_erreur'] = True
        session['modification_reussi'] = False
        session['liste_validation_admin'] = liste_validation_admin
        session['liste_champs_admin'] = liste_champs_admin
        return redirect(url_for('.admin_modif_article', identifiant=liste_champs_admin['identifiant']))

    else:
        conn_db = get_db()
        conn_db.update_article(liste_champs_admin['identifiant'], liste_champs_admin['titre'],
                               liste_champs_admin['paragraphe'])
        liste_validation_admin['update_reussi'] = True
        liste_champs_admin['messages'] = message_erreur_admin(liste_validation_admin)
        # On doit mettre la valeur contraire
        # Lorsque nous avons une erreur, on doit mettre à False l'indicateur erreur et à True indicateur réussi
        session['modification_reussi'] = True
        session['situation_erreur'] = False
        session['liste_validation_admin'] = liste_validation_admin
        session['liste_champs_admin'] = liste_champs_admin

        return redirect(url_for('.admin_modif_article', identifiant=liste_champs_admin['identifiant']))


@app.route('/admin-nouveau', methods=["GET"])
def admin_nouveau():
    # Lorsque nous arrivons ici, on doit supprimer les cookies
    # ayant pas encore été supprimés car ils ne seront plus nécessaire ici
    session.clear()
    page_ajout_article = True  # Seulement ici est sera mise à vrai pour les besoins du formulaire ajout d'article
    return render_template("admin_nouveau.html", titre="Ajout d'article", page_ajout_article=page_ajout_article)


@app.route('/admin-nouveau/article_ajout', methods=["POST"])
def admin_nouveau_ajout():
    conn_db = get_db()
    liste_champs_admin = initial_champ_admin()  # Création de la liste d'information nécessaire
    liste_validation_admin = initial_champ_validation_admin()
    liste_champs_admin = remplissage_champs_admin(request, liste_champs_admin, "admin_nouveau")
    article_verifier = conn_db.get_articles_selectionner(liste_champs_admin['identifiant'])
    if len(article_verifier) > 0:
        liste_validation_admin['identifiant_deja_prise'] = True

    print(liste_validation_admin['identifiant_deja_prise'])
    return "Allo"


@app.route('/article/')
def article_inexistante():
    session.clear()  # Rendu ici, je dois killer mes cookies car j'en ai plus besoin !
    return render_template("erreur_404.html", titre="Page inexistante - 404", erreur_404=True), 404


@app.route('/admin-modif/')
def admin_modif_inexistant():
    session.clear()  # Rendu ici, je dois killer mes cookies car j'en ai plus besoin !
    return render_template("erreur_404.html", titre="Page inexistante - 404", erreur_404=True), 404
