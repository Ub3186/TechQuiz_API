from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from config import db
from models import models
from functions import map_question

app = APIRouter()
c = db.c
convert_question = map_question.convert_question

@app.post("/question/c/add")
async def add_c_question(question:models.Question):
    response = c.insert_one(question.dict())
    return question.dict()

@app.get("/question/c/basic")
async def get_basic_question(skip=0, limit=10):
    response = c.find({
        "type":"basic"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/c/intermediate")
async def get_intermediate_question(skip=0, limit=10):
    response = c.find({
        "type":"intermediate"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/c/complex")
async def get_complex_question(skip=0, limit=10):
    response = c.find({
        "type":"complex"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.delete("/question/c/delete")
async def delete_c_question(id):
    response = c.find_one_and_delete({
        "_id":ObjectId(id)
    })
    response["_id"] = str(response["_id"])
    return response