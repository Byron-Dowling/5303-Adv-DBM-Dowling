from typing import Optional
from pydantic import BaseModel


class Course(BaseModel):
    Col: Optional[str] = None
    Crn: Optional[str] = None
    Subj: Optional[str] = None
    Crse: Optional[str] = None
    Sect: Optional[str] = None
    Title:Optional[str] = None
    PrimaryInstructor:Optional[str] = None
    Max:Optional[int] = None
    Curr: Optional[int] = None
    Aval: Optional[str] = None
    Days: Optional[str] = None
    Begin:Optional[str] = None
    End: Optional[str] = None
    Bldg: Optional[str] = None
    Room: Optional[str] = None
    Year:Optional[int] = None
    Semester: Optional[str] = None

class Todo(BaseModel):
    name: str
    description:str
    #completed: bool

class Student_info(BaseModel):
    first_name: str
    last_name: str
    classification: str
    email: str
    gpa: int
    mnumber: str
    github: str


class Advising_form(BaseModel):
    Semester: str
    Year: int
    Student: str
    Courses: str
    Created: str
