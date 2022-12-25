# Store API - FastAPI
> This is a study project of a API in FastAPI with Store (User, Seller, Departments) as theme.

### Attentions
This project has some problems:
* It's not connecting with db when the app is running in a container (swagger is running)
* The docker compose has only postgres;
* If you want to try, execute the container with postgres and run the app in python;
* Before run in python, you need to execute: `python create_tables.py` in app folder to drop and create all tables.

### What is used in this project
* FastAPI:
    * Models;
    * Schemas;
    * Async.
* SQLAlchemy;
* Postgres;
* Authentication with Bearer Token.


### Swagger
* Running swagger when the application is running in: `http://localhost:8000/docs` or `http://localhost:8000/redoc`


### Docker Commands
* To create a Postgres container execute: `docker compose -up`;
* To create a app's image: `docker run --name fastapi-ctn -p 8000:8000 -d fastapi-img`;
* To create a container with the app img: `docker build -t fastapi-img .`.

### Future Improvements
1. Create `migrations` using Alembic;
2. Discover how to create tests with async functions (using a test-db);
3. Fix connection between Postgres and Application in Docker Compose;
4. Refactor all code.