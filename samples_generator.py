from dbhandler import connect_to_db, choose_collections
import os
import json

def create_sample_students():
    """ Generate sample students """
    with open("student_names.txt", "r") as student_names:
        lines = student_names.readlines()
        student_names = [line.strip() for line in lines]
        print(student_names)

    db = connect_to_db()
    students, teachers, journals = choose_collections(db)

    teacher = get_teacher("Miss Lim")

    for name in student_names:
        insert_student(name, teacher["_id"])


def create_sample_journals():
    """ Generate sample journals """

    def load_entries(json_path):
        """ return jouranl entries from json file """
        entries = json.load(open(json_path))
        return entries['entries']

    # load all json files in journals/
    folder_path = os.path.join(os.getcwd(), 'journals')
    journal_filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    db = connect_to_db()
    students, teachers, journals = choose_collections(db)
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
