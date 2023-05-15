import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_student_pages
#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)

remove_top_space_canvas()
navbar_edit()

st.session_state.update(st.session_state)

if "logged_in" not in st.session_state:
    "Please return to home page and wait for page to load"

elif not st.session_state.logged_in:
    "You are not logged in"

elif st.session_state.logged_in:
    st.title("Teacher Dashboard")

    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname

    @st.cache_data
    def show_student_filter():
        return [student for student in db.get_all_students(teacher_id)]

    db = st.session_state.db

    st.markdown(f"You have logged in! :) {teacher_name}")
    students = db.students
    student_list = show_student_filter()
    student_names = [student['name'] for student in student_list]
    selected_student_name = st.selectbox("Your students", student_names)

    for student in student_list:
        if student['name'] == selected_student_name:
            selected_student = student
            st.session_state.selected_student = selected_student
            break