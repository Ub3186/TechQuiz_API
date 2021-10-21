from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from config import db
from models import models
from functions import map_question

app = APIRouter()
cpp = db.cpp
convert_question = map_question.convert_question

@app.post("/question/cpp/add")
async def add_cpp_question(question:models.Question):
    response = cpp.insert_one(question.dict())
    return question.dict()

@app.get("/question/cpp/basic")
async def get_basic_question(skip=0, limit=10):
    response = cpp.find({
        "type":"basic"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/cpp/intermediate")
async def get_intermediate_question(skip=0, limit=10):
    response = cpp.find({
        "type":"intermediate"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.get("/question/cpp/complex")
async def get_complex_question(skip=0, limit=10):
    response = cpp.find({
        "type":"complex"
    }).skip(int(skip)).limit(int(limit))

    questions = map(convert_question, response)
    return list(questions)

@app.delete("/question/cpp/delete")
async def delete_cpp_question(id):
    response = cpp.find_one_and_delete({
        "_id":ObjectId(id)
    })
    response["_id"] = str(response["_id"])
    return response