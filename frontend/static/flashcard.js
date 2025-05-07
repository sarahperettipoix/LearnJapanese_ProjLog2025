const card = document.querySelector(".card");
const prev = document.querySelector(".nav-btn-previous")
const next = document.querySelector(".nav-btn-next")

const card_front = document.querySelector(".card-front")
const card_back = document.querySelector(".card-back")

let index = 0;

card.addEventListener("click", function(){
    card.classList.toggle("show");
})


window.addEventListener("DOMContentLoaded", () => {
    const jsonScript = document.getElementById("kana-json");
    try {
        const hiraganaData = JSON.parse(jsonScript.textContent.trim());
        
        hiraganaData.sort(() => Math.random() - 0.5);   //mélange

        //console.log("Hiragana list:", hiraganaData);



        // Vérifie si au moins un objet du tableau contient la clé "JLPT"
        const contientJLPT = hiraganaData.some(obj => "JLPT" in obj);

        function test_and_afficher(index){

            const current = hiraganaData[index];

            // On teste si les données sont des kana ou des kanjis, c'est un peu sale mais bon
            // il faudra aussi faire pleins de if pour les checkbox
            if (contientJLPT) {
                card_front.textContent = current.kanji
                card_back.innerHTML = String(current.onyomi + "<br>" + current.kunyomi + "<br>" + current.meaning);
            } else {

                // 💡 Tu peux mettre ici du code pour mettre à jour l'HTML dynamiquement
                //console.log("Kana:", current.kana, "Romaji:", current.romaji);
                card_front.textContent = current.kana
                card_back.textContent = current.romaji
            }
        }

        function showFirstCard() {
            index = 0
            test_and_afficher(index)
        }

        function showNextCard() {
            index = index + 1;
            test_and_afficher(index)
        }
        

        function showPreviousCard() {
            if (index > 0) {  // Si ce n'est pas le premier élément, on décrémente l'index
                index = index - 1;
            }
            test_and_afficher(index)
        }

        next.addEventListener("click", showNextCard);
        prev.addEventListener("click", showPreviousCard);

        showFirstCard()
    } catch (e) {
        console.error("Erreur lors du parsing JSON :", e);
        window.alert("Erreur lors du parsing JSON");
    }
    
});

// favoris
document.getElementById('favourite').addEventListener('click', async () => {
    const kanaData = JSON.parse(document.getElementById('kana-json').textContent);
    
    // exemple simple : on prend l’élément affiché (tu peux adapter)
    const currentIndex = index;
    const currentKana = kanaData[currentIndex];

    const response = await fetch('/add-favourite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentKana)
    });

    if (response.ok) {
        alert("Ajouté aux favoris !");
    } else {
        alert("Erreur lors de l'ajout.");
    }
});