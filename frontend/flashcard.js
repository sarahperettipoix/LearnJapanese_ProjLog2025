const card = document.querySelector(".card");

/* make the card clicable */
card.addEventListener("click", function(){
    card.classList.toggle("show"); /* allow the card to be flipped over */
})

/* document.getElementById("favourite").addEventListener("click", async () => {
    const username = "sophie";  // Replace with dynamic user data
    const flashcardId = "kanji_123";  // Replace with the actual flashcard ID

    try {
        const response = await fetch(`http://127.0.0.1:8000/user/${username}/favorites?flashcard_id=${flashcardId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" }
        });

        const result = await response.json();
        if (response.ok) {
            alert("Added to favorites!");
        } else {
            alert("Error: " + result.detail);
        }
    } catch (error) {
        console.error("Failed to add favorite:", error);
    }
}); */
 
const button = document.getElementById("favourite")
/* a list to store the favourite cards */
const favList = []

/* test */
button.addEventListener("click", doSomething);
/* adding 1 to the list each time it is clicked */
button.addEventListener("click", add);

function doSomething (){
    alert("It did something!");
}
function add (){
    favList.push(1);
    console.log(favList);
    alert("Added to Favourites List!");
}

/* https://www.youtube.com/watch?v=i_8NQuEAOmg */