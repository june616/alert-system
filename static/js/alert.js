document.addEventListener('DOMContentLoaded', function() {
    var helpButton = document.getElementById('helpButton');
    var statusMessage = document.getElementById('statusMessage');
    var socket = io(); // Initialize socket.io here to make sure it's in scope

    helpButton.onclick = function() {
        statusMessage.innerHTML = "<p>Working on it...</p>";
        navigator.geolocation.getCurrentPosition(function(position) {
            const userID = localStorage.getItem('userID');
            // Emit the location data to the server
            socket.emit('send_help', {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                id: userID
            });

        }, function(error) {
            console.error('Geolocation error:', error);
            statusMessage.innerHTML += "<p>Error fetching location.</p>"; // Display error if geolocation fails
        });
    };

    // Handle status updates from the server
    socket.on('status_update', function(data) {
        statusMessage.innerHTML += `<p>${data.message}</p>`; // Update status message dynamically
    });

    // Listen for 'help_response' event from the server to update the user
    socket.on('help_response', function(data) {
        // Update the display with the user-friendly location
        statusMessage.innerHTML += `<p>Help is on the way!</p><p>Location: ${data.location}</p><p>We have notified your contact.</p>`;
    });
});
