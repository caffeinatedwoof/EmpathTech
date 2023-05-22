import streamlit as st
import random
import plotly.express as px
from datetime import datetime
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_student_pages, error_page_redirect, connect_db
from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    # layout = "wide",
    initial_sidebar_state = 'expanded'
)

remove_top_space_canvas()
navbar_edit()
hide_student_pages()

# st.session_state.update(st.session_state)
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
        st.session_state.current_student_name = selected_student_name
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
    sent_dict = dict(zip([2, 1, 0],emotion_list))
    time_periods = [entry['date'] for entry in entries_list[::-1]]
    sentiment_list = []
    for entry in entries_list:
        sentiment = db.get_summary(entry['_id'])['sentiment']['score']
        sentiment_list.append(sent_dict[sentiment])
    
    # emotions = [random.choice(emotion_list) for _ in time_periods]

    fig = px.scatter(x=time_periods, y=sentiment_list)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

    ####
    #Journal entries
    ####
    st.subheader(f"Journal entries by {selected_student_name}")
    # Iterate cursor
    counter = 0
    for entry in entries_list:
        subcol1, subcol2, subcol3, subcol4= st.columns([0.5,2,0.5,0.8])
        with subcol1:
            if counter == 0:
                st.markdown("**Date**")
            # format entry datetime to dd/mm/yyyy
            entry_date = datetime.strftime(entry['date'], "%d/%m/%Y")
            st.markdown(f"{entry_date}")
        with subcol2:
            if counter == 0:
                st.markdown("**Entry**")
            content = entry['content']
            content = content[:100] + "..." if len(content) > 100 else content
            st.markdown(f"{content}")
        with subcol3:
            if counter == 0:
                st.markdown("**Emotion**")
            sentiment = db.get_summary(entry['_id'])['sentiment']['score']
            st.markdown(f"<div align='center'>{sentiment}</div>", unsafe_allow_html=True)
        with subcol4:
            if counter == 0:
                st.markdown("**Action**")
            if st.button("View full entry", key=f"{entry['_id']}_btn"):
                chatlog = db.chatlogs.find_one({"journal_id": entry['_id']})
                st.session_state.chatlog_id = chatlog['_id']
                st.session_state.current_student_name = selected_student_name
                switch_page("View Journal")
        st.markdown("----")
        counter += 1

else:
    error_page_redirect()