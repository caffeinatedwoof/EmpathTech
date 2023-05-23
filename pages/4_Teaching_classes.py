import streamlit as st
import pandas as pd
from st_helper_func import remove_top_space_canvas, navbar_edit, post_navbar_edit, hide_student_pages, error_page_redirect, connect_db, hide_st_table_row_index
#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)

st.session_state.update(st.session_state)

remove_top_space_canvas()
#navbar_edit
post_navbar_edit(st.session_state.user_fullname)
hide_student_pages()

@st.cache_data
def show_student_filter():
    return [student for student in db.get_all_students(teacher_id)]

#Temporary hack
#st.session_state.logged_in = True

if 'logged_in' in st.session_state and st.session_state.logged_in:
    # Initialize variables from sessions
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname
    teaching_class = st.session_state.teaching_class

    st.title(f"Hi {teacher_name}, Teaching classes for this year")

    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    students = db.students
    student_list = show_student_filter()

    total_students = len(student_list)
    year_head = 'Pending information'
    role = 'Form teacher'
    subject = 'English'

    # Put info into dictionary
    teaching_info_dict = {
        'Class taught': [teaching_class],
        'Role': [role],
        'Year Head': [year_head],
        'Subject': [subject],
        'Total Students': [len(student_list)]
    }

    df = pd.DataFrame(teaching_info_dict)

    hide_st_table_row_index()
    st.table(df)

else:
    error_page_redirect()