function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        const [name, value] = c.trim().split('=');
        if (name === 'csrftoken') return decodeURIComponent(value);
    }
    return '';
}

// Add on Enter key
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

function addToPantry() {
    const input = document.getElementById("ingredient");
    const ingredient = (input?.value || "").trim().toLowerCase();
    if (!ingredient) return;

    fetch('/add-to-pantry/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ ingredient: [ingredient] })
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed to add ingredient');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            window.location.reload(); // ensures categorization applied
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


function removeFromPantry(ingredient, element) {
    fetch('/remove-from-pantry/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ ingredient })
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed to remove ingredient');
        return res.json();
    })
    .then(data => {
        if (data.success && element) {
            element.remove(); // instant feedback
        }
    })
    .catch(err => console.error(err));
}
