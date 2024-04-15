document.addEventListener('DOMContentLoaded', function() {
    var helpButton = document.getElementById('helpButton');
    var statusMessage = document.getElementById('statusMessage');
    var socket = io(); // Initialize socket.io here to make sure it's in scope

    helpButton.onclick = function() {
        statusMessage.innerHTML = "<p>Sending your location...</p>"; // Notify user that the location is being sent
        navigator.geolocation.getCurrentPosition(function(position) {
            // Emit the location data to the server
            socket.emit('send_help', {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
            });

        }, function(error) {
            console.error('Geolocation error:', error);
            statusMessage.innerHTML = "<p>Error fetching location.</p>"; // Display error if geolocation fails
        });
    };

    // Listen for 'help_response' event from the server to update the user
    socket.on('help_response', function(data) {
        // Update the display with the user-friendly location
        statusMessage.innerHTML = `<p>Help is on the way!</p><p>Location: ${data.location}</p><p>We have notified your contact.</p>`;
    });
});
