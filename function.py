from flask import g

from .database import Database  # Importer le fichier database.py


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def initial_champ():
    liste_champs = {"user": "", "password": "", "email": ""}

    return liste_champs


def initial_champ_validation():
    liste_validation = {"situation_erreur": False, "champ_user_vide": False, "champ_password_vide": False,
                        "champ_email_vide": False, "champs_vides": False, "user_existant": False,
                        "email_existant": False, "user_password_eqal": False, "user_inexistant": False,
                        "password_invalide": False}

    return liste_validation


def validation_creation_user(liste_champs, liste_validation):
    if liste_champs['user'] == "":
        liste_validation['champ_user_vide'] = True

    if liste_champs['password'] == "":
        liste_validation['champ_password_vide'] = True

    if liste_champs['email'] == "":
        liste_validation['champ_email_vide'] = True

    if liste_validation['champ_user_vide'] or liste_validation['champ_password_vide'] or \
            liste_validation['champ_email_vide']:
        liste_validation['champs_vides'] = True

    if not liste_validation['champ_user_vide'] and not liste_validation['champ_password_vide']:
        if liste_champs['user'] == liste_champs['password']:
            liste_validation['user_password_eqal'] = True

    return liste_validation


def validation_ouverture_session(liste_champs, liste_validation):
    if liste_champs['user'] == "":
        liste_validation['champ_user_vide'] = True

    if liste_champs['password'] == "":
        liste_validation['champ_password_vide'] = True

    if liste_validation['champ_user_vide'] or liste_validation['champ_password_vide']:
        liste_validation['champs_vide'] = True

    return liste_validation


def situation_erreur(liste_validation):
    situation = False
    for cle, valeur in liste_validation.items():
        if valeur:
            situation = True

    return situation


def message_erreur(liste_validation):
    messages = []

    if liste_validation["champ_user_vide"]:
        messages.append("Veuillez saisir un nom utilisateur !")

    if liste_validation["champ_password_vide"]:
        messages.append("Veuillez saisir un password !")

    if liste_validation["champ_email_vide"]:
        messages.append("Veuillez saisir un email !")

    if liste_validation["user_inexistant"] and not liste_validation["champ_user_vide"]:
        messages.append("Votre utilisateur n'existe pas dans notre base de données !")

    if liste_validation["password_invalide"] and not liste_validation["champ_password_vide"]:
        messages.append("Votre utilisateur est valide mais pas votre password !")

    if liste_validation["user_existant"]:
        messages.append("Veuillez saisir un nom utilisateur qui n'existe pas encore dans nos systèmes !")

    if liste_validation["email_existant"]:
        messages.append("Veuillez saisir un email qui n'existe pas encore dans nos systèmes !")

    if liste_validation["user_password_eqal"]:
        messages.append("Veuillez saisir un nom utilisateur et un password différent !")

    return messages
