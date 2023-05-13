from dbhandler import DBHandler
import os
import json

db = DBHandler()
students, teachers, journals = db.students, db.teachers, db.journals

def create_sample_students():
    """ Generate sample students """
    with open("student_names.txt", "r") as student_names:
        lines = student_names.readlines()
        student_names = [line.strip() for line in lines]
        print(student_names)

    teacher = db.get_teacher("Miss Lim")

    for name in student_names:
        db.insert_student(name, teacher["_id"])


def create_sample_journals():
    """ Generate sample journals """

    def load_entries(json_path):
        """ return jouranl entries from json file """
        entries = json.load(open(json_path))
        return entries['entries']

    # load all json files in journals/
    folder_path = os.path.join(os.getcwd(), 'journals')
    journal_filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    journal_index = 0

    for student in students.find():
        journal_path = os.path.join(folder_path, journal_filenames[journal_index])
        all_entries = load_entries(journal_path)
        for entry in all_entries:
            content = entry['entry']
            title = entry['title']
            date = entry['entry_date']

            new_entry = {
                "title": title,
                "content": content,
                "date": date,
                "student_id": student['_id'],
            }
            journals.insert_one(new_entry)

        journal_index += 1
        

def load_journal_entries(filepath):
    entries = json.load(open(filepath))['entries']
    for entry in entries:
        print("Title: " + entry['title'])
        print("Content: " + entry['entry'])
        print("Date: " + entry['entry_date'])


def generate_users():
    """ Generate sample users """
    teachers = db.get_all_teachers()
    students = db.get_all_students()

    # for teacher in teachers:
    #     teacher_name = teacher['name'].lower().replace(" ", "")
    #     db.insert_user(username=teacher_name, password="password", role="teacher", role_id=teacher['_id'])

    for student in students:
        student_name = student['name'].lower().replace(" ", "")
        db.insert_user(username=student_name, password="password", role="student", role_id=student['_id'])    