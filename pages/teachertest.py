import streamlit as st
import dbhandler
from login import connect_db

# db = connect_db()

# Initialize variables
teacher_id = st.session_state.role_id
teacher_name = st.session_state.user_fullname

@st.cache_data
def show_student_filter():
    return [student['name'] for student in db.get_all_students(teacher_id)]
    

db = st.session_state.db
print(db)
print(db.students)
print(type(st.session_state.role_id))

st.markdown(f"You have logged in! :) {teacher_name}")
students = db.students
student_list = show_student_filter()
selected_student = st.selectbox("Your students", student_list)
