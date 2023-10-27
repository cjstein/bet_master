# Bet Master

Create and consolidate bets

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT
## Initial Setup
1. Download the code
2. Create a virtual environment `python -m venv venv`
    - If you name it venv, it will already be in the gitignore
3. Activate the new environment
4. Download requirements: `pip install -r requirements/local.txt`
5. Download Version 15 of [Postgres](https://www.postgresql.org/download/windows/)
    - Create a DB, an admin user and password.  Save this to put in your Environment Variable file next.
6. Copy the `template.env` file and name it just `.env`
    - Update the variables to match your local setup
    - you will have to add the environment variable `DJANGO_READ_DOT_ENV_FILE` to you systems Environment Variables and set it to True
7. Run `python manage.py migrate`
8. Run `python manage.py runserver`
    - To ensure the initial setup is correct
## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy bet_master

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
