document.addEventListener('DOMContentLoaded', function () {
    // Attach the event listener to the form with id 'loginForm'
    let form = document.getElementById('loginForm');
    form.onsubmit = function (e) {
        // Prevent the form from submitting the traditional way
        e.preventDefault();

        // Get the form data
        let username = document.getElementById('loginUsername').value;
        let password = document.getElementById('loginPassword').value;

        // Create an object to send as JSON
        let formData = {
            username: username,
            password: password
        };

        // Use the Fetch API to send the form data
        fetch('/login', {
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
                if (data.message === 'Login successful') {
                    // Redirect to the home page or dashboard on success
                    window.location.href = '/'; // Redirect to home on success
                } else {
                    // Handle errors, show messages to the user, etc.
                    alert('Login failed. Please check your username and password and try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };
});
