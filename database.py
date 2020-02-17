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

    # Sera utiliser avec la route /
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
                sous_ensemble = {'titre': un_article[0], 'identifiant': un_article[1], 'auteur': un_article[2],
                                 'date_publication': un_article[3], 'paragraphe': un_article[4]}
                ensemble[un_article[1]] = sous_ensemble

        return ensemble

    # Sera utiliser avec la route /recherche
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
        ensemble_trouve = {}  # L'ensemble des articles jusqu'à un max de 5 des plus récents
        if result is not None:
            for un_article_trouvee in result:
                sous_ensemble = {'titre': un_article_trouvee[0], 'date_publication': un_article_trouvee[1]}
                ensemble_trouve[un_article_trouvee[2]] = sous_ensemble

        return ensemble_trouve

    # Sera utiliser avec la route /article/<identifiant»
    def get_articles_selectionner(self, identifiant):
        cursor = self.get_connection().cursor()
        select = "select titre, identifiant, auteur, date_publication, paragraphe "
        fromm = "from article "
        where = "where identifiant = ?"
        sql = select + fromm + where
        cursor.execute(sql, (identifiant,))
        result = cursor.fetchone()
        ensemble_trouve = {}  # L'ensemble des articles jusqu'à un max de 5 des plus récents

        if result is not None:
            ensemble_trouve = {'titre': result[0], 'identifiant': result[1], 'auteur': result[2],
                               'date_publication': result[3], 'paragraphe': result[4]}

        return ensemble_trouve

    # Sera utiliser avec la route /admin
    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        select = "select titre, date_publication, identifiant "
        fromm = "from article "
        order_by = "order by titre"
        sql = select + fromm + order_by
        cursor.execute(sql)
        result = cursor.fetchall()
        ensemble = {}  # L'ensemble des articles jusqu'à un max de 5 des plus récents
        if result is not None:
            for un_article_trouvee in result:
                sous_ensemble = {'titre': un_article_trouvee[0], 'date_publication': un_article_trouvee[1]}
                ensemble[un_article_trouvee[2]] = sous_ensemble

        return ensemble

    def update_article(self, identifiant, titre, paragraphe):
        connection = self.get_connection()
        update_from = "update article "
        update_set = "set titre = ? , paragraphe = ?"
        update_where = "where identifiant = ?"
        sql = update_from + update_set + update_where
        connection.execute(sql, (titre, paragraphe, identifiant))
        connection.commit()

    def create_user(self, username, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute("insert into users(utilisateur, email, salt, hash) values(?, ?, ?, ?)",
                           (username, email, salt, hashed_password))
        connection.commit()
