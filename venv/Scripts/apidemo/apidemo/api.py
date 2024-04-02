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
    id: Optional[int] = None      #Optional[int]: This is a type hint indicating that the variable can be of type int or None. 
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
    
    # Update book fields with values from payload
    for field, value in payload.dict().items():
        setattr(book, field, value)
    
    # Save the updated book object to the database
    book.save()
    
    # Return a JSON response with the updated data
    return JsonResponse({"success": True, "data": payload.dict()})     #The purpose of exclude_unset=True is to exclude fields that have not been set or have their default values.

"""
"payload": This is an instance of the BookPatchSchema class, which is likely a Pydantic model representing the data expected for patching a book (partial update).

"payload.dict()": This method call converts the payload object into a dictionary. By default, it includes all fields defined in the schema, whether they have been explicitly set or not.

"exclude_unset=True": This argument specifies that only fields that have been explicitly set with a value other than the default value should be included in the resulting dictionary. Fields that have not been set (i.e., unset fields) are excluded from the dictionary.
"""

