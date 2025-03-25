let kanjiObjects = []; 

fetch("../db/kanjis.json")
    .then(response => response.json())  // Convertit le JSON en objet JS
    .then(data => {
        //console.log("Données chargées :", data)
        // On crée des objets avec les données
        let kanjiObjects = data.map(item => new Kanji(
            item.id,
            item.kanji,
            item["on'yomi"],  // Accès aux clés avec apostrophe
            item["kun'yomi"],
            item.meaning,
            item.JLPT
        ));
        
        console.log("CEST QUOI CA ",kanjiObjects); // Affiche les objets Kanji
        displayKanji(kanjiObjects); // Appel de la fonction d'affichage
    })
    .catch(error => console.error("Erreur lors du chargement du JSON :", error));

// Définition d'une classe Kanji
class Kanji {
    constructor(id, kanji, onyomi, kunyomi, meaning, jlpt) {
        this.id = id;
        this.kanji = kanji;
        this.onyomi = onyomi;
        this.kunyomi = kunyomi;
        this.meaning = meaning;
        this.jlpt = jlpt
    }
}

// Fonction pour afficher les kanjis dans la page
function displayKanji(paramKanjiObjects) {
    console.log("KanjiObjects :", paramKanjiObjects); // Vérification du contenu de kanjiObjects

    const kanjiContainer = document.getElementById("kanji-list");

    if (!kanjiContainer) {
        console.error("Le conteneur pour les kanjis n'a pas été trouvé.");
        return;
    }

    kanjiContainer.innerHTML = ""; // Nettoie l'affichage précédent

    if (paramKanjiObjects.length === 0) {
        console.log("Aucun kanji à afficher.");
        kanjiContainer.innerHTML = "Aucun kanji disponible.";
        return;
    }

    //      ##      POUR FILTRER CEST TROP BIEN      ##
    //const N3 = paramKanjiObjects.filter(kanji => kanji.jlpt === "Kanji N3 (intermediate)");
    //paramKanjiObjects = N3


    // Vérifie si on rentre bien dans la boucle forEach
    //console.log("Affichage des kanjis :");
    paramKanjiObjects.forEach(kanji => {
        console.log("Affichage du kanji :", kanji.kanji); // Vérifie que chaque kanji est bien passé dans la boucle

        const div = document.createElement("div");
        div.innerHTML = `
            <strong>${kanji.kanji}</strong> (${kanji.jlpt}) : ${kanji.meaning} <br>
            🔹 On’yomi : ${kanji.onyomi.join(", ")} <br>
            🔹 Kun’yomi : ${kanji.kunyomi.join(", ")}
            <hr>
        `;
        kanjiContainer.appendChild(div);
    });
}