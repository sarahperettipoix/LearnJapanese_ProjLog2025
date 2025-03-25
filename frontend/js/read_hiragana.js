let hiraganaObjects = []; 

fetch("../db/hiragana.json")
    .then(response => response.json())  // Convertit le JSON en objet JS
    .then(data => {
        //console.log("Données chargées :", data)
        // On crée des objets avec les données
        let hiraganaObjects = data.map(item => new Hiragana(
            item.id,
            item.kana,
            item.romaji
        ));
        
        console.log("CEST QUOI CA ",hiraganaObjects); // Affiche les objets Kanji
        displayHiragana(hiraganaObjects); // Appel de la fonction d'affichage
    })
    .catch(error => console.error("Erreur lors du chargement du JSON :", error));

// Définition d'une classe Kanji
class Hiragana {
    constructor(id, kana, romaji) {
        this.id = id;
        this.kana = kana;
        this.romaji = romaji;
    }
}

// Fonction pour afficher les kanjis dans la page
function displayHiragana(paramHiraganaObjects) {
    console.log("hiraganaObjects :", paramHiraganaObjects); // Vérification du contenu de kanjiObjects

    const hiraganaContainer = document.getElementById("hiragana-list");

    if (!hiraganaContainer) {
        console.error("Le conteneur pour les kanjis n'a pas été trouvé.");
        return;
    }

    hiraganaContainer.innerHTML = ""; // Nettoie l'affichage précédent

    if (paramHiraganaObjects.length === 0) {
        console.log("Aucun kanji à afficher.");
        hiraganaContainer.innerHTML = "Aucun kanji disponible.";
        return;
    }

    //      ##      POUR FILTRER CEST TROP BIEN      ##
    //const N3 = paramKanjiObjects.filter(kanji => kanji.jlpt === "Kanji N3 (intermediate)");
    //paramKanjiObjects = N3


    // Vérifie si on rentre bien dans la boucle forEach
    //console.log("Affichage des kanjis :");
    paramHiraganaObjects.forEach(hiragana => {
        console.log("Affichage du hiragana :", hiragana.kana); // Vérifie que chaque kanji est bien passé dans la boucle

        const div = document.createElement("div");
        div.innerHTML = `
            <strong>${hiragana.kana}</strong> <br>
            🔹 id : ${hiragana.id} <br>
            🔹 prononciation : ${hiragana.romaji}
            <hr>
        `;
        hiraganaContainer.appendChild(div);
    });
}