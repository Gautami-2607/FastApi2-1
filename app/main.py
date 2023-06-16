import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.schema import Book as SchemaBook
from app.schema import Author as SchemaAuthor

from app.schema import Book
from app.schema import Author

from app.models import Book as ModelBook
from app.models import Author as ModelAuthor

import os
from dotenv import load_dotenv

from google.cloud import bigquery, storage
from google.oauth2 import service_account

from fastapi.responses import HTMLResponse

load_dotenv('.env')

key_path = "cloudkarya-internship-32c8df6a1507.json"
bigquery_client = bigquery.Client.from_service_account_json(key_path)
storage_client = storage.Client.from_service_account_json(key_path)

app = FastAPI()

# to avoid csrftokenError
# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

project_id = "cloudkarya-internship"

@app.get("/")
async def root():
   return {"message": "hello world"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
   query = f"""
   INSERT INTO {project_id}.Books.books VALUES("4","abcd","2","abcd");
   """
   client.query(query)
   return db_book

@app.get('/books/',response_class=HTMLResponse)
async def book():
   query = f"""
         SELECT  * FROM {project_id}.Books.books;
   """
   df = bigquery_client.query(query).to_dataframe()
   # df.head()
   return df.to_html()


@app.post('/author/', response_model=SchemaAuthor)
async def author(author:SchemaAuthor):
   db_author = ModelAuthor(name=author.name, age=author.age)
   db.session.add(db_author)
   db.session.commit()
   return db_author

@app.get('/authors/')
async def author():
   
   return author


# To run locally
if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)


