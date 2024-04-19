document.addEventListener('DOMContentLoaded', function () {
    // Attach the event listener to the form with id 'registrationForm'
    let form = document.getElementById('registrationForm');
    form.onsubmit = function (e) {
        // Prevent the form from submitting the traditional way
        e.preventDefault();

        // Get the form data
        let username = document.getElementById('username').value;
        let password = document.getElementById('password').value;
        let contact = document.getElementById('contact').value;

        // Create an object to send as JSON
        let formData = {
            username: username,
            password: password,
            contact: contact
        };

        // Use the Fetch API to send the form data
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
            .then(response => response.json())
            .then(data => {
                // Handle response data
                console.log(data);
                if (data.message === 'Registered successfully') {
                    // Maybe redirect to the login page or show a success message
                    window.location.href = '/login'; // Redirect to login on success
                } else {
                    // Handle errors, show messages to the user, etc.
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };
});