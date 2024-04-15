# Location-based Safety Network Alert System

This project implements a simple web-based alert system that allows users to send distress signals along with their geographical location to a designated contact. It utilizes Flask for backend processing, Flask-SocketIO for real-time communication, and HTML/CSS/JavaScript for the frontend.

## Project Structure

- app.py: Contains the main application and route configurations. It includes routes for user registration and login, and sets up WebSocket communication.
- config.py: Stores configuration settings such as secret keys and database URI.
- requirements.txt: Lists all project dependencies, ensuring all necessary libraries are installed.

### Directories

- templates/: Holds HTML files for the user interface.
  - login.html: Provides the user login interface.
  - register.html: Provides the user registration interface.
  - index.html: Main page that includes the help button for sending alerts.
- static/: Contains static files used in the web application.
  - css/: Directory for CSS files that style the web pages.
  - js/: Contains JavaScript files that handle frontend logic.
    - login.js: Manages login functionality.
    - register.js: Manages registration functionality.
    - alert.js: Handles the logic for sending help alerts and communicating with the backend via WebSocket.

## Usage

To run the project, ensure you have Python installed, set up a virtual environment, install dependencies listed in requirements.txt, and execute the following command in your terminal:

```
python app.py
```

This command starts the Flask application and the SocketIO server, making the web interface accessible via http://127.0.0.1:5000/ in your web browser.
