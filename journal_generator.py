# Generates journal entries given a list of personas and prompts

import json

with open('student_personas.json') as f:
    students_json = json.load(f)
    student_list = students_json['students']

    total_entries = 0
    for student in student_list:
        total_entries += int(student['journalEntries'])

    print(total_entries)