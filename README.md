# NTFY Message Scheduler

Welcome to the Message Scheduler! This app lets you schedule messages to be sent at specific times, with options for repeating intervals. It's perfect for reminders, notifications, and more!

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Files and Structure](#files-and-structure)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is a message scheduling application built using Flask, SQLite, jQuery, and Bootstrap. It allows users to schedule messages, manage servers and topics, and view sent and scheduled messages.

## Getting Started

This guide will help you set up and run the Message Scheduler Application using Docker and Docker Compose. Follow the steps below to get your application up and running in your home lab.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- [Install Docker](https://docs.docker.com/get-docker/)

### Project Structure

```
.
├── Dockerfile
├── app
│   ├── main.py
│   ├── scheduler.py
│   ├── database.py
│   ├── templates
│   │   └── index.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   └── messages.db
└── README.md
```

### Building and Running the Application

1. **Build the Docker images:**

   ```sh
   podman build -t ntfy-scheduler .
   ```

2. **Run the Docker containers:**

   ```sh
   podman run -d -p 5000:5000 --rm --name ntfy-scheduler localhost/ntfy-scheduler:latest
   ```

   This command will start the application and the database service. The web application will be available at `http://localhost:5000`.

3. **Stopping the containers:**

   ```sh
   podman stop ntfy-scheduler
   ```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/savitojs/ntfy-scheduler.git
    cd ntfy-scheduler
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    bash entrypoint.sh
    ```

5. Open your web browser and go to `http://localhost:5000`.

## Files and Structure

Here’s a quick tour of the files and what they do:

### `main.py`
- The main Flask application file. It sets up the routes and starts the server.

### `database.py`
- Handles all database operations, including initialization, adding, editing, and retrieving messages, servers, and topics.

### `scheduler.py`
- Contains the scheduling logic, including checking for messages to send and handling the message sending process.

### `templates/index.html`
- The main HTML file for the app. It includes the form for scheduling messages and sections for viewing scheduled and sent messages.

### `static/js/scripts.js`
- Contains the client-side JavaScript for handling form submissions, dynamic content loading, and interaction with the API.

### `static/css/styles.css`
- Custom styles for the application.

## API Endpoints

Here’s a quick rundown of the API endpoints and what they do:

### `POST /schedule`
- Schedule a new message.
- **Required Data**: `message`, `datetime`, `server`, `topic`
- **Optional Data**: `interval`, `custom_days`, `timezone`, `header_title`, `header_priority`, `header_tags`

### `GET /scheduled`
- Get all scheduled messages.

### `GET /sent`
- Get all sent messages.

### `DELETE /delete/<int:id>`
- Delete a scheduled message by ID.

### `PUT /edit/<int:id>`
- Edit an existing scheduled message.
- **Required Data**: `message`, `datetime`, `server`, `topic`, `interval`, `custom_days`, `timezone`, `headers`

### `GET /topics`
- Get all topics.

### `POST /add_topic`
- Add a new topic.
- **Required Data**: `name`

### `DELETE /delete_topic/<int:id>`
- Delete a topic by ID.

### `GET /servers`
- Get all servers.

### `POST /add_server`
- Add a new server.
- **Required Data**: `address`

### `DELETE /delete_server/<int:id>`
- Delete a server by ID.

### `GET /default_server`
- Get the default server.

### `POST /set_default_server`
- Set the default server.
- **Required Data**: `server`

### `GET /default_topic`
- Get the default topic.

### `POST /set_default_topic`
- Set the default topic.
- **Required Data**: `topic`

## Usage

1. **Schedule a Message**: Fill out the form on the main page to schedule a new message. You can set a specific time and choose if the message should repeat.

2. **View Scheduled Messages**: Click on "View Scheduled Messages" to see all messages that are scheduled to be sent.

3. **View Sent Messages**: Click on "View Sent Messages" to see all messages that have been sent.

4. **Manage Topics**: Click on "Manage Topics" to add or delete topics.

5. **Manage Servers**: Click on "Manage Servers" to add or delete servers.

## Contributing

Feel free to fork the repository and submit pull requests. I appreciate any contributions to make this project better!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

Enjoy scheduling your messages with our awesome app! 🚀
