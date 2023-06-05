import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from st_helper_func import remove_top_space_canvas, navbar_edit, post_navbar_edit, hide_student_pages, error_page_redirect, connect_db, hide_streamlit_footer, hide_other_pages, show_privacy_data_protection_footer
from streamlit_extras.switch_page_button import switch_page
from src.sidebar import render_sidebar

# Layout config 
st.set_page_config(
    # layout = "wide",
    initial_sidebar_state = 'expanded'
)

if 'user_fullname' not in st.session_state:
    error_page_redirect()

remove_top_space_canvas()
hide_student_pages()
hide_other_pages()
navbar_edit()
hide_streamlit_footer()
render_sidebar()

# st.session_state.update(st.session_state)

def SetColor(df):
    """Function that sets color in a color list based on dataframe's Sentiment column

    Args:
        df (pd.Dataframe): Dataframe

    Returns:
        list: List of color
    """
    values = df['Sentiment'].tolist()
    color_list = []
    for i in values:
        if(i == 1):
            color_list.append("orange")
        elif(i == 0):
            color_list.append("red")
        elif(i == 2):
            color_list.append("green")

    return color_list

@st.cache_data
def show_student_filter():
    return [student for student in db.get_all_students(teacher_id)]

if 'user_fullname' not in st.session_state:
    error_page_redirect()

if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()
    post_navbar_edit(st.session_state.user_fullname)

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
        
        # Create a selectbox using dict values containing student full name
        selected_student_name = st.selectbox("Student name",\
                                              student_names_id_dict.values())
        st.session_state.current_student_name = selected_student_name


    key_list = list(student_names_id_dict.keys())
    value_list = list(student_names_id_dict.values())

    # Get its id for journal entry search
    selected_student_id = value_list.index(selected_student_name)

    #Iterator cursor output
    entries = db.get_journal_entries(key_list[selected_student_id])
    
    # Pymongo has sorted order
    entries_list = [i for i in entries]
    
    ####
    #Emotion history
    ####
    st.subheader("Emotion history")
    emotion_list = ['Positive', 'Neutral', 'Negative']
    sent_dict = dict(zip([2, 1, 0], emotion_list))

    # Reverse order to plot
    time_periods = [entry['date'] for entry in entries_list]


    sentiment_list = []
    for entry in entries_list:
        sentiment = db.get_summary(entry['_id'])['sentiment']['score']
        sentiment_list.append(sentiment)
        #sentiment_list.append(sent_dict[sentiment])
    
    # emotions = [random.choice(emotion_list) for _ in time_periods]

    df = pd.DataFrame(zip(time_periods, sentiment_list), 
                     columns = ['Time', 'Sentiment'])
    
    fig = px.scatter(df,
                     x='Time', 
                     y='Sentiment',
                     color='Sentiment',
                     )
    
    fig.update_layout(xaxis_title='Time',
                      yaxis_title=None,
                      yaxis_range=[-0.5,2.5],
                      yaxis = dict(tickmode = 'array', tickvals = [0, 1, 2],
                                ticktext = emotion_list[::-1])
    )
    

    # Remove color scale, Set marker size
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(marker=dict(size=15, color=SetColor(df)) )
    st.plotly_chart(fig, use_container_width=True)

    ####
    #Journal entries
    ####
    st.subheader(f"Journal entries by {selected_student_name}")

    counter = 0
    public_entries = [entry for entry in entries_list if entry['private'] == False]
    for entry in public_entries:
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

            # Converted sentiment from value to string
            sentiment = sent_dict[db.get_summary(entry['_id'])['sentiment']['score']]
            st.markdown(f"<div align='center'>{sentiment}</div>", unsafe_allow_html=True)
        with subcol4:
            if counter == 0:
                st.markdown("**Action**")
            if st.button("View full entry", key=f"{entry['_id']}_btn"):
                chatlog = db.chatlogs.find_one({"journal_id": entry['_id']})
                st.session_state.chatlog_id = chatlog['_id']
                st.session_state.current_student_name = selected_student_name

                # Switch page after click button
                switch_page("View_Journal")
        st.markdown("----")
        counter += 1
       
else:
    error_page_redirect()