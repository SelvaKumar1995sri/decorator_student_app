import uvicorn
import pymongo

from functools import wraps
from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi import FastAPI, Request
from pydantic import BaseModel

import sys

client = pymongo.MongoClient(
    "mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
my_db = client['mydatabase']
Student_collection = my_db['school_registry']

def get_collection():
    return Student_collection


app = FastAPI()

def token_required(f):
    def wrapper_auth(*args, **kwargs):
        token = Request.headers
        dec = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        if dec['name'] == "ramu" :
            return f(*args, **kwargs)
        else:
            return {'message' : 'Token is incorrect'}
    return wrapper_auth

def create_access_token(data: dict):
    to_encode = data.copy()
     
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 'SECRET_KEY', algorithm="HS256")
     
    return encoded_jwt

class Student(BaseModel):
    roll_no: int
    name: str
    age: int
    location: str

@app.get("/get_token")
async def get_token():
    
    data = Student_collection.find_one({"roll_no":1},{"_id":0})

    token = create_access_token(data=data)
    return {'token': token}

def student_serialize_list(student_list):
    return [student.dict() for student in student_list]

@app.get('/', tags=['student'])
def greetings():
    return "Welcome to Student registry type 'doc#s' in URL to switch swagger page"
    

@token_required
@app.get('/api/viewAllstudents', tags=['student'])
def view_all():
    try:
        output = list(Student_collection.find({},{"_id": 0}))
        if output == []:
            return "No Data exist to view"
        else:
            return {"data": output}

    except Exception as e:
        print("error on viewing data " + str(e))

@app.get('/api/viewstudentdetails/{roll_no}', tags=['student'])
def view_student(roll_no):
    try:
        output = Student_collection.find_one({"roll_no": int(roll_no)},{"_id": 0})
        print(output)
        if output == []:
            return "give a valid value to find"

        else:
            return {"status": "ok", "data": output}

    except Exception as e:
        print("error on viewing data " + str(e))

@token_required
@app.post('/api/addingNewStudent/', tags=['student'])
def add_student(student: Student):
    try:
        Student_collection.insert_one(student.dict())
        return "successfully added"
    except Exception as e:
        print("error on add data " + str(e))


@app.delete('/api/deleteStudentByRollno/{roll_no}', tags=['student'])
def delete_student(roll_no):
    try:
        output = Student_collection.find({"roll_no": int(roll_no)})
        if output == []:
            return "Give vaid roll_no from existing database"
        else:
            Student_collection.delete_one({"roll_no": int(roll_no)})
            return "deleted successfully"

    except Exception as e:
        print("error on viewing data " + str(e))


@app.put('/api/update/{roll_no}', tags=["student"])
def update_student(roll_no, student: Student):
    try:
        list_id = []
        for i in Student_collection.find():
            list_id.append(i["roll_no"])
        max_id = max(list_id)
        userip = dict(student)

        if max_id >= int(roll_no):
            Student_collection.update_one(
                {"roll_no": int(roll_no)}, {"$set": userip})
            return "Updated Successfully"

        else:
            return "Given value not valid ,choose from existing Data "

    except Exception as e:
        print("error on viewing data " + str(e))


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, access_log=False)