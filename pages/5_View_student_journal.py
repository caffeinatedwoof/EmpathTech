import streamlit as st
import random
import plotly.express as px
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

@st.cache_data
def show_student_filter():
    return [student for student in db.get_all_students(teacher_id)]


if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    st.title("Student Journal View")

    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname
    teaching_class = st.session_state.teaching_class
    
    students = db.students
    student_list = show_student_filter()

    col1, padding, col2 = st.columns((10,2,10))
    with col1:
        student_class = set([student['class'] for student in student_list])
        selected_class = st.selectbox("Class", student_class)

    with col2:
        # Apply filter after extracting all student based on class selection
        student_names_id_dict = {student['_id']: student['name']\
                            for student in student_list\
                            if student['class']==selected_class}
        
        selected_student_name = st.selectbox("Student name", student_names_id_dict.values())

    key_list = list(student_names_id_dict.keys())
    value_list = list(student_names_id_dict.values())

    # Get its id for journal entry search
    selected_student_id = value_list.index(selected_student_name)

    #Iterator cursor output
    entries = db.get_journal_entries(key_list[selected_student_id])
    
    # Consolidate results and reverse their order. Not needed if we can use pymongo to sort based on dates itself
    entries_list = [i for i in entries][::-1]
    
    ####
    #Emotion history
    ####
    st.subheader("Emotion history")
    emotion_list = ['Positive', 'Neutral', 'Negative']
    time_periods = [entry['date'] for entry in entries_list[::-1]]
    emotions = [random.choice(emotion_list) for _ in time_periods]

    fig = px.scatter(x=time_periods, y=emotions)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

    ####
    #Journal entries
    ####
    st.subheader(f"Journal entries by {selected_student_name}")
    # Iterate cursor
    for entry in entries_list:
        subcol1, subcol2, subcol3= st.columns([3,1,1])
        with subcol1:
            st.markdown(f"{entry['title']}")
            st.markdown(f"{entry['content']}")

        with subcol2:   
            st.markdown(f"Date submitted") 
            st.markdown(f"**{entry['date']}**")

        with subcol3:
            st.markdown("Sentiment")
            st.markdown("TBC")
        st.markdown("----")
 

else:
    error_page_redirect()