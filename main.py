import logging
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from alembic.config import Config
from alembic import command

from schema import AuthorCreate, AuthorResponse, Book as SchemaBook, FullBook

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

def run_all_migrations():
    os.environ['FROM_MAIN'] = 'true'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    run_migrations(os.path.join(BASE_DIR, 'alembic'), os.environ['DATABASE_URL'])

def run_migrations(script_location: str, dsn: str) -> None:
    logging.warning('Running DB migrations in %r on %r', script_location, dsn)
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

run_all_migrations()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):  # Fixed
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post('/book/', response_model=FullBook)
async def post_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/book/')
async def get_book():
    books = db.session.query(ModelBook).all()
    return books

@app.post('/author/', response_model=AuthorResponse)  # Using AuthorResponse schema for the response
async def post_author(author: AuthorCreate):  # Using AuthorCreate schema for the input (no ID)
    db_author = ModelAuthor(name=author.name, surname=author.surname, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    db.session.refresh(db_author)  # Refresh to get the auto-generated ID from the database
    return db_author  # This will return the author with the ID included

@app.get('/author/')
async def get_author():
    authors = db.session.query(ModelAuthor).all()
    return authors

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
