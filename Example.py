import json
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery, storage
from google.oauth2 import service_account

from fastapi.responses import HTMLResponse
import pandas as pd

key_path = "cloudkarya-internship-32c8df6a1507.json"
bigquery_client = bigquery.Client.from_service_account_json(key_path)
storage_client = storage.Client.from_service_account_json(key_path)

project_id = "cloudkarya-internship"

class Item(BaseModel):
    book_id: str
    book_name: str 
    book_author_id: str
    book_author_name: str

app = FastAPI()

@app.get('/books/',response_class=HTMLResponse)
async def book():
   query = f"""
         SELECT  * FROM {project_id}.Books.books;
   """
   df = bigquery_client.query(query).to_dataframe()
   # df.head()
   return df.to_html()

@app.post("/items/")
async def create_item(item: Item):
    print(item)
    item = json.dumps(item.__dict__)
    '''query = f"""
    INSERT INTO {project_id}.Books.books VALUES({item});
    """'''
    query = f"""
    INSERT INTO `{project_id}.Books.books`
    VALUES(JSON_EXTRACT_SCALAR('{item}', '$.book_id'),
           JSON_EXTRACT_SCALAR('{item}', '$.book_name'),
           JSON_EXTRACT_SCALAR('{item}', '$.book_author_id'),
           JSON_EXTRACT_SCALAR('{item}', '$.book_author_name')
           );
    """
    db_book = bigquery_client.query(query)
    print(db_book)
    return db_book