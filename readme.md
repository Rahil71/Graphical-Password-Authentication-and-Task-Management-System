# Graphical Password Authentication and Task Management System

## Description

This project implements a **Graphical Password Authentication** system combined with a **Task Management System (To-Do List)**, developed using **Flask**, **PostgreSQL**, and **Redis**. The system allows users to securely authenticate via graphical images, create tasks, and manage their to-do lists. This application ensures a seamless user experience with a focus on security, performance, and task organization.

## Features

- **Graphical Password Authentication**: Users authenticate by selecting a set of images they’ve previously chosen during sign-up.
- **To-Do List**: Users can manage tasks, add new ones, and delete existing ones from their personal to-do list.
- **PostgreSQL Integration**: The app uses PostgreSQL as the primary database backend to store user credentials, selected images for authentication, and task lists.
- **Redis Caching**: The app leverages Redis to cache frequently accessed user data, improving login performance and reducing database load.

## Prerequisites

Before running the application, ensure that you have the following installed:

- **Python 3.x**: The application is developed in Python.
- **PostgreSQL**: The database backend for storing user information and tasks.
- **Redis**: A high-performance in-memory data store used for caching.
- **Flask**: The web framework used to build the app.
- **Flask-SQLAlchemy**: For ORM-based database interaction.

You can install the necessary Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

**Requirements.txt**

```txt
flask==3.1.0
Flask-SQLAlchemy==3.0.3
psycopg2==2.9.1
redis==5.2.1
```

## Database and Redis Setup

### PostgreSQL

This application uses **PostgreSQL** as the database. Follow the steps below to set it up:

1. **Install PostgreSQL**: If you don't have PostgreSQL installed, download and install it from [PostgreSQL official website](https://www.postgresql.org/download/).

2. **Create a Database**: Create a database for this project (e.g., `lexus`).

    ```bash
    psql -U postgres
    CREATE DATABASE lexus;
    ```

3. **Update Database URI**: Update the database URI in `app.py`:

    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:<your-password>@localhost/lexus"
    ```

4. **Run Database Migrations**: Run the `table.py` script to create the necessary tables in the PostgreSQL database.

    ```bash
    python table.py
    ```

    This will create the required tables (`users` and any other necessary tables) in your `lexus` database.

### Redis

This application uses **Redis** to cache user data for performance optimization. Follow these steps to set up Redis:

1. **Install Redis**: Install Redis on your machine. For installation instructions, visit [Redis Official Website](https://redis.io/).

2. **Start the Redis Server**: Start the Redis server to enable caching.

    ```bash
    redis-server
    ```

3. **Verify Connection**: Ensure that Redis is running and accessible on `localhost` at port `6379` (default settings). No additional configuration is required unless you use a custom setup.

4. **Integration in App**: Redis is used to store user session data and improve login efficiency by reducing database queries. Data like `user credentials` and `selected images` are cached during login and sign-up processes.

## File Structure

The directory structure is as follows:

```
└── Rahil71-Graphical-Password-Authentication-and-Task-Management-System/
    ├── app.py                  # Main application logic
    ├── table.py                # Creates the database tables
    ├── static/
    │   ├── styles.css          # CSS styles for the web pages
    │   └── .DS_Store           # macOS specific file (can be ignored)
    └── templates/
        ├── home.html           # Home page template
        ├── login.html          # Login page template
        ├── signup.html         # Sign-up page template
        └── success.html        # Dashboard page (after successful login)
```

## Running the Application

To run the application locally, use the following steps:

1. **Set up the virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:

    ```bash
    python app.py
    ```

    By default, the app will run on `http://127.0.0.1:5000/`.

## Routes

- `/home`: The home page where users can navigate to login or signup.
- `/login`: The login page where users can authenticate using their username, email, password, and selected images.
- `/signup`: The sign-up page where new users can create an account by choosing their username, email, password, and selecting images.
- `/success`: The dashboard where users can manage their to-do list (add/delete tasks).

## User Authentication

- During **Sign-Up**, users are asked to select a set of images that will be used for authentication.
- During **Login**, users must enter their username, email, password, and select the same images they initially selected during sign-up to authenticate.

### Redis Caching in Authentication

- **Sign-Up**: User data, including selected images, is stored in PostgreSQL and cached in Redis for quick access.
- **Login**: The app first checks Redis for user data. If found, it avoids querying the database and validates user credentials directly from Redis. This reduces latency and improves performance.

## Screenshots

Here are some screenshots of the application:

### 1. Home Page

![Home Page](./static/images-git/homepage.png)

### 2. Login Page

![Login Page](./static/images-git/login.png)

### 3. Sign-Up Page

![Sign-Up Page](./static/images-git/signup.png)

### 4. Success Page (Dashboard)

![Success Page](./static/images-git/success1.png)

![Success Page](./static/images-git/success2.png)

### 5. PostgreSQL Database

![PostgreSQL Database](./static/images-git/postgresql.png)

### 6. Redis Database
![Redis Database](./static/images-git/redis.png)

## Technologies Used

- **Flask**: The web framework for building the application.
- **Flask-SQLAlchemy**: The ORM used for database interaction.
- **PostgreSQL**: The relational database used to store user information and tasks.
- **Redis**: The in-memory data store used for caching user data.
- **HTML/CSS**: For the front-end design of the web pages.

## Contribution

Feel free to fork the repository and submit pull requests. If you find any bugs or issues, please open an issue so that it can be addressed.

