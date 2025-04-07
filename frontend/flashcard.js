const card = document.querySelector(".card");

card.addEventListener("click", function(){
    card.classList.toggle("show");
})

document.getElementById("favourite").addEventListener("click", async () => {
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
});