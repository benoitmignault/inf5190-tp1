import re  # pour la gestion des patterns pour les différents champs input

from flask import g

from .database import Database  # Importer le fichier database.py

PATTERN_DATE = "^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$"  # Ce pattern est pour valider la date
PATTERN_TITRE = "^[a-z0-9-'A-Z ]{3,15}$"  # Ce pattern est pour valider le titre
PATTERN_AUTEUR = "^[a-z-'A-Z ]{3,15}$"  # Ce pattern est pour valider l'auteur
PATTERN_IDENTIFIANT = "^[a-z0-9A-Z]{3,15}$"  # Ce pattern est pour valider l'identifiant
PATTERN_PARAGRAPHE = "^[a-z0-9-'A-Z @_!#$%^&*()<>?/\\|}{~:]{10,100}$"  # Ce pattern est pour valider le paragraphe


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fonction utiliser pour la page d'accueil et la route qui fait des recherches articles
def initial_champ_recherche():
    liste_champs = {"nb_article": 0, "nb_article_recent": 0, "nb_article_trouve": 0, "recher_article": "",
                    "message": {}, "titre": "", "paragraphe": "", "identifiant": "", "date_publication": "",
                    "auteur": ""}

    return liste_champs


# Fonction utiliser pour la page d'accueil et la route qui fait des recherches articles
def initial_champ_validation_recherche():
    liste_validation = {"aucun_article": False, "aucun_article_recent": False, "champ_recher_article_vide": False,
                        "aucun_article_trouve": False, "situation_erreur": False}

    return liste_validation


def remplissage_champs_recherche(formulaire, liste_champs):
    liste_champs['recher_article'] = formulaire['recher_article']

    return liste_champs


def validation_champs_recherche(liste_champs, liste_validation):
    if liste_champs['recher_article'] == "":
        liste_validation['champ_recher_article_vide'] = True

    return liste_validation


# Fonction utiliser pour la gestion des articles lors d'ajout ou modification 
def initial_champ_admin():
    liste_champs_admin = {"titre": "", "titre_avant": "", "paragraphe": "", "paragraphe_avant": "", "identifiant": "",
                          "date_publication": "", "auteur": ""}

    return liste_champs_admin


# Cette fonction sera utiliser pour les modifications et ajout des articles
def initial_champ_validation_admin():
    liste_validation_admin = {"situation_erreur": False, "champ_titre_pareil": False, "champs_pareils": False,
                              "update_reussi": False, "aucune_modification": False, "champ_paragraphe_pareil": False,
                              "champs_vides": False, "champ_titre_vide": False, "champ_paragraphe_vide": False,
                              "champ_date_vide": False, "champ_identifiant_vide": False, "champ_auteur_vide": False,
                              "identifiant_deja_prise": False, "champ_paragraphe_inv": False,
                              "longueur_date_inv": False,
                              "longueur_paragraphe_inv": False, "champ_titre_inv": False, "champ_auteur_inv": False,
                              "champ_identifiant_inv": False, "longueur_titre_inv": False, "longueur_auteur_inv": False,
                              "longueur_identifiant_inv": False, "champ_date_inv": False, "ajout_reussi": False
                              }

    return liste_validation_admin


# J'ai décidé de séparer mes fonction de remplissages comme ce n'est pas les mêmes champs qui seront utilisés
# Fonction utiliser lors de modification articles
# liste_champs représente ceux du fichier index.py liste_champs_admin
def remplissage_champs_modif_article(request, liste_champs):
    liste_champs['titre'] = request.form['nom_article']
    # Je dois utiliser strip pour retirer les retours de lignes non nécessaire
    liste_champs['paragraphe'] = request.form['nom_paragraphe'].strip()
    liste_champs['identifiant'] = request.form['identifiant']
    liste_champs['auteur'] = request.form['nom_auteur']
    liste_champs['date_publication'] = request.form['date_publication']
    liste_champs['titre_avant'] = request.form['nom_article_avant']
    liste_champs['paragraphe_avant'] = request.form['nom_paragraphe_avant']

    return liste_champs


# Fonction utiliser lors d'ajout les articles
# liste_champs représente ceux du fichier index.py liste_champs_admin
def remplissage_champs_ajout_article(request, liste_champs):
    liste_champs['date_publication'] = request.form['date']
    liste_champs['titre'] = request.form['nom_article']
    # Je dois utiliser strip pour retirer les retours de lignes non nécessaire
    liste_champs['paragraphe'] = request.form['nom_paragraphe'].strip()
    liste_champs['identifiant'] = request.form['identifiant']
    liste_champs['auteur'] = request.form['nom_auteur']

    return liste_champs


# liste_champs représente ceux du fichier index.py liste_champs_admin
# liste_validation représente ceux du fichier index.py liste_validation_admin
# Le but était de simpliment aléger la lourdeur du code
def validation_champs_article(liste_champs, liste_validation):
    liste_validation = validation_titre(liste_champs['titre'], liste_validation)
    liste_validation = validation_paragraphe(liste_champs['paragraphe'], liste_validation)
    liste_validation = validation_date(liste_champs['date_publication'], liste_validation)
    liste_validation = validation_identifiant(liste_champs['identifiant'], liste_validation)
    liste_validation = validation_auteur(liste_champs['auteur'], liste_validation)

    # Validation si on a au moins un champ vide
    if liste_validation['champ_titre_vide'] or liste_validation['champ_paragraphe_vide'] or \
            liste_validation['champ_date_vide'] or liste_validation['champ_identifiant_vide'] or \
            liste_validation['champ_auteur_vide']:
        liste_validation['champs_vides'] = True

    if not liste_validation['champs_vides']:
        # Seulement si les champs ne sont pas vide, qu'on va poursuivre les validations de manière logique
        if liste_champs['paragraphe'] == liste_champs['paragraphe_avant']:
            liste_validation['champ_paragraphe_pareil'] = True

        if liste_champs['titre'] == liste_champs['titre_avant']:
            liste_validation['champ_titre_pareil'] = True

        if liste_validation['champ_paragraphe_pareil'] and liste_validation['champ_titre_pareil']:
            liste_validation['aucune_modification'] = True
            # On calcul les validités sur les longueurs des champs

    return liste_validation


