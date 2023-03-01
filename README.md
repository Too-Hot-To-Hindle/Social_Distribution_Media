[![Deploy to Heroku](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/actions/workflows/heroku.yml/badge.svg?branch=main)](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/actions/workflows/heroku.yml)

# Social_Distribution_Media

[Deployed App](https://social-distribution-media.herokuapp.com/) | [API Documentation](https://social-distribution-media.herokuapp.com/api/schema/swagger-ui/)

[Project implementation](https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org) of a social network using the inbox model.

## Running Instructions

Our app uses a React frontend and Django backend. The frontend code is built and copied to the `backend/build` directory, which is served when running the Django app.

When making changes, the new version is automatically built and depolyed to Heroku by a [github action](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/blob/main/.github/workflows/heroku.yml).

### React Setup

#### Install packages

`cd frontend`

`npm install`

#### Copy build files to Django project

`npm run relocate`

This will build the app and copy the `/build` folder to `/backend/build`, where Django will serve it.

> **_NOTE:_** You can also use `npm run start`, but this won't have access to the backend

### Django Setup

#### Virtual Environment

`cd backend`

Create a virtual environment

e.g. `virtualenv venv`

Activate the environment

`. venv/bin/activate`

Install all the required packages

`pip install -r requirements.txt`

#### Local DB

Run intial migrations

`python manage.py migrate`

Create Superuser

`python manage.py createsuperuser`

#### Run App

`python manage.py runserver`