from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    email: str


class StudentCreate(BaseModel):
    name: str
    email: str


student_list: List[Student] = [
    Student(id=0, name="Victor", email="victor@gmail.com"),
    Student(id=1, name="Gilmar", email="gilmar@gmail.com"),
]
id_counter = student_list[-1].id


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/alunos/", status_code=201, response_model=Student)
async def create_student(student: StudentCreate):
    global id_counter
    id_counter += 1
    new_student = Student(id=id_counter, name=student.name, email=student.email)
    student_list.append(new_student)
    return new_student


@app.get("/alunos/", response_model=List[Student])
async def read_students():
    return student_list


@app.get("/alunos/{student_id}", response_model=Student)
async def read_students_by_id(student_id: int):
    for student in student_list:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
