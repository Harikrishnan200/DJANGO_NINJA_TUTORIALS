from ninja import  NinjaAPI,Schema,ModelSchema
from django.shortcuts import get_object_or_404
from books.models import Book, Author
from django.http import JsonResponse
from typing import Optional

api = NinjaAPI()
"""
class BookSchema(ModelSchema):  #In Django Ninja, a Schema is a class that defines the structure of the data that will be received or sent by the API. It is used to validate and serialize the data.
    id: int
    title: str
    author_id: int
    description: str
    isbn: str 
"""
# instead of this we can define the BookSchema using ModelSchema
    
class AuthorSchema(ModelSchema):
    class Meta:
        model=Author    
   #   fields = "__all__"   # include all fields in serialization/deserialization process 
        fields= ['name']

class BookSchema(ModelSchema): 
    author : AuthorSchema   #used to connect  with Author model

    class Meta:
        model = Book
        fields = "__all__"  

class BookInSchema(Schema):
    id: int
    title: str
    author_id: int
    description: str
    isbn: str 

class BookPatchSchema(Schema):
    id: Optional[int] = None
    title: Optional[str] = None
    author_id: Optional[int] = None
    description: Optional[str] = None
    isbn: Optional[str] = None 



@api.get("/hello")
def hello(request):
    return {'message': 'Hello World'}


@api.get("/books/{book_id}", response=BookSchema)  #The 'response' parameter of the @api.get decorator specifies the response schema.
def book_detais(request, book_id:int):
    book = get_object_or_404(Book,id = book_id)
    return book


@api.get("/books", response=list[BookSchema])
def book_list(request):
    return Book.objects.all()


@api.post( "/books/" ,response=BookSchema )
def create_book(request,payload:BookInSchema):
    """Create a new book."""
    book = Book.objects.create(**payload.dict())  
    return book

@api.delete("/books/{book_id}")
def delete_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@api.patch("/books/{book_id}")    
def edit_book(request, book_id: int, payload: BookPatchSchema):
    book = get_object_or_404(Book, id=book_id)
    # Apply changes from payload to the book object here
    return payload.dict(exclude_unset=True)   #The purpose of exclude_unset=True is to exclude fields that have not been set or have their default values.