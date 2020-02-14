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

    def get_articles_trouvees(self, texte):
        cursor = self.get_connection().cursor()
        select = "select titre, date_publication, identifiant "
        fromm = "from article "
        where = "where titre like ? or paragraphe like ? "
        order_by = "order by titre"
        sql = select + fromm + where + order_by
        texte = "%" + texte + "%"
        cursor.execute(sql, (texte, texte))
        result = cursor.fetchall()
        ensemble = {}  # L'ensemble des articles jusqu'à un max de 5 des plus récents
        if result is not None:
            for un_article_trouvee in result:
                sous_ensemble = {'Titre': un_article_trouvee[0], 'Date de publication': un_article_trouvee[1]}
                ensemble[un_article_trouvee[2]] = sous_ensemble

        return ensemble

    def create_user(self, username, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute("insert into users(utilisateur, email, salt, hash) values(?, ?, ?, ?)",
                           (username, email, salt, hashed_password))
        connection.commit()
