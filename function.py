from flask import g

from .database import Database  # Importer le fichier database.py


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def initial_champ():
    liste_champs = {"nb_article_recent": 0, "nb_article_trouve": 0, "recher_article": "", "message": []}

    return liste_champs


def initial_champ_validation():
    liste_validation = {"aucun_article_recent": False, "champ_recher_article_vide": False,
                        "aucun_article_trouve": False,
                        "situation_erreur": False}

    return liste_validation


def remplissage_champs(formulaire, liste_champs):
    liste_champs['recher_article'] = formulaire['recher_article']

    return liste_champs


def validation_champs(liste_champs, liste_validation):
    if liste_champs['recher_article'] == "":
        liste_validation['champ_recher_article_vide'] = True

    return liste_validation


def situation_erreur(liste_validation):
    for cle, valeur in liste_validation.items():
        if valeur:
            liste_validation['situation_erreur'] = True

    return liste_validation


def message_erreur(liste_validation):
    messages = []
    if liste_validation["champ_recher_article_vide"]:
        messages.append("Le champ ne peut rester vide si vous voulez faire une recherche !")

    if liste_validation["aucun_article_trouve"]:
        messages.append("Le texte utilisé pour la recherche n'a donné aucun article trouvé !")

    if liste_validation["aucun_article_recent"]:
        messages.append("Aucun article est en date du jour dans l'inventaire !")

    return messages
