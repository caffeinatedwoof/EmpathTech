import streamlit as st
from dbhandler import DBHandler
import semantic_search as ss
from bson.objectid import ObjectId

def get_student_names():
    db_handler = DBHandler()
    students = db_handler.get_all_students(teacher_id = ObjectId('645c899105bbb927a7f09a1d'))  # Assuming you have a method to retrieve all students
    return [student['name'] for student in students]

def app():
    # Fetch student names for the dropdown
    student_names = get_student_names()

    # Create dropdown for student names
    student_name = st.selectbox('Select a Student', student_names)
    
    # Create date input for start and end date
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')

    # Create text input for the query
    question = st.text_input('Your Query')

    # If the query is not empty, process it
    if st.button('Submit'):
        if question:
            st.write('Processing your query...')
            result = main(student_name, start_date, end_date, question)
            st.write('Answer:', result['answer'])
            for i, entry in enumerate(result['source_documents']):
                st.write(f'Journal Entry {i+1}')
                st.write(f'Date:', result['source_documents'][i].metadata['journal_date'].split(' ')[0])
                st.write(f'Journal Prompt:', result['source_documents'][i].metadata['journal_title'])
                st.write(f'Journal Entry:', result['source_documents'][i].page_content)
        else:
            st.write('Please enter a query.')
    
def main(student_name, start_date, end_date, question):
    journal_entries, metadatas = ss.filter_journal_entries(student_name, start_date, end_date)
    vector_store = ss.convert_journal_entries_to_vectors(journal_entries, metadatas)
    return ss.process_query(question, vector_store, student_name)

# Run the app
if __name__ == "__main__":
    app()