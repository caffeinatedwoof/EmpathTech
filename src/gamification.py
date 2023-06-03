import streamlit as st
import os
import sys
from PIL import Image
from datetime import datetime, timedelta
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from dbhandler import DBHandler

if "db" not in st.session_state:
    st.session_state.db = DBHandler()
else:
    db = st.session_state.db

WIDTH = 200
LVL_1_THRESHOLD = 1
LVL_2_THRESHOLD = 3
LVL_3_THRESHOLD = 8
LVL_4_THRESHOLD = 15

class journalPlant:
    def __init__(self, entries, plant="default"):
        self.level = self._calculate_lvl(entries)
        self.plant = plant

    def _calculate_lvl(self, entries):
        if entries >= LVL_4_THRESHOLD:
            return 4
        elif entries >= LVL_3_THRESHOLD:
            return 3
        elif entries >= LVL_2_THRESHOLD:
            return 2
        elif entries >= LVL_1_THRESHOLD:
            return 1
        else:
            return 0

    def get_level(self):
        return self.level

    def get_plant(self):
        return self.plant

    def set_level(self, level):
        self.level = level

    def set_plant(self, plant):
        self.plant = plant

    def show(self):
        current_plant = os.path.join(current, "images", f"plant{self.level}.png")
        image = Image.open(current_plant)
        st.image(image, width=WIDTH)
        

def count_journals(student_id):
    journals = db.get_journal_entries(student_id)
    journal_list = [journal for journal in journals if journal['private'] == False]
    return len(journal_list)

def count_recent_journals(student_id):
    # find date two weeks ago from today
    today = datetime.now()
    two_weeks_ago = today - timedelta(days=14)
    journals = db.get_journal_entries(student_id)
    journal_list = [journal for journal in journals if journal['private'] == False and journal['date'] > two_weeks_ago]
    return len(journal_list)


# misslim = db.teachers.find_one({"name": "Miss Lim"})
# teacher_id = misslim['_id']

# # get all students
# students = db.get_all_students(teacher_id)
# for student in students:
#     print(count_journals(student['_id']))