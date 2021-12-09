from random import sample
from typing import List
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse,HTMLResponse
from config.database import collection, collection_name, collection_test,collection_students
import pymongo
from models.schedules_models import Course, Todo, Student_info, Advising_form
from schemas.schedules_schema import  key_exist, courses_info, todo_serializer, todos_serializer, student_info, students_info,filter_course, advising_form, advising_forms
from bson import ObjectId


student_api_route = APIRouter()

@student_api_route.get('/home')
async def test():
    sampleQuery = list(collection.find({},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}

#Get course information
#Get All Courses
@student_api_route.get("/course/")
async def get_course_list():
    result = list(collection.find({},{"_id":0}).skip(0).limit(1000))
    for c in result:
        if not key_exist(c,["Bldg", "Room"]):
            #print(c)
            pass
    #print(result)
    #course_query = filter_course(result)
        
    return {"status": "ok", "result": result}
   
#Get Courses with distinct Title
@student_api_route.get('/course/title')
async def get_course_title():

    course_query = collection.distinct('Title')
    count = len(course_query)

    return {"Count": count, "List of Classes":course_query}

@student_api_route.get('/course/Subjects')
async def get_course_by_distint_subjects():

    course_query = collection.distinct('Subj')
    count = len(course_query)

    return {"Count": count, "List of Subject":course_query}


#Get Courses by subject
@student_api_route.get('/course/subj={subject}')
async def get_course_subject(subject: str):
    if subject:
        sampleQuery = list(collection.find({'Subj':subject},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return{'response': result}


#Get Courses by CRN
@student_api_route.get('/course/CRN={crn}')
async def get_course_crn(crn: str):
    sampleQuery = list(collection.find({'Crn':crn},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return result

#Get Course by instructor
@student_api_route.get('course/instructor={instructor}')
async def get_course_instructor(instructor: str):
    query = list(collection.find({'PrimaryInstructor':instructor},{'_id':0}).limit(1000))
    result ={'result': query}

    return result

#Get Course by building
@student_api_route.get('/course/building={bldg}')
async def get_course_building(bldg: str):
    sampleQuery = list(collection.find({'Bldg':bldg},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return result


#Get Courses by Course number
@student_api_route.get('/course/CourseNum={crse}')
async def get_course_number(crse: str):
    sampleQuery = list(collection.find({'Crse':crse},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return result


#Get Close courses
@student_api_route.get('/course/Closed')
async def get_closed():

    sampleQuery = list(collection.find({},{'_id':0}).limit(1000))
    test = []

    for index in sampleQuery:
        try:
            if index['Max'] == index['Curr']:
                test.append(index)
        except:
            continue

    count = len(test)


    result = {'Number of courses': count,'result': test}

    return result


#Get course by subject and section
@student_api_route.get('/course/Subj={subject}/Sect={section}')
async def get_course_subject_section(subject: str, section: str):
    sampleQuery = list(collection.find({'Subj':subject,'Sect':section},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return result


#Get course by building and room
@student_api_route.get('/course/Bldg={Bldg}/Room={Room}')
async def get_course_bldg_room(Bldg: str, Room: str):
    sampleQuery = list(collection.find({'Bldg':Bldg,'Room':Room},{'_id':0}).limit(1000))

    result = {'result': sampleQuery}

    return result

#Course POST Routes

@student_api_route.post("/addCourse/")
async def post_course(course: Course):
    _id = collection.insert_one(dict(course))
    sample = list(collection.find({"_id": _id.inserted_id},{'_id':0}))

    return {"status": "ok", "result": sample}

#Course PUT routes
@student_api_route.put("/putCourse/")
async def update_course(crn: str, update_course: Course):
    collection.find_one_and_update({"CRN": crn}, {
        "$set": dict(update_course)
    })
    update_query = courses_info(collection.find({"Crn": crn}))

    return {"result": update_query}



#Get test routes

# @student_api_route.get("/")
# async def get_data():
#     sample = todos_serializer(collection_test.find())

#     return {"status": "ok", "result": sample} 

# @student_api_route.get("/{id}")
# async def get_single_todo(id: str):
#     sample = todos_serializer(collection_test.find({"_id": ObjectId(id)}))
    
#     return {"status": "ok", "result": sample}

#Post test routes

# @student_api_route.post("/api/todo/")
# async def post_todo(todo: Todo):
#     _id = collection_test.insert_one(dict(todo))
#     sample = todos_serializer(collection_test.find({"_id": _id.inserted_id}))

#     return {"status": "ok", "result": sample}


# @student_api_route.delete("/api/todo/{name}")
# async def delete_todo(name):
#     sample_query = collection_test.delete_one({"name": name})
#     if sample_query:
#         return "Successfully Deleted todo"
#     raise HTTPException(404, f"There is not TOdo item with this name {name}")



#Get list of students information

@student_api_route.get("/student/")
async def get_list_of_student():
    student_query = students_info(collection_students.find())

    return {"data": student_query}

# Get Student information for single student

@student_api_route.get("/student/single/{id}")
async def single_student_id(id: str):
    student_query = students_info(collection_students.find({"_id": ObjectId(id)}))

    return {"data": student_query}

# Get Single student by name information

@student_api_route.get("/student/name/{name}")
async def student_by_name(name: str):
    student_query = students_info(collection_students.find({"first_name": name}))

    return {"data": student_query}

#Get single student by M#

@student_api_route.get("/student/number/{number}")
async def student_by_number(number: str):
    student_query = students_info(collection_students.find({"mnumber": number}))

    return {"data": student_query}

#Get student by gpa
@student_api_route.get("/student/gpa/{gpa}")
async def student_by_gpa(gpa: int):
    student_query = students_info(collection_students.find({"gpa": gpa}))

    return {"data": student_query}


#POST student route
@student_api_route.post("/student/", response_description="Student data added into the database")
async def add_new_student(student: Student_info):
    _id = collection_students.insert_one(dict(student))
    #insert_in = await collection_students.insert_one(student, {'_id':0})
    insert_query = students_info(collection_students.find({"_id": _id.inserted_id}))
    #new_student = await collection_students.find_one({"_id": insert_in.inserted_id})
    #insert_query = students_info(collection_students.find({"_id": _id.inserted_id}))


    return {"result": insert_query}

#PUT student route
@student_api_route.put("/{id}")
async def update_student(name:str, update_student: Student_info):
    collection_students.find_one_and_update({"first_name": name}, {
        "$set": dict(update_student)
    })
    update_query = students_info(collection_students.find({"first_name": id}))

    return {"result": update_query}


# ------------------------------------------
# Student Advising Form GET routes
@student_api_route.get("/forms/")
async def advising_forms_list():
    advising_query = advising_forms(collection_name.find())

    return advising_query

    #return {"List of Student": advising_query}

#Find by student
@student_api_route.get("/student_form/{student}")
async def single_student(student: str):
    advising_query = advising_forms(collection_name.find({"Student": student}))

    return {"status": "ok", "data": advising_query}

#Find by semester
@student_api_route.get("/semster/{semester}")
async def semester(semester: str):
    advising_query = advising_forms(collection_name.find({"Semester": semester}))

    return {"data": advising_query}


#Find by year
@student_api_route.get("/year/{year}")
async def year(year: int):
    advising_query = advising_forms(collection_name.find({"Year": year}))

    return {"data": advising_query}

# POST Advising form
@student_api_route.post("/advising_form/{id}")
async def add_advising_form(advising: Advising_form):
    _id = collection_name.insert_one(dict(advising))
    insert_query = advising_forms(collection_name.find({"_id": _id.inserted_id}))

    return  insert_query
