const nom_article = document.querySelector('#nom_article');
const nom_paragraphe = document.querySelector('#nom_paragraphe');

function customReset(){
    // Le bouton Effacer dans la page admin_modif_selectionner doit avoir cet event pour effacer les champs.
    nom_article.defaultValue = "";
    nom_paragraphe.defaultValue = "";
}