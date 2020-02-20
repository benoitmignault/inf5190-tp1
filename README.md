# Site web de base pour une gestion articles

	Logiciel de type CMS (Content Management System) dans le cadre d'une gestion fictive d'articles dans une bibliothèque.

## Pré-installation 

Nous avons besoin de python 3.7+ et de flask minimalement !
	
Pour les systèmes linux/Mac

```bash
sudo python3.8
pip3 install flask
```
Python3.7+ sera le language de programmation back-end 
Flask sera le framework utiliser pour gérer le serveur web 

## Démarrage du site web 

On doit simplement faire cette commande dans le dossier racine
```bash
make
```
Le site web sera hébergé sur l'adresse ip en local soit : 127.0.0.1:5000

### Navigation du site

Il y a plusieurs routes (liens web) possible dans la navigation du site web

1. La page d'accueil ( Cette page va afficher les articles les plus récents) -> http://127.0.0.1:5000/

2. La page d'une recherche d'article qui donnera un résultat positif -> http://127.0.0.1:5000/recherche_article_trouve

3. La page d'un article sélectionné venant de la route «/recherche_article_trouve» -> http://127.0.0.1:5000/article/identifiant

4. La page où tous les articles seront disponibles pour l'administrateur -> http://127.0.0.1:5000/admin

5. La page de modification d'un article qui sera disponible seulement pour l'administrateur -> http://127.0.0.1:5000/admin-modif/identifiant

6. La page pour ajouter un article qui sera disponible seulement pour l'administrateur -> http://127.0.0.1:5000/admin-nouveau

7. Dans l'éventualité que l'identifiant soit inconnu de l'inventaire au point 3 et 5 cela affichera la page
	
	http://127.0.0.1:5000/admin-modif/ et http://127.0.0.1:5000/article/ on affichera une page erreur 404.


## License

* Travail présenté par Benoît Mignault étudiant de l'UQAM 
* Code permanent : MIGB09078205
* Travail remis le 2020-02-20
