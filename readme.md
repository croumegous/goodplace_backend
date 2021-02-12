# Backend Requirements
* [Docker](https://www.docker.com/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

# Instalation
```bash
poetry install
```

# Run
Rename .env.template to .env and set your own configuration.
Generate a new ACCESS_TOKEN_SECRET_KEY and REFRESH_TOKEN_SECRET_KEY with : 
```bash
openssl rand 256 | base64
```

Before running the application you must create database table see [here](./migrations/README.md)
```bash
poetry run uvicorn main:app --reload
```

# Instructions

There are 5 main folder in this backend:
> apis/v1  
Where are defined all api endpoints

> crud  
CRUD function (query to database)

> db/models  
Models for the ORM

> schemas  
Pydantic schemas to validate and serialize api payloads and returns

> core  
Core and useful functions for the project


# Usage 
You can find documentation of api endpoints in production here: https://api.goodplace.cyril-roumegous.com/docs 