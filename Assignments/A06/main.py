import pymongo
import pprint
import random
import json
from typing import Optional,List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse,HTMLResponse 
from bson.objectid import ObjectId
from geojson import Feature, Point
from pydantic import BaseModel,Field
from pymongo.message import query
import uvicorn


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['Restaurant']
collection = db['restaurant']


class mymodel(BaseModel):
    restaurant_id: str 
    name: str 
    address: dict
    cuisine: str  
    borough: str 
    grades: list

class distance(BaseModel):
    x: float
    y: float


app = FastAPI()

@app.get("/")
async def root(request: Request):
    return {
        #"Listing of all routes": request.url_for("routes"),
        "URL for 'categories'": request.url_for("categories"),
        "URL for ''restaurants'": request.url_for("restaurants"),
        "URL for ''ratings' with value 13 for test": request.url_for("all_ratings", **{"rate": 13}),
        "URL for ''categories' by cuisine for example Mexican ": request.url_for("by_cuisine", **{"cuisine": "Mexican"}),
        "URL for ''location' go to postman to pass in dictionary of coordinates": request.url_for("location"),
        "URL for ''zipcode' go to postman to pass in a list element for zipcode": request.url_for("by_zipcode"),
       
    }

# @app.get("/", response_class=HTMLResponse)
# async def all_routes():
#     all_routes ="""
#         <a href= /categories> click for cuisine list</a><br>


#         <a href= /resturants> click for resturants list and count</a><br>

#         <a href= /rating/11> Ratings</a><br>
        
    
#     """
#     #    <a href= /rating> Ratings</a>
    
#     #note =f"Here is a list of all the routes.<br> " + all_routes
    
        
#     return HTMLResponse(content=all_routes, status_code=200)



@app.get("/categories", name= "categories")
async def allcats():
    res = list(collection.distinct('cuisine'))
    if not res:
        raise HTTPException(status_code=404)
    return {"count":len(res),"data":res}

@app.get("/restaurants", name= "restaurants")
async def resturentsall():
    response_list = []
    res = list(collection.find().skip(100).limit(1000))
    
    for r in res:
            response_list.append(mymodel(**r))
    return {"count is ":len(res),"data":response_list}

@app.get("/rating/{rate}")
async def all_ratings(rate:int):
    response_list = []
    stuff ={"grades.score":{"$gte":rate}}
    res= collection.find(stuff).skip(100).limit(1000)
    
    for r in res:
        response_list.append(mymodel(**r))
    return response_list

@app.get("/categories/{cuisine}")
async def by_cuisine(cuisine:str):
    sample ={'cuisine':cuisine}
    res = collection.find(sample)
    count = res.count()
    response_list = []
    toadd = f'<a href= /categories> click for cuisine list</a>'
    if(count ==0):
        note =f"{cuisine} is not in the list of genre.<br> " + toadd
        return HTMLResponse(content=note, status_code=200)
    else:
        for r in res:
            response_list.append(mymodel(**r))
        return response_list

@app.get("/location/")
async def location(latlong:distance):
    
    query = list(collection.find(
   {
     "location":
       { "$near":
          {
            "$geometry": { "type": "Point",  "coordinates": [latlong.x, latlong.y] },
            "$minDistance": 1000,
            "$maxDistance": 5000
          }
       }
   },{"_id":0}
))
    #print(latlong)

    res = {'result': query}
    
    return res

  

@app.get("/zipcode")
async def by_zipcode(Zips:list):
    zipcodes_arr =[]
    for zip in Zips:
        zipcodes_arr.append(str(zip))
    stuff = { "address.zipcode": {"$in":zipcodes_arr}}
    res = collection.find(stuff)
    response_list = []
    for z in res:
        response_list.append(mymodel(**z))
    return response_list

if __name__ == "__main__":
  uvicorn.run(app, host="143.244.188.178", port=8003, log_level="info")
