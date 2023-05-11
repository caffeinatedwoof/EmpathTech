from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv("conf/.env")

MONGODB_PW = os.getenv("MONGODB_PW")

def connect_to_db():
    # Create a connection
    client = MongoClient(f'mongodb+srv://empathtech:{MONGODB_PW}@cluster0.it4z2ov.mongodb.net/?retryWrites=true&w=majority')
    db = client['empathtech']
    return db

def choose_collections(db):
    # Choose the collections
    students = db['students']
    teachers = db['teachers']
    journals = db['journals']

    return students, teachers, journals

def insert_student(student_name, teacher_id):
    new_student = {
        "name": student_name,
        "teacher_id": teacher_id,
    }
    student_id = students.insert_one(new_student).inserted_id
    return student_id

def get_student(student_name):
    student = students.find_one({"name": student_name})
    return student
# Insert a new teacher
def insert_teacher(teacher_name):
    new_teacher = {
        "name": teacher_name,
    }
    teacher_id = teachers.insert_one(new_teacher).inserted_id
    return teacher_id

def get_teacher(teacher_name):
    teacher = teachers.find_one({"name": teacher_name})
    return teacher

def update_teacher_name():
    myquery = { "address": "Valley 345" }
    newvalues = { "$set": { "address": "Canyon 123" } }
    

def insert_journal(student_id, title, content, date):
    
    """ Insert a new journal entry """
    new_entry = {
        "title": title,
        "content": content,
        "date": date,
        "student_id": student_id,
    }
    journal_id = journals.insert_one(new_entry).inserted_id
    return journal_id


def get_journal_entries(student_id):
    """ Return all journal entries for a student """
    entries = journals.find({"student_id": student_id})
    return entries

students, teachers, journals = choose_collections(connect_to_db())

my_student = get_student("Jun Hao Ng")
entries = get_journal_entries(my_student["_id"])
for entry in entries:
    print(entry['date'], entry["title"])
    print(entry["content"])
    