import os
import sys
# add classes to teachers and students
# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(parent_dir)

from dbhandler import DBHandler
db = DBHandler()
students, teachers, journals = db.students, db.teachers, db.journals
summaries = db.summaries

miss_lim = teachers.find_one({"name": "Miss Lim"})
students.update_many({"teacher_id": miss_lim["_id"]}, {"$set": {"class": "P1-1"}})

all_students = students.find({"teacher_id": miss_lim["_id"]})
for student in all_students:
    print(student)

teachers.update_one({"name": "Miss Lim"}, {"$set": {"class": "P1-1"}})
print(teachers.find_one({"name": "Miss Lim"}))