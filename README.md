A very simple quiz game about books for a fatec project.

# Requirements
- python 3.6 >
- pip

# Running it locally
Its quite simple, just install the requirements:
- `pip install -r requirements`
- `python manage.py migrate`
- `python manage.py runserver`

# Running it on docker
### You must have docker and docker compose installed
- `docker-compose build`
- `docker-compose up`

# Before the first access
You must create the admin user:

## Locally
- `python manage.py createsuperuser`

## On docker
- `docker-compose run web python manage.py createsuperuser`

It will ask you to fill some information about the user.
Consult [here](https://docs.djangoproject.com/en/3.0/intro/tutorial02/#creating-an-admin-user) if you have any throuble.

# Access
- For access the admin just go to `http://localhost:8000/admin`, in this page you can create new users, books, questions about books etc.
- For access the quiz itself you go to `http://localhost:8000`.
