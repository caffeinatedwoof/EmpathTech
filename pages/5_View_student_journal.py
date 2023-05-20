import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_student_pages, error_page_redirect, connect_db
#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)

remove_top_space_canvas()
navbar_edit()
hide_student_pages()

st.session_state.update(st.session_state)
#Temporary hack
#st.session_state.logged_in = True

if 'logged_in' in st.session_state and st.session_state.logged_in:

    st.title("View Student Journal")

    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname

    @st.cache_data
    def show_student_filter():
        return [student for student in db.get_all_students(teacher_id)]

    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    students = db.students
    student_list = show_student_filter()
    student_names = [student['name'] for student in student_list]
    selected_student_name = st.selectbox("Your students", student_names)

    for student in student_list:
        if student['name'] == selected_student_name:
            selected_student = student
            st.session_state.selected_student = selected_student
            break

else:
    error_page_redirect()