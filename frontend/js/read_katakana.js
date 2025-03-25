let katakanaObjects = []; 

fetch("../db/katakana.json")
    .then(response => response.json())  // Convertit le JSON en objet JS
    .then(data => {
        //console.log("Données chargées :", data)
        // On crée des objets avec les données
        let katakanaObjects = data.map(item => new Katakana(
            item.id,
            item.kana,
            item.romaji
        ));
        
        console.log("CEST QUOI CA ",katakanaObjects); // Affiche les objets Kanji
        displayKatakana(katakanaObjects); // Appel de la fonction d'affichage
    })
    .catch(error => console.error("Erreur lors du chargement du JSON :", error));

// Définition d'une classe Kanji
class Katakana {
    constructor(id, kana, romaji) {
        this.id = id;
        this.kana = kana;
        this.romaji = romaji;
    }
}

// Fonction pour afficher les kanjis dans la page
function displayKatakana(paramKatakanaObjects) {
    console.log("katakanaObjects :", paramKatakanaObjects); // Vérification du contenu de kanjiObjects

    const katakanaContainer = document.getElementById("katakana-list");

    if (!katakanaContainer) {
        console.error("Le conteneur pour les kanjis n'a pas été trouvé.");
        return;
    }

    katakanaContainer.innerHTML = ""; // Nettoie l'affichage précédent

    if (paramKatakanaObjects.length === 0) {
        console.log("Aucun kanji à afficher.");
        katakanaContainer.innerHTML = "Aucun kanji disponible.";
        return;
    }

    //      ##      POUR FILTRER CEST TROP BIEN      ##
    //const N3 = paramKanjiObjects.filter(kanji => kanji.jlpt === "Kanji N3 (intermediate)");
    //paramKanjiObjects = N3


    // Vérifie si on rentre bien dans la boucle forEach
    //console.log("Affichage des kanjis :");
    paramKatakanaObjects.forEach(katakana => {
        console.log("Affichage du katakana :", katakana.kana); // Vérifie que chaque kanji est bien passé dans la boucle

        const div = document.createElement("div");
        div.innerHTML = `
            <strong>${katakana.kana}</strong> <br>
            🔹 id : ${katakana.id} <br>
            🔹 prononciation : ${katakana.romaji}
            <hr>
        `;
        katakanaContainer.appendChild(div);
    });
}