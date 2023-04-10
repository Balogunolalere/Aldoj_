# Aldoj Agri-Investment Platform

Aldoj is an agricultural investment platform that connects investors with available investment opportunities in the agricultural sector. The platform allows investors to invest in various properties and monitor their investments through a user-friendly interface. The backend is built with Django and Django Rest Framework.

## Table of Contents

    Features
    Installation
    Usage
    Testing
    API Documentation
    Contributing
    License

## Features

    User registration and authentication
    Investor and staff user roles
    Property listing and management
    Investment management
    Crop management
    Search, filter, and ordering for listings
    Django admin customization

## Installation

### Clone the repository.
    git clone https://github.com/your_username/aldoj_project.git

### Create a virtual environment and activate it.
    python -m venv venv
    source venv/bin/activate

### Install the required packages.
    pip install -r requirements.txt

### Apply migrations.
    python manage.py migrate

### Create a superuser for the Django admin.
    python manage.py createsuperuser

### Start the development server.
    python manage.py runserver

Now you can access the application at http://127.0.0.1:8000/.

## Usage
    Visit the Django admin at http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

    Create new properties, investments, and crops through the Django admin.

    Interact with the API endpoints to register users, log in, and manage investments.

## Testing
    To run the test suite, execute the following command:
    python manage.py test

