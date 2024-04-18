document.getElementById('registrationForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let emergencyContact = document.getElementById('emergencyContact').value;

    // Simple validation
    if (!username || !password || !emergencyContact) {
        alert('Please fill out all fields');
        return;
    }

    // Asynchronous request to the backend
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password, emergencyContact})
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
});