const card = document.querySelector(".card");
const prev = document.querySelector(".nav-btn-previous")
const next = document.querySelector(".nav-btn-next")

const card_front = document.querySelector(".card-front")
const card_back = document.querySelector(".card-back")

card.addEventListener("click", function(){
    card.classList.toggle("show");
})



window.addEventListener("DOMContentLoaded", () => {
    const jsonScript = document.getElementById("kana-json");

    try {
        const hiraganaData = JSON.parse(jsonScript.textContent.trim());
        
        hiraganaData.sort(() => Math.random() - 0.5);   //mélange

        console.log("Hiragana list:", hiraganaData);

        let index = 0;

        function showFirstCard() {
            index = 0
            const current = hiraganaData[index];

            // 💡 Tu peux mettre ici du code pour mettre à jour l'HTML dynamiquement
            //console.log("Kana:", current.kana, "Romaji:", current.romaji);
            card_front.textContent = current.kana

            card_back.textContent = current.romaji
        }

        function showNextCard() {
            index = index + 1;
            const current = hiraganaData[index];

            // 💡 Tu peux mettre ici du code pour mettre à jour l'HTML dynamiquement
            //console.log("Kana:", current.kana, "Romaji:", current.romaji);
            
            card_front.textContent = current.kana

            card_back.textContent = current.romaji   
        }        

        function showPreviousCard() {
            if (index > 0) {  // Si ce n'est pas le premier élément, on décrémente l'index
                index = index - 1;
            }
            const current = hiraganaData[index];

            // 💡 Tu peux mettre ici du code pour mettre à jour l'HTML dynamiquement
            //console.log("Kana:", current.kana, "Romaji:", current.romaji);
            card_front.textContent = current.kana

            card_back.textContent = current.romaji
        }

        next.addEventListener("click", showNextCard);
        prev.addEventListener("click", showPreviousCard);

        showFirstCard()
    } catch (e) {
        console.error("Erreur lors du parsing JSON :", e);
        window.alert("Erreur lors du parsing JSON");
    }
    
});

