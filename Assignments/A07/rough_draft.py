import uvicorn
from typing import Collection, Optional, List
from fastapi.params import Query
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.errors import ListError
import pymongo
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.requests import ClientDisconnect
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['Advising']
collection = db['Schedules']


# class User(BaseModel):
#     _id: ObjectId
#     col: str
#     crn: int
#     subj: str
#     sect: int
#     title: str
#     primaryinstructor: str
#     Max: int
#     curr: int
#     aval:Optional = None
#     days: str
#     begin: str
#     end: str
#     bldg: str
#     room: str

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")



class AdvisingModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    col: str = Field(...)
    crn: int = Field(...)
    subj: str = Field(...)
    crse: int = Field(...)
    sect: int = Field(...)
    title: str = Field(...)
    primaryinstructor: str = Field(...)
    Max: int = Field(...)
    curr: int = Field(...)
    aval: str = Field(...)
    days: str = Field(...)
    begin: str = Field(...)
    end: str = Field(...)
    bldg: str = Field(...)
    room: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        json_encoders = {ObjectId: str}



@app.get('/')
async def index():
    return {'hello':'world'}



@app.get('/home')
async def test():
    sampleQuery = list(collection.find({},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}


## Not currently working, not sure if student data is loaded properly into Mongo
@app.get('/home/Students/Gender={G}')
async def test(G: str):
    if G:
        sampleQuery = list(collection.find({'gender':G},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



@app.get('/home/Courses')
async def sample():

    Titles = collection.distinct('Title')

    return Titles


@app.get('/home/Courses/Subj=')
async def test():

    sampleQuery = list(collection.find({'Subj':{}},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}


@app.get('/home/Courses/Subj={subject}')
async def test(subject: str):
    if subject:
        sampleQuery = list(collection.find({'Subj':subject},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



@app.get('/home/Courses/CRN={crn}')
async def test(crn: str):
    sampleQuery = list(collection.find({'CRN':crn},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



@app.get('/home/Courses/CourseNum={crse}')
async def test(crse: str):
    sampleQuery = list(collection.find({'Crse':crse},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



@app.get('/home/Courses/Closed')
async def test():

    sampleQuery = list(collection.find({},{'_id':0}).limit(1000))
    test = []

    for index in sampleQuery:
        try:
            if index['Max'] == index['Curr']:
                test.append(index)
        except:
            continue


    result = {'result': test}

    return{'response': result}



@app.get('/home/Courses/Subj={subject}/Sect={section}')
async def test(subject: str, section: str):
    sampleQuery = list(collection.find({'Subj':subject,'Sect':section},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



@app.get('/home/Courses/Bldg={Bldg}/Room={Room}')
async def test(Bldg: str, Room: str):
    sampleQuery = list(collection.find({'Bldg':Bldg,'Room':Room},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}



# @app.get('/home/CMPS_Courses')
# async def sample():
#     sampleQuery = list(collection.find({'Subj':'CMPS'},{'_id':0}).limit(1000))

#     return sampleQuery



@app.get("/home/advising/", response_description="List all classes", response_model = List[AdvisingModel])
async def list_all_classes():
    sampleQuery = list(collection.find().limit(1000))

    return {'respone': sampleQuery}




if __name__== "__main__":
    
    uvicorn.run(app, host="143.244.188.178", port=8001, log_level="info", reload=True)
