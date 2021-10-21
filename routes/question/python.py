from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from config import db
from models import models
from functions import map_question

app = APIRouter()
python = db.python
convert_question = map_question.convert_question

@app.post("/question/python/add")
async def add_python_question(question:models.Question):
    response = python.insert_one(question.dict())
    return question.dict()

@app.get("/question/python/basic")
async def get_basic_question(skip=0, limit=10):
    response = python.find({
        "type":"basic"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/python/intermediate")
async def get_intermediate_question(skip=0, limit=10):
    response = python.find({
        "type":"intermediate"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/python/complex")
async def get_complex_question(skip=0, limit=10):
    response = python.find({
        "type":"complex"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.delete("/question/python/delete")
async def delete_python_question(id):
    response = python.find_one_and_delete({
        "_id":ObjectId(id)
    })
    response["_id"] = str(response["_id"])
    return response