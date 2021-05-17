# Breeze App
### One app for manager spotify playlists

## About this project
This app is a project made for spotify api case study, with it is
possible to manage your favorite playlist. This application is able to connect
with a spotify account using your authentication system and listing,
add and remove songs from a playlist.

The application also has an api for external use in other applications of the data saved in this application.

## Installation

To run this project, you must have installed in your development environment:

- Python ~= 3.9
- PostgreSql ~= 12.6
- redis ~= 6.0

To install the project, you must clone this repository, and in the desired folder, follow the following step by step:
<br>1- $ python install pipen
<br>2- $ pipenv install
<br>3- $ pipenv install --dev
<br>4- $ psql (utilize suas credenciais para acessar)
<br>5- $ create database breeze;
<br>6- $ \q -->  para sair do postgresql
<br>7- $ ./manage.py migrate
<br>8- $ ./manage.py runserver

The project will be available at: http://localhost:8000/

## Functionalities
In this project you will find:

- Registration, login and password recovery system
- Authentication with spotify api and automatic token update when accessing the application's endponts
- Spotify playlist CRUD
- CRUD of songs related to playlists
- Storage of data retrieved from the api
- Api for accessing application data using JWT authentication standard
- Simple automation of data listing using redis and celery

## Running Api

To access the api for this project, you must generate an authentication token at the endpoint:
- POST http://localhost:8000/api/token/ 
- in body:

{
    "username": ["{{put your username here }}"]
    "password": ["{{put your password here}}"]
}

If the token has expired, access the following link and pass the token as a parameter:, If the token has expired, visit the following link and pass the token as a parameter:
- POST http://localhost:8000/api/refresh_token/
- int body:

{
    "token": ["{{put your old token here}}"]
}

The api has the following endpoints:
-  GET, POST, PUT e DELETE http://localhost:8000/api/v1/track
-  GET, POST, PUT e DELETE http://localhost:8000/api/v1/playlists

## Running celery automation

For case study, I implemented an automation with celery, using the broker redis to run an automation that lists users' playlists every 60 seconds.

To run, just type the following command:

$ celery -A breeze_project beat --loglevel=info