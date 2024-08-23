# Django Project

This is a Django project that provides a web application for companies to post internship opportunities for graduated people and for students. In this project we make an api for the internship data from the database. This README file contains instructions for setting up and running the project.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Explainable AI Integration](#explainable-ai-integration)
- [License](#license)
- [Contact](#contact)

## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (version 3.11 or later)
- pip (Python package installer)
- Virtualenv (optional but recommended)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Ali-Jaan-Butt/Django-rest-api.git

2. **Installations:**
   Install all the libraries required specially Django using pip.
   ```bash
   pip install Django
   pip install pymongo
   pip install smtplib
   pip install fastapi
   pip install sentence_transformers
   pip install requests

4. **Connect Database:**
   Install MongoDB GUI on your system and then run
   ```bash
   cd db
   mongod --dbpath ./

## Configuration

### Check all the requirements installed or not.
### You need to be in root directory in terminal where "manage.py" file is located.

## Running the project

### To run project we should have to run the server.

Be in the root directory where the manage.py file is located, then

1. **Run Server**
   ```bash
   python manage.py runserver

## Testing

### You can test the project by using the website at locsl host: "http://127.0.0.1:8000"

## Explainable AI integration

### I have also integrated AI in it which is cosine text similarity for checking the similarity between the student tags and company internships description. So that right internship will reach to the right person.

## Licence

### Having MIT licence to this project

## Contact

- **Name:** Ali Jaan Butt
- **Email:** aliwsservices@gmail.com
- **Phone:** +923201540500
