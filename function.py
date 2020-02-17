from flask import g

from .database import Database  # Importer le fichier database.py


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def initial_champ():
    liste_champs = {"nb_article": 0, "nb_article_recent": 0, "nb_article_trouve": 0, "recher_article": "",
                    "message": {}, "titre": "", "paragraphe": "", "identifiant": "", "date_publication": "",
                    "auteur": ""}

    return liste_champs


def initial_champ_admin():
    liste_champs_admin = {"titre": "", "titre_avant": "", "paragraphe": "", "paragraphe_avant": "",
                          "identifiant": "", "date_publication": "", "auteur": ""}

    return liste_champs_admin


def initial_champ_validation():
    liste_validation = {"aucun_article": False, "aucun_article_recent": False, "champ_recher_article_vide": False,
                        "aucun_article_trouve": False, "situation_erreur": False}

    return liste_validation


def initial_champ_validation_admin():
    liste_validation_admin = {"situation_erreur": False, "champ_titre_pareil": False, "champs_pareils": False,
                              "update_reussi": False, "aucune_modification": False, "champ_paragraphe_pareil": False,
                              "champs_vides": False, "champ_titre_vide": False, "champ_paragraphe_vide": False,
                              "identifiant_deja_prise": False}

    return liste_validation_admin


def remplissage_champs(formulaire, liste_champs):
    liste_champs['recher_article'] = formulaire['recher_article']

    return liste_champs


def remplissage_champs_admin(request, liste_champs_admin, route):
    liste_champs_admin['titre'] = request.form['nom_article']
    # Je dois utiliser strip pour retirer les retours de lignes non nécessaire
    liste_champs_admin['paragraphe'] = request.form['nom_paragraphe'].strip()
    liste_champs_admin['identifiant'] = request.form['identifiant']
    liste_champs_admin['date_publication'] = request.form['date_publication']
    liste_champs_admin['auteur'] = request.form['auteur']

    # Cette condition est pour éviter de la répétition de code avec le remplissage des informations venant de la route
    # /admin-nouveau/article_ajout'
    if route == "admin_modif":
        liste_champs_admin['titre_avant'] = request.form['nom_article_avant']
        liste_champs_admin['paragraphe_avant'] = request.form['nom_paragraphe_avant']

    return liste_champs_admin


def validation_champs(liste_champs, liste_validation):
    if liste_champs['recher_article'] == "":
        liste_validation['champ_recher_article_vide'] = True

    return liste_validation


def validation_champs_admin(liste_champs_admin, liste_validation_admin):
    if liste_champs_admin['titre'] == "":
        liste_validation_admin['champ_titre_vide'] = True

    if liste_champs_admin['paragraphe'] == "":
        liste_validation_admin['champ_paragraphe_vide'] = True

    if liste_validation_admin['champ_titre_vide'] or liste_validation_admin['champ_paragraphe_vide']:
        liste_validation_admin['champs_vides'] = True

    if not liste_validation_admin['champs_vides']:
        # Seulement si les champs ne sont pas vide, qu'on va poursuivre les validations de manière logique
        if liste_champs_admin['paragraphe'] == liste_champs_admin['paragraphe_avant']:
            liste_validation_admin['champ_paragraphe_pareil'] = True

        if liste_champs_admin['titre'] == liste_champs_admin['titre_avant']:
            liste_validation_admin['champ_titre_pareil'] = True

        if liste_validation_admin['champ_paragraphe_pareil'] and liste_validation_admin['champ_titre_pareil']:
            liste_validation_admin['aucune_modification'] = True

    return liste_validation_admin


# Nous allons utiliser cette focntion pour la recherche et pour la section admin
def situation_erreur(liste_validation):
    for cle, valeur in liste_validation.items():
        if valeur:
            liste_validation['situation_erreur'] = True

    return liste_validation


def message_erreur(liste_validation):
    messages = {}
    if liste_validation["champ_recher_article_vide"]:
        messages['champ_vide'] = "Le champ ne peut rester vide si vous voulez faire une recherche !"

    if liste_validation["aucun_article_trouve"]:
        messages['zero_article_trouve'] = "Le texte utilisé pour la recherche n'a donné aucun article trouvé !"

    if liste_validation["aucun_article_recent"]:
        messages['zero_article_recent'] = "Aucun article est en date du jour dans l'inventaire !"

    if liste_validation["aucun_article"]:
        messages['aucun_article'] = "Aucun article a été enregistré dans l'inventaire !"

    return messages


def message_erreur_admin(liste_validation_admin):
    messages = {}

    if liste_validation_admin['champ_titre_vide']:
        messages['champ_titre_vide'] = "Le nouveau titre de l'article ne peut être vide !"

    if liste_validation_admin['champ_paragraphe_vide']:
        messages['champ_paragraphe_vide'] = "Le nouveau paragraphe de l'article ne peut être vide !"

    if liste_validation_admin['aucune_modification']:
        messages['aucune_modification'] = "Vous devez modifier au moins l'un des champs suivant : Titre ou Paragraphe !"

    if liste_validation_admin['update_reussi']:
        messages['update_reussi'] = "La mise à jour de l'article a été un succès !"

    return messages
