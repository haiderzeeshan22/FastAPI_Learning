from sqlmodel import SQLModel , Field, Relationship
from typing import Optional, List


class StudentCourselink(SQLModel, table=True):
    student_id : Optional[int] = Field(default=None, foreign_key="student.id", primary_key=True)
    course_id  : Optional[int] = Field(default=None, foreign_key="course.id", primary_key=True)

class Student(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    email : str
    # course_id  : Optional[int] = Field(default=None, foreign_key="course.id")    
    courses : List["Course"] = Relationship(back_populates="students", link_model=StudentCourselink)



class Course(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    Course_name : str
    description : str
    # student_id : Optional[int] = Field(default=None, foreign_key="student.id")

    students : Optional[Student] = Relationship(back_populates="courses", link_model=StudentCourselink)




