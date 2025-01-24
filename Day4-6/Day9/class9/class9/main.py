from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_table, get_session
from models import StudentCourselink, Student, Course


app : FastAPI = FastAPI()

@app.on_event("startup")
def create_table():
    create_db_and_table()


@app.post("/students", response_model=Student)
def create_student(student:Student, session:Session= Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.post("/courses", response_model=Course)
def create_course(course:Course, session:Session=Depends(get_session)):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@app.post("/enroll")
def create_link(studen_id:int, course_id:int, session:Session=Depends(get_session)):
    student = session.get(Student, studen_id)
    course = session.get(Student, course_id)

    if not student and not course:
        raise HTTPException(status_code=404, detail= "no student and course found")
    link = StudentCourselink(student_id=studen_id, course_id=course_id)
    session.add(link)
    session.commit()
    return {
        "message":"student  enrolled in course successfully"
    }

