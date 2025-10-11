from fastapi import FastAPI,Path
import json


app = FastAPI()

def load_data():
    with open('patients.json',"r") as file:
        data = json.load(file)
    return data



@app.get("/")
def home():
    return {"Message": "Hello, World!"}








