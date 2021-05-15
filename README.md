# Breeze App
### One app for manager spotify playlists

## About this project
This app is a project feito para estudo de caso da api do spotify, com ele é 
possível gerenciar sua playlist favorita. Este aplicativo é capaz de se conectar
com uma conta do spotify utilizando seu sistema de autenticação e listar, adicionar e remover músicas de uma playlist.

A aplicação conta também com uma api para uso externo em outras aplicações dos dados salvos nesta aplicação.

## Workflow


## Installation

Para rodar este projeto, você deve ter instalado em seu ambiente de desenvolvimento:

- Python ~= 3.9
- PostgreSql ~= 12.6
- redis ~= 6.0

Para instalar o projeto, você deve clonar este repositório, e na pasta desejada,seguir o seguinte passo a passo:
<br>1- python install pipen
<br>2- pipenv install
<br>3- pipenv install --dev
<br>4- psql (utilize suas credenciais para acessar)
<br>5- create database breeze;
<br>6- \q -->  para sair do postgresql
<br>7- ./manage.py migrate
<br>8- ./manage.py runserver

O projeto ficará disponível em: http://localhost:8000/


## Functionalities
Neste projeto você vai encontrar:

- Sistema de cadastro, login e recuperação de senha
- Authenticação com api do spotify e atualização automática de token ao acessar os endponts da aplicação
- CRUD de playlist do spotify
- CRUD de músicas relacionadas a playlists
- Armazenamento de dados recuperados da api
- Api de acesso aos dados da aplicação utilizando padrão de atuenticação JWT
- Automatização simples de listagem de dados utilizando redis e celery

## Running Api

Para acessar a api deste projeto acesse: 

### JWT AUTHENTICATION
A api possui os seguintes endpoints

GET

PUT 

POST

DELETE

## Running celery automation

Para estudo de caso, implementei uma automação com celery, utilizando o broker redis para rodar uma automação que lista as playlists dos usuários a cada 60 segundos.

Para rodar 