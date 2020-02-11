import sqlite3


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

    def create_user(self, username, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute("insert into users(utilisateur, email, salt, hash) values(?, ?, ?, ?)",
                           (username, email, salt, hashed_password))
        connection.commit()

    # Méthode pour vérifier que utilisateur existe ou pas, lors de la tentative d'enregistrement d'un utilisateur
    def verify_user_exist(self, liste_validation, username, email):
        cursor = self.get_connection().cursor()
        cursor.execute("select utilisateur, email from users where utilisateur=? OR email=?", (username, email,))
        # nb_result = cursor.rowcount # Ceci n'existe pas

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
