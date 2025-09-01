// Get CSRF token from hidden div
function getCSRFToken() {
    const el = document.getElementById('csrf-token');
    return el ? el.dataset.token : '';
}

// Add ingredient on Enter key
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('ingredient');
    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addToPantry();
            }
        });
    }
});

// Add ingredient to pantry without reloading
function addToPantry() {
    const input = document.getElementById("ingredient");
    const ingredient = (input?.value || "").trim();
    if (!ingredient) return;

    fetch('/add-to-pantry/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ ingredient: [ingredient] })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Append to the correct category dynamically
            const pantrySection = document.getElementById('pantry-section');
            if (pantrySection) {
                // Here we just reload the pantry section
                window.location.reload(); // temporary, later we can fully update dynamically
            }
        }
    })
    .catch(err => {
        alert("Error adding ingredient. Please try again.");
        console.error(err);
    })
    .finally(() => {
        if (input) input.value = '';
    });
}

// Remove ingredient from pantry dynamically
function removeFromPantry(ingredient, element) {
    fetch('/remove-from-pantry/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ ingredient })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && element) {
            element.remove(); // remove from DOM instantly
        }
    })
    .catch(err => console.error(err));
}
