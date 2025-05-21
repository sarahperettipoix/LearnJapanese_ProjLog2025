/* document.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-btn')) {
        // Find the nearest card-front and remove the whole card
        const cardFront = event.target.closest('.card-front');
        if (cardFront) {
            const card = cardFront.closest('.card');
            card.remove(); // or cardFront.remove() if you want to remove only the front
        }
    }
});
 */

document.addEventListener('click', async (event) => {
    if (event.target.classList.contains('delete-btn')) {
        const cardFront = event.target.closest('.card');
        if (!cardFront) return;

        // Trouve l'id du favori dans la carte
        const itemId = cardFront.dataset.id; // Assure-toi que le HTML a un data-id="1996" par exemple

        if (!itemId) {
            alert("ID manquant");
            return;
        }

        try {
            const response = await fetch('/remove-favourite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: Number(itemId) }),
            });

            const result = await response.json();

            if (response.ok) {
                // Supprime la carte du DOM
                const card = cardFront.closest('.card');
                if (card) card.remove();
            } else {
                alert(result.error || "Erreur lors de la suppression");
            }
        } catch (error) {
            alert("Erreur réseau");
        }
    }
});
