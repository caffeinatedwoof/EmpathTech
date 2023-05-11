from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv("conf/.env")

MONGODB_PW = os.getenv("MONGODB_PW")

# Create a DBHandler class
class DBHandler:
    def __init__(self):
        client = MongoClient(f'mongodb+srv://empathtech:{MONGODB_PW}@cluster0.it4z2ov.mongodb.net/?retryWrites=true&w=majority')
        db = client['empathtech']
        self.students = db['students']
        self.teachers = db['teachers']
        self.journals = db['journals']

    def insert_student(self, student_name, teacher_id):
        """ Insert a new student into the database give

        Parameters
        ----------
        student_name : str
            name of the student
        teacher_id : ObjectId
            _id of the teacher

        Returns
        -------
        ObjectId
            _id of the student
        """
        new_student = {
            "name": student_name,
            "teacher_id": teacher_id,
        }
        student_id = self.students.insert_one(new_student).inserted_id
        return student_id


    def get_student(self, student_name):
        """ Returns a single student given the name

        Parameters
        ----------
        student_name : str
            name of the student

        Returns
        -------
        dict
            a student document
        """
        student = self.students.find_one({"name": student_name})
        return student
    

    def insert_teacher(self, teacher_name):
        """ Inserts a teacher given the teacher_name

        Parameters
        ----------
        teacher_name : str
            name of the teacher

        Returns
        -------
        ObjectId
            _id of the teacher
        """
        new_teacher = {
            "name": teacher_name,
        }
        teacher_id = self.teachers.insert_one(new_teacher).inserted_id
        return teacher_id


    def get_teacher(self, teacher_name):
        """ Returns a teacher given the teacher_name

        Parameters
        ----------
        teacher_name : str
            name of the teacher

        Returns
        -------
        dict
            a teacher document
        """
        teacher = self.teachers.find_one({"name": teacher_name})
        return teacher
    

    def insert_journal(self, student_id, title, content, date):
        """
        Inserts a journal entry for a student

        Parameters
        ----------
        student_id : ObjectId
            _id of the student
        title : str
            title of the journal entry
        content : str
            content of the journal entry
        date : datetime
            datetime object containing the date/time of entry creation

        Returns
        -------
        ObjectId
            _id of the journal entry
        """
        new_entry = {
            "title": title,
            "content": content,
            "date": date,
            "student_id": student_id,
        }
        journal_id = self.journals.insert_one(new_entry).inserted_id
        return journal_id


    def get_journal_entries(self, student_id):
        """ Return all journal entries for a student given the student_id

        Parameters
        ----------
        student_id : ObjectId
            _id of the student

        Returns
        -------
        pymongo.cursor.Cursor
            a list of all the journal entries of the student
        """
        entries = self.journals.find({"student_id": student_id})
        return entries


db = DBHandler()
my_student = db.get_student("Jun Hao Ng")
entries = db.get_journal_entries(my_student["_id"])
print("type of entries is ", type(entries))
for entry in entries:
    print(entry['date'], entry["title"])
    print(entry["content"])
    print(type(my_student))