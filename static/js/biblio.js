// Variable pour le bouton Effacer dans la page d'accueil pour une recherche infructueuse
const recher_article = document.querySelector('#recher_article');

// Variable pour le bouton Effacer dans la page des articles à modifier
const nom_article = document.querySelector('#nom_article');
const nom_paragraphe = document.querySelector('#nom_paragraphe');

// Variable pour le bouton Effacer dans la page des articles à ajouter
const ajout_article = document.querySelector('#ajout_article');
const ajout_identifiant = document.querySelector('#ajout_identifiant');
const nom_auteur = document.querySelector('#ajout_auteur');
const ajout_paragraphe = document.querySelector('#ajout_paragraphe');
const ajout_date = document.querySelector('#ajout_date');

// Variable pour effacer les messages erreurs
const aucun = document.querySelector('.aucun');

/*
    En fonction où nous sommes, sur le site, la fonction «re_initialiser_tous_champs» sera
    appelée pour chaque type de champs que le formulaire contient.
*/
function reset_modif(){
    nom_article.defaultValue = "";
    nom_paragraphe.defaultValue = "";
    effacer_messages_erreurs();
    re_initialiser_tous_champs("input[type=text]");
    re_initialiser_tous_champs("textarea");
}

function reset_ajout(){
    ajout_article.defaultValue = "";
    ajout_identifiant.defaultValue = "";
    nom_auteur.defaultValue = "";
    ajout_paragraphe.defaultValue = "";
    ajout_date.defaultValue = "";
    effacer_messages_erreurs();
    re_initialiser_tous_champs("input[type=text]");
    re_initialiser_tous_champs("input[type=date]");
    re_initialiser_tous_champs("textarea");
}

function reset_recherche(){
    recher_article.defaultValue = "";
    effacer_messages_erreurs();
    re_initialiser_tous_champs("input[type=search]");
}

function effacer_messages_erreurs(){
    aucun.innerHTML = "";
}

/*
    Cette fonction aura pour but de remettre au valeur initial la bordure et couleur de fond
    sur tous les champs d'un formulaire
*/
function re_initialiser_tous_champs(type_champs){
    var tous_champs = document.querySelectorAll(type_champs);
    tous_champs.forEach(function(un_champ){
        un_champ.style.border = "initial";
        un_champ.style.background = "white";
    });
}