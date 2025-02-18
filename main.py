from fastapi import FastAPI, HTTPException
'''
pip install fastapi uvicorn 
'''

# Using basemodel
from pydantic import BaseModel

# Documentation: http://127.0.0.1:8000/docs
# Documentation: http://127.0.0.1:8000/redocs
app = FastAPI()

class Item(BaseModel):
    text: str = None # Removing '= None' makes the text field required
    is_done: bool = False
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://127.0.0.1:8000/items' <-- Will Work if we remove '= None'
    curl -X POST -H "Content-Type: application/json" -d '{"title":"apple"}' 'http://127.0.0.1:8000/items' <-- Will work if there is no text field requirement
    '''

items = []

# uvicorn main:app --reload
@app.get("/")
def root():
    return {"Hello": "World"}



#   curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple'
#       --> Use case when using an array

#   curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://127.0.0.1:8000/items'
#       --> Use case when using a BaseModel
@app.post("/items")
def create_item(item: Item): # Using a model object
    items.append(item)
    return items



#  curl -X GET 'http://127.0.0.1:8000/items?limit=3'
@app.get("/items", response_model=list[Item]) # 'response_model=list[Item]' ensures the response is a list of Item objects and follows the correct format.
def list_items(limit: int = 10): # Default Value = 10
    return items[0:limit]



# curl -X GET http://127.0.0.1:8000/items/5
@app.get("/items/{item_id}", response_model=Item) # 'response_model=Item' makes sure the response is a single Item and follows the correct format.
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        # Raise an Error if an item that doesn't exist is requested
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")