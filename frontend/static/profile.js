/* Supprimer élément carte du DOM */
/* Async + await travaillent ensemble */
/* Async = fonction retourne promesse */
/* Wait = attendre une promesse */
document.addEventListener('click', async (event) => {
    /* Si element html contient delete-btn alors... */
    if (event.target.classList.contains('delete-btn')) {
        /* html element avec class card */
        const cardFront = event.target.closest('.card');
        /* Si ne trouve pas card, sort de fonction */
        if (!cardFront) return;
        /* Trouve l'ID {{ item.id }} du favori dans la carte */
        const itemId = cardFront.dataset.id; // Assure-toi que le HTML a un data-id="1996" par exemple

        /* Si pas de ID, alerte et arrêt */
        if (!itemId) {
            alert("ID missing");
            return;
        }
        /* await réponse serveur (reçue/échouée) */
        try {
            /* Chercher fonction dans main.py */
            const response = await fetch('/remove-favourite', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: Number(itemId) }),
            });
            /* Vérification, lire contenu JSON */
            const result = await response.json();
            /* Si ok, supprime carte */
            if (response.ok) {
                const card = cardFront.closest('.card');
                /* Peut ne rien trouver et alors card = null */
                if (card) {
                    card.remove();
                }
            } else {
                /* Sinon, message erreur */
                alert(result.error || "Error while deleting");
            }
        } catch (error) {
            alert("Server error");
        }
    }
});
