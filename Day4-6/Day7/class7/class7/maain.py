from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from pydantic import ConfigDict
import uvicorn
from fastapi import FastAPI, Depends, HTTPException

# Database Connection
DATABASE_URL = "postgresql://user:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)

# One-to-Many Relationship: Author and Books
class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # One-to-Many relationship with Book
    books: List["Book"] = Relationship(back_populates="author")

class BookBase(SQLModel):
    title: str
    genre: str
    author_id: int = Field(default=None, foreign_key="author.id")

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationship back to Author
    author: Optional[Author] = Relationship(back_populates="books")






# Many-to-Many Relationship: Student and Courses
class CourseStudentLink(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, foreign_key="student.id",primary_key=True)
    course_id: Optional[int] = Field(default=None, foreign_key="course.id", primary_key=True )

class StudentBase(SQLModel):
    name: str
    email: str

class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Many-to-Many relationship with Course
    # Forward reference/forward declaration needed here because Course is not yet defined
    courses: List["Course"] = Relationship(back_populates="students", link_model=CourseStudentLink)

class CourseBase(SQLModel):
    name: str
    description: str

class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Many-to-Many relationship with Student
    # No forward reference/forward declaration needed because Student is already defined
    students: List[Student] = Relationship(back_populates="courses", link_model=CourseStudentLink)

# Pydantic models for input/output
class AuthorCreate(SQLModel):
    name: str

class BookCreate(SQLModel):
    title: str
    genre: str
    author_id: int

class StudentCreate(StudentBase):
    pass

class CourseCreate(CourseBase):
    pass

# FastAPI Application
app = FastAPI()

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session

# One-to-Many Endpoints
@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    # Validate that the author exists
    author = session.get(Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/authors/{author_id}/books")
def get_author_books(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books

# Many-to-Many Endpoints
@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.post("/courses/", response_model=Course)
def create_course(course: CourseCreate, session: Session = Depends(get_session)):
    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@app.post("/enroll")
def enroll_student_in_course(student_id: int, course_id: int, session: Session = Depends(get_session)):
    # Validate student and course exist
    student = session.get(Student, student_id)
    course = session.get(Course, course_id)
    
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    # Create link between student and course
    link = CourseStudentLink(student_id=student_id, course_id=course_id)
    session.add(link)
    session.commit()
    
    return {"message": "Enrollment successful"}

@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.courses

# Create database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Main entry point
if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)