import streamlit as st
import random
import pandas as pd
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_student_pages,  error_page_redirect, connect_db, hide_st_table_row_index
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

    
@st.cache_data
def show_student_filter():
    return [student for student in db.get_all_students(teacher_id)]


# Function to highlight using different colours for positive/neutral/negative based on the max value amongst these 3.
def highlight_sentiments():
    """_summary_

    Args:
        row (pd.series): Panda series of interest

    Returns:
        str: css string indicating highlight color
    """

    return ['background-color: green;',
            'background-color: grey;',
            'background-color: red;']


if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    st.title("Emotion dashboard summary of your students")

    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname
    teaching_class = st.session_state.teaching_class

    students = db.students
    student_list = show_student_filter()

    col1, padding, padding = st.columns(3)
    
    with col1:
        student_class = set([student['class'] for student in student_list])
        selected_class = st.selectbox("Class", student_class)


    # Apply filter after extracting all student based on class selection
    student_names_id_dict = {str(student['_id']): {'Student name': student['name']}\
                        for student in student_list\
                        if student['class']==selected_class}
    
    emotion_list = ['Positive', 'Neutral', 'Negative', 'Sentiment Value']

    # Arbitrary set positive, neutral, negative emotions count. Removed when we have actual values from sentiment analysis count
    for key in student_names_id_dict:
        for emotion in emotion_list:
            if emotion!='Sentiment Value':
                student_names_id_dict[key][emotion] = random.randint(1, 10)
            else:
                student_names_id_dict[key][emotion] = random.random()

    
    # Construct dataframe for display
    df = pd.DataFrame(student_names_id_dict).T
    df = df.reset_index().drop('index', axis=1)
    # Shift index to start from 1
    df.index = df.index + 1
    #hide_st_table_row_index()


    # Rowwise highlight
    st.dataframe(df.style\
                .highlight_max(subset=['Positive','Neutral','Negative'], axis=1),
                use_container_width=True)
else:
    error_page_redirect()