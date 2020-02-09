import hashlib
import uuid

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from .function import *

app = Flask(__name__, static_url_path='', static_folder='static')

app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', titre="Présentation")


@app.route('/register', methods=["GET", "POST"])
def formulaire_creation():
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    messages = []

    if request.method == "GET":
        return render_template("register.html", titre="Enregistrement En Cours", messages=messages,
                               liste_validation=liste_validation)
    else:
        liste_champs['user'] = request.form['user']
        liste_champs['password'] = request.form['password']
        liste_champs['email'] = request.form['email']
        liste_validation = validation_creation_user(liste_champs, liste_validation)

        # On commence par vérifier si le user existe ou pas dans la bd
        conn_db = get_db()
        if not liste_validation['champs_vides']:
            liste_validation = conn_db.verify_user_exist(liste_validation, liste_champs['user'], liste_champs['email'])

        liste_validation['situation_erreur'] = situation_erreur(liste_validation)
        if liste_validation['situation_erreur']:
            messages = message_erreur(liste_validation)
            return render_template("register.html", titre="Problème d'enregistrement",
                                   liste_validation=liste_validation, messages=messages)
        else:
            # On peut maintenant prendre le password du client et le securiser
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(str(liste_champs['password'] + salt).encode("utf-8")).hexdigest()
            conn_db.create_user(liste_champs['user'], liste_champs['email'], salt, hashed_password)
            return redirect(url_for('.creation_user_ok'))


@app.route('/login', methods=["GET", "POST"])
def logging_utilisateur():
    """
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, username)
        session["id"] = id_session
    """
    liste_champs = initial_champ()  # Création de la liste d'information nécessaire
    liste_validation = initial_champ_validation()  # Création des indicateurs erreurs
    messages = []
    if request.method == "GET":
        return render_template("login.html", titre="Connexion En Cours", messages=messages,
                               liste_validation=liste_validation)
    else:
        liste_champs['user'] = request.form['user']
        liste_champs['password'] = request.form['password']
        liste_validation = validation_ouverture_session(liste_champs, liste_validation)
        # On commence par vérifier si le user existe ou pas dans la bd
        conn_db = get_db()
        if not liste_validation['champs_vides']:
            user = conn_db.get_user_login_info(liste_champs['user'])

        if user is not None:
            salt = user[0]  # la maniere de crypté le password
            hashed_password = hashlib.sha512(str(liste_champs['password'] + salt).encode("utf-8")).hexdigest()
            if not hashed_password == user[1]:
                liste_validation['password_invalide'] = True

        else:
            liste_validation['user_inexistant'] = True

        liste_validation['situation_erreur'] = situation_erreur(liste_validation)
        if liste_validation['situation_erreur']:
            messages = message_erreur(liste_validation)
            return render_template("login.html", titre="Problème de connexion",
                                   liste_validation=liste_validation, messages=messages)
        else:
            return redirect(url_for('.connexion_user_ok', user=liste_champs['user']))


@app.route('/creation_user_ok')
def creation_user_ok():
    return render_template("creation_user_ok.html", nom_lien_web="Creation user reussi !!!")


@app.route('/connexion_user_ok/<user>')
def connexion_user_ok(user):
    return render_template("connexion_user_ok.html", user=user)
