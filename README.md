This project is a web application that allows users to create and add links to collections, from which the service will automatically collect information. Key features include:

- User registration with verification via email
- Authentication using JWT token
- Changing your password and recovering your password via email
- Create, view, edit and delete links
- Create, view, edit, and delete collections
- API documentation in Swagger
- Filling with test data using a script
- Endpoint with complex SQL query

**To run this application locally, follow these steps:**

Clone the repository: git clone https://github.com/AnastasiaSavenok/xOneProject.git
Go to the project directory: cd xOneProject/
Create a .env file and specify the following variables in it:
- SECRET_KEY (for example: django-insecure-vuwdf%4f$uvhfg!9w+2ikx(zumsvp9o&g4ep3-gch)s=+(*th+ )
- DEBUG
- DJANGO_ALLOWED_HOSTS (for example: 0.0.0.0)
- POSTGRES_ENGINE = django.db.backends.postgresql_psycopg2
- POSTGRES_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- EMAIL_ADDRESS (address from which the verify code will be sent)
- EMAIL_PASSWORD (Password for applications)
Launch the application in one of two ways:
- Build and run Docker containers: docker-compose up --build
- Install requirements: pip install -r requirements.txt and run: python manage.py runserver 
Open the swagger application documentation in a browser: http://localhost:8000/api/v1/docs/