def validation_titre(titre, liste_validation):
    if titre == "":
        liste_validation['champ_titre_vide'] = True

    else:
        if not (3 <= len(titre) <= 15):
            liste_validation['longueur_titre_inv'] = True

        match_titre = re.compile(PATTERN_TITRE).match
        if match_titre(titre) is None:
            liste_validation['champ_titre_inv'] = True

    return liste_validation


def validation_paragraphe(paragraphe, liste_validation):
    if paragraphe == "":
        liste_validation['champ_paragraphe_vide'] = True

    else:
        if not (10 <= len(paragraphe) <= 100):
            liste_validation['longueur_paragraphe_inv'] = True

        match_paragraphe = re.compile(PATTERN_PARAGRAPHE).match
        if match_paragraphe(paragraphe) is None:
            liste_validation['champ_paragraphe_inv'] = True

    return liste_validation


def validation_date(date, liste_validation):
    if date == "":
        liste_validation['champ_date_vide'] = True
    else:
        if not (len(date) == 10):
            liste_validation['longueur_date_inv'] = True

        match_date = re.compile(PATTERN_DATE).match
        if match_date(date) is None:
            liste_validation['champ_date_inv'] = True

    return liste_validation


def validation_identifiant(identifiant, liste_validation):
    if identifiant == "":
        liste_validation['champ_identifiant_vide'] = True

    else:
        if not (3 <= len(identifiant) <= 15):
            liste_validation['longueur_identifiant_inv'] = True

        match_identifiant = re.compile(PATTERN_IDENTIFIANT).match
        if match_identifiant(identifiant) is None:
            liste_validation['champ_identifiant_inv'] = True

    return liste_validation


def validation_auteur(auteur, liste_validation):
    # Validation pour l'auteur
    if auteur == "":
        liste_validation['champ_auteur_vide'] = True

    else:
        if not (3 <= len(auteur) <= 15):
            liste_validation['longueur_auteur_inv'] = True

        match_auteur = re.compile(PATTERN_AUTEUR).match
        if match_auteur(auteur) is None:
            liste_validation['champ_auteur_inv'] = True

    return liste_validation


# L'indicateur pour savoir si on continu ou si on arrête se que nous sommes entrains de faire
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


def message_erreur_admin(liste_validation):
    messages = []
    if liste_validation['champ_titre_vide']:
        messages.append("Le nouveau titre de l'article ne peut être vide !")

    if liste_validation['champ_paragraphe_vide']:
        messages.append("Le nouveau paragraphe de l'article ne peut être vide !")

    if liste_validation['aucune_modification']:
        messages.append("Vous devez modifier au moins l'un des champs suivant : Titre ou Paragraphe !")

    if liste_validation['update_reussi']:
        messages.append("La mise à jour de l'article a été un succès !")

    return messages


def message_erreur_admin_ajout(liste_validation):
    messages = []
    if liste_validation['ajout_reussi']:
        messages.append("L'ajout de l'article a fonctionné !")
    else:
        if liste_validation['identifiant_deja_prise']:
            messages.append("Attention ! L'identifiant existe déjà, veuiller en choisir un autre !")

        if liste_validation['champ_titre_vide']:
            messages.append("Attention ! Le titre ne peut être vide !")

        if liste_validation['champ_paragraphe_vide']:
            messages.append("Attention ! Le paragraphe  ne peut être vide !")

        if liste_validation['champ_date_vide']:
            messages.append("Attention ! La date de publication ne peut être vide !")

        if liste_validation['champ_identifiant_vide']:
            messages.append("Attention ! Le identifiant ne peut être vide !")

        if liste_validation['champ_auteur_vide']:
            messages.append("Attention ! Un article doit être associer à un auteur !")

        if liste_validation['longueur_paragraphe_inv']:
            messages.append("Attention ! La longueur du paragraphe doit être entre 10 et 100 caractères !")

        if liste_validation['longueur_titre_inv']:
            messages.append("Attention ! Le titre de l'article doit être entre 3 et 15 caractères !")

        if liste_validation['longueur_auteur_inv']:
            messages.append("Attention ! L'auteur de l'article doit être entre 3 et 15 caractères !")

        if liste_validation['longueur_identifiant_inv']:
            messages.append("Attention ! L'identifiant doit être entre 3 et 15 caractères !")

        if liste_validation['champ_date_inv']:
            messages.append("Attention ! La date saisie n'est pas valide selon le format «AAAA-MM-DD» !")

        if liste_validation['champ_auteur_inv']:
            messages.append("Attention ! le nom de l'auteur n'est pas valide !")

        if liste_validation['champ_titre_inv']:
            messages.append("Attention ! le titre de l'article n'est pas valide !")

        if liste_validation['champ_identifiant_inv']:
            messages.append("Attention ! l'identifiant unique pour l'article n'est pas valide !")

        if liste_validation['champ_paragraphe_inv']:
            messages.append("Attention ! le contenu du paragraphe de l'article n'est pas valide !")

    return messages
