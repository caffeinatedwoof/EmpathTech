import streamlit as st
import numpy as np
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

def highlight_max(cell):
    """Function that highlights cells which are positive via css properties

    Args:
        cell (pd.dataframe cell): Cell of interest

    Returns:
        None.
    """
    if type(cell) != str and cell > 0 :
        return 'background-color: red; color:white'
    else:
        return 'background-color: transparent; color: white'
    return None

if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    st.title("Emotion dashboard summary of your students based on journal entries - Number of instances")
 
    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname
    teaching_class = st.session_state.teaching_class

    students = db.students
    student_list = show_student_filter()

    col1, padding1, padding2 = st.columns(3)
    
    # Drop down selector
    with col1:
        student_class = set([student['class'] for student in student_list])
        selected_class = st.selectbox("Class", student_class)

    with padding1:
        pass

    with padding2:
        pass    

    # Apply filter after extracting all student based on class selection
    student_names_id_dict = {student['name']: {} \
                             for student in student_list\
                             if student['class']==selected_class}
    
    emotion_list = ['Positive', 'Neutral', 'Negative', 'Concerning']

    # To get all j_summaries via a student_id and subsequently map
    for student in student_list:
        if student['class']==selected_class:
            # Gets cursor object (iterator)
            journal_summaries = [summary for summary in\
                                  db.get_all_summaries(student['_id'])]
            #st.write(journal_summaries)
            # Start with all 0 for 3 state of emotion and concerning = 0
            positive, neutral, negative, concerning = 0,0,0,0


            # Sum all values of the 3 emotions across journals
            for j_summary in journal_summaries:
                positive += int(j_summary['events']['positive']['count'])
                neutral += int(j_summary['events']['neutral']['count'])
                negative += int(j_summary['events']['negative']['count'])
                concerning += int(j_summary['events']['concerning']['count'])

            # Update values to dictionary prior to display in dataframe
            student_names_id_dict[student['name']]['Positive'] = positive
            student_names_id_dict[student['name']]['Neutral'] = neutral
            student_names_id_dict[student['name']]['Negative'] = negative
            student_names_id_dict[student['name']]['Concerning'] = concerning
    
    # Construct dataframe for display
    df = pd.DataFrame(student_names_id_dict).T
    df = df.reset_index().rename(columns = {'index':'Student Name'})

    # Shift index to start from 1
    df.index = df.index + 1
    #hide_st_table_row_index()
    #df.style.apply(lambda x: ['background-color: lightgreen']*len(df)\
    #                    if (x.name == 'Positive') \
    #                        else (['background-color: grey']*len(df) if (x.name == 'Negative') else 'background-color: red'*len(df), axis = 0))

    # Rowwise highlight
    st.dataframe(df.style.applymap(highlight_max,
        subset=['Concerning']),
        use_container_width=True)
else:
    error_page_redirect()