from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import os
import streamlit as st
import certifi

CONNECT_STR = st.secrets.CONNECT_STR

# Create a DBHandler class
class DBHandler:
    def __init__(self):
        client = MongoClient(CONNECT_STR, 
                       tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)
        db = client['empathtech']
        self.students = db['students']
        self.teachers = db['teachers']
        self.journals = db['journals']
        self.summaries = db['j_summaries']
        self.auth = db['auth']
        self.chatlogs = db['chatlogs']

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


    def get_student(self, student_name=None, username=None):
        """ Returns a single student given the name or username

        Parameters
        ----------
        student_name : str
            username or name of the student

        Returns
        -------
        dict
            a student document
        """
        if student_name:
            student = self.students.find_one({"name": student_name})

        elif username:
            student_id = self.auth.find_one({"username": username})['student_id']
            student = self.students.find_one({"_id": student_id})
        
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


    def get_teacher(self, teacher_id):
        """ Returns a teacher given the teacher_name

        Parameters
        ----------
        teacher_id : str
            id of the teacher

        Returns
        -------
        dict
            a teacher document
        """
        teacher = self.teachers.find_one({"_id": teacher_id})
        return teacher
    

    def del_teacher(self, teacher_id):
        """ Deletes a teacher given the teacher_id

        Parameters
        ----------
        teacher_id : ObjectId
            _id of the teacher
        """
        self.teachers.find_one_and_delete({"_id": teacher_id})
        print("Teacher deleted")
        return None


    def insert_journal_entry(self, student_id, title, content, date):
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
            "comments": []
        }
        journal_id = self.journals.insert_one(new_entry).inserted_id
        return journal_id


    def update_journal_entry(self, journal_id, title, content):
        """ Updates a journal entry

        Parameters
        ----------
        journal_id : ObjectId
            _id of the journal entry
        title : str
            title of the journal entry
        content : str
            content of the journal entry

        Returns
        -------
        None
        """

        update_entry = {
            "title": title,
            "content": content
        }
        self.journals.update_one({"_id": journal_id}, {"$set": update_entry})
        return None


    def del_journal_entry(self, journal_id):
        """ Deletes a journal entry

        Parameters
        ----------
        journal_id : ObjectId
            _id of the journal entry
        """
        self.journals.delete_one({"_id": journal_id})
        return None


    def get_journal_entry(self, journal_id):
        """ Returns a journal entry given the journal_id

        Parameters
        ----------
        journal_id : ObjectId
            _id of the journal entry

        Returns
        -------
        dict
            a journal entry document
        """
        entry = self.journals.find_one({"_id": journal_id})
        return entry
    
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
        entries = self.journals.find({"student_id": student_id}).sort('date', pymongo.DESCENDING)
        return entries


    def get_all_teachers(self):
        """ Returns all the teachers in the collection

        Returns
        -------
        pymongo.cursor.Cursor
            list of all the teachers
        """
        return self.teachers.find({})


    def get_all_students(self, teacher_id):
        """ Returns all the students in the collection

        Returns
        -------
        pymongo.cursor.Cursor
            list of all the students
        """
        if teacher_id is None:
            return self.students.find({})
        else:
            return self.students.find({"teacher_id": teacher_id})
    
    
    def insert_summary(self, journal_id, summary):
        """_summary_

        Parameters
        ----------
        journal_id : ObjectId
            _description_
        is_genuine : dict
            dict containing keys "is_genuine" and "explanation"
        sentiment : dict 
            dict containing keys "score" and "explanation"
        events : dict
            dict containing keys "positive", "neutral", "negative", "concerning"
            with nested dicts containing keys "count" for number of sub-events and "list" for a list of sub-events

        Returns
        -------
        ObjectId
            _id of inserted summary
        """

        new_summary = {
            "sentiment" : summary['sentiment'],
            "events" : summary['events'],
            "journal_id" : journal_id,
            "student_id" : self.journals.find_one({"_id": journal_id})["student_id"]
        }

        summary_id = self.summaries.insert_one(new_summary).inserted_id
        return summary_id


    def get_summary(self, journal_id):
        """ Given a journal_id, gets the summary / sentiment analysis

        Parameters
        ----------
        journal_id : ObjectId
            ObjectId of the journal entry

        Returns
        -------
        dict
            dict containing the summary
        """

        summary = self.summaries.find_one({"journal_id": journal_id})
        return summary
    

    def get_all_summaries(self, student_id):
        """ Returns all the summaries for a student

        Parameters
        ----------
        student_id : ObjectId
            ObjectId of the student
        """

        summaries = self.summaries.find({"student_id": student_id})
        return summaries

    def insert_user(self, username, password, role, role_id):
        """
        Inserts a user into the database

        Parameters
        ----------
        username : str
            login username
        password : str
            user password
        role : str
            'student' or 'teacher'
        role_id : ObjectId
            Optional ObjectId of the student or teacher. If not provided, a new teacher / student will be created in the appropriate collection
        """
        if role == "student":
            new_student = {
                "username": username,
                "password": password,
                "role": role,
                "student_id": role_id
            }
            self.auth.insert_one(new_student)

        elif role == "teacher":
            new_teacher = {
                "username": username,
                "password": password,
                "role": role,
                "teacher_id": role_id
            }
            self.auth.insert_one(new_teacher)
        
        print(f"{role} User, '{username}' inserted")
        return None

    
    def insert_chatlog(self, chatlog):
        new_chatlog = {
            "start_time": chatlog['start_time'],
            "end_time": chatlog["end_time"],
            "student_id": chatlog["student_id"],
            "journal_id": chatlog["journal_id"],
            "messages": chatlog["messages"]
        }
        chatlog_id = self.chatlogs.insert_one(new_chatlog).inserted_id

        print("Chatlog inserted")
        return chatlog_id


    def update_chatlog(self, chatlog_id, chatlog):
        update_chatlog = { 
            "end_time": chatlog["end_time"],
            "journal_id": chatlog["journal_id"],
            "messages": chatlog["messages"]
        }

        self.chatlogs.update_one({"_id": chatlog_id}, {"$set": update_chatlog})
        print("Chatlog updated")
        return None
    
 
    def get_all_chatlogs(self, student_id):
        return self.chatlogs.find({"student_id": student_id}).sort('start_time', pymongo.DESCENDING)
    
 
    def get_chatlog(self, chatlog_id):
        return self.chatlogs.find_one({"_id": chatlog_id})