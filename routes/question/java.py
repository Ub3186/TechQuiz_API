from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from config import db
from models import models
from functions import map_question

app = APIRouter()
java = db.java
convert_question = map_question.convert_question

@app.post("/question/java/add")
async def add_java_question(question:models.Question):
    response = java.insert_one(question.dict())
    return question.dict()

@app.get("/question/java/basic")
async def get_basic_question(skip=0, limit=10):
    response = java.find({
        "type":"basic"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/java/intermediate")
async def get_intermediate_question(skip=0, limit=10):
    response = java.find({
        "type":"intermediate"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/java/complex")
async def get_complex_question(skip=0, limit=10):
    response = java.find({
        "type":"complex"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.delete("/question/java/delete")
async def delete_java_question(id):
    response = java.find_one_and_delete({
        "_id":ObjectId(id)
    })
    response["_id"] = str(response["_id"])
    return response