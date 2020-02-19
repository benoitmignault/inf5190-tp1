// Variable pour le bouton Effacer dans la page des articles à modifier
const nom_article = document.querySelector('#nom_article');
const nom_paragraphe = document.querySelector('#nom_paragraphe');

// Variable pour le bouton Effacer dans la page des articles à ajouter
const ajout_article = document.querySelector('#ajout_article');
const ajout_identifiant = document.querySelector('#ajout_identifiant');
const nom_auteur = document.querySelector('#ajout_auteur');
const ajout_paragraphe = document.querySelector('#ajout_paragraphe');
const ajout_date = document.querySelector('#ajout_date');

function reset_modif(){
    // Le bouton Effacer dans la page admin_modif_selectionner.html doit avoir cet event pour effacer les champs.
    nom_article.defaultValue = "";
    nom_paragraphe.defaultValue = "";
}

function reset_ajout(){
    // Le bouton Effacer dans la page admin_nouveau.html doit avoir cet event pour effacer les champs.
    ajout_article.defaultValue = "";
    ajout_identifiant.defaultValue = "";
    nom_auteur.defaultValue = "";
    ajout_paragraphe.defaultValue = "";
    ajout_date.defaultValue = null;
}