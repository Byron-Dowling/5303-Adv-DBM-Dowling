
#Courses schema
def key_exist(course, keys=[]):
    for key in keys:
        if not key in course:
            return False
    return True

def filter_course(course) -> dict:
    print(list(course))
    d = {}
    d["Col"] = course.get("Col", None)
    d["Col"] = course.get("Col",None)
    d["Crn"] = course.get("Crn",None)
    d["Subj"] = course.get("Subj",None)
    d["Crse"] = course.get("Crse",None)
    d["Sect"] = course.get("Sect",None)
    d["Title"] = course.get("Title",None)
    d["PrimaryInstructor"] = course.get("PrimaryInstructor",None)
    d["Max"] = course.get("Max",None)
    d["Curr"] =course.get("Curr",None)
    d["Aval"] =course.get("Aval",None)
    d["Days"] = course.get("Days",None)
    d["Begin"] = course.get("Begin",None)
    d["End"] = course.get("End",None)
    d["Bldg"] = course.get("Bldg",None)
    d["Room"] = course.get("Room",None)
    d["Year"] = course.get("Year",None)
    d["Semester"] = course.get("Semester",None)

    return d
    #
    

def courses_info(courses) -> list:
    # if course_info(course="Aval") not in course_info:
       # print("Aval missing")

    return [filter_course(course) for course in courses]

#Test schema for learning

def todo_serializer(todo) -> dict:
    return {
        #"id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        #"completed": todo["completed"]
    }

def todos_serializer(todos) -> list:
    return [todo_serializer(todo) for todo in todos]


#Student information Schema

def student_info(form) -> dict:
    return{
        # "id": str(form["_id"]),
        "first_name": form["first_name"],
        "last_name": form["last_name"],
        "classification": form["classification"],
        "email": form["email"],
        "gpa": form["gpa"],
        "mnumber": form["mnumber"],
        "github": form["github"]
    }

def students_info(forms) -> list:
    return [student_info(form) for form in forms]



# Advising Form schema

def advising_form(stuff) -> dict:
    return{
        "id": str(stuff["_id"]),
        "Semester": stuff["Semester"],
        "Year": stuff["Year"],
        "Student": stuff["Student"],
        "Courses": stuff["Courses"],
        "Created": stuff["Created"]
    }

def advising_forms(stuffs) -> list:
    return[ advising_form(stuff) for stuff in stuffs]
