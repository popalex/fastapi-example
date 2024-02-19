import logging
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from alembic.config import Config
from alembic import command

from schema import Book as SchemaBook, FullBook
from schema import Author as SchemaAuthor

from schema import Book
from schema import Author

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

def run_all_migrations():
    # setup environment variable to ignore logging changes from env.py
    os.environ['FROM_MAIN'] = 'true'
    BASE_DIR= os.path.dirname(os.path.abspath(__file__))
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

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/book/', response_model=FullBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id = book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


  
@app.post('/author/', response_model=Author)
async def author(author:SchemaAuthor):
    db_author = ModelAuthor(name=author.name, surname=author.surname, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get('/author/')
async def author():
    author = db.session.query(ModelAuthor).all()
    return author


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)