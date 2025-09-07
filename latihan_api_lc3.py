import pandas as pd
from fastapi import FastAPI, HTTPException


app = FastAPI()

df = pd.read_csv('latihan_api_lc3.csv')
data_dict = df.to_dict(orient='index')


# 1. GET

@app.get("/")
def read_data():
    return data_dict


# 2. PUT

@app.put("/items/{item_id}")
def update_item(item_id: int, update_data: dict):
    if item_id not in data_dict:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    
    data_dict[item_id].update(update_data)  # update hanya field yang dikirim
    return {
        "message": f"Item with ID {item_id} has been updated successfully.",
        "updated_item": data_dict[item_id]
    }

# 3. POST

current_id = len(data_dict)

@app.post("/items/")

def create_item(new_item: dict):
    global current_id
    current_id += 1  # increment ID setiap kali insert
    data_dict[current_id] = new_item
    return {
        "message": f"Item with ID {current_id} has been created successfully.",
        "new_item": data_dict[current_id]
    }

# 4. DELETE

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in data_dict:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    
    data_dict.pop(item_id)
    return {"message": f"Item with ID {item_id} has been deleted successfully.", "data": data_dict}