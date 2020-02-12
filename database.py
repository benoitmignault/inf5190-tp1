import sqlite3
from datetime import date


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/tp1.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_articles_recents(self):
        date_auj = date.today()
        cursor = self.get_connection().cursor()
        select = "select titre, identifiant, auteur, date_publication, paragraphe "
        fromm = "from article "
        where = "where date_publication <=? "
        order_by = "order by date_publication desc"
        sql = select + fromm + where + order_by
        cursor.execute(sql, (date_auj,))
        result = cursor.fetchall()
        ensemble = {}  # L'ensemble des articles jusqu'à un max de 5 des plus récents
        if result is not None:
            for un_article in result:
                sous_ensemble = {'Titre': un_article[0], 'Identifiant': un_article[1], 'Auteur': un_article[2],
                                 'Date de publication': un_article[3], 'Contenu': un_article[4]}
                ensemble[un_article[1]] = sous_ensemble

        return ensemble

    def create_user(self, username, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute("insert into users(utilisateur, email, salt, hash) values(?, ?, ?, ?)",
                           (username, email, salt, hashed_password))
        connection.commit()

    # Méthode pour vérifier que utilisateur existe ou pas, lors de la tentative d'enregistrement d'un utilisateur
    def verify_user_exist(self, liste_validation, username, email):
        cursor = self.get_connection().cursor()
        cursor.execute("select utilisateur, email from users where utilisateur=? OR email=?", (username, email,))

        result = cursor.fetchall()
        if result is not None:
            for one_result in result:
                if one_result[0] == username:
                    liste_validation['user_existant'] = True

                if one_result[1] == email:
                    liste_validation['email_existant'] = True

        return liste_validation

    # On vérifie que le user a saisie le bon password
    def get_user_login_info(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute("select salt, hash from users where utilisateur=?", (username,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0], result[1]
