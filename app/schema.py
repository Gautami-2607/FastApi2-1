# build a schema using pydantic
from pydantic import BaseModel

class Book(BaseModel):
   book_id: str
   book_name: str
   book_author_id: str
   book_author_name: str

   class Config:
       orm_mode = True

class Author(BaseModel):
   name:str
   age:int

   class Config:
       orm_mode = True
      


