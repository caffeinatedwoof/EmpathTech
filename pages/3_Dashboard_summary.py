import streamlit as st
import pandas as pd
from st_helper_func import remove_top_space_canvas, navbar_edit, post_navbar_edit, hide_student_pages, error_page_redirect, connect_db, hide_streamlit_footer, hide_other_pages, show_privacy_data_protection_footer
from src.sidebar import render_sidebar
import semantic_search as ss
#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)

if 'user_fullname' not in st.session_state:
    error_page_redirect()

remove_top_space_canvas()
navbar_edit()
hide_student_pages()
hide_other_pages()
hide_streamlit_footer()

def ss_query(student_name, start_date, end_date, question):
    journal_entries, metadatas = ss.filter_journal_entries(student_name, start_date, end_date)
    vector_store = ss.convert_journal_entries_to_vectors(journal_entries, metadatas)
    return ss.process_query(question, vector_store, student_name)


@st.cache_data
def show_student_filter():
    return [student for student in db.get_all_students(teacher_id)]


def highlight_max(cell):
    """Function that highlights cells which are positive via css properties

    Args:
        cell (pd.dataframe cell): Cell of interest

    Returns:
        string: css properties
    """
    if type(cell) != str and cell > 0 :
        return 'background-color: #A30000; color:white'
    else:
        return 'background-color: transparent; color: white'


if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

    post_navbar_edit(st.session_state.user_fullname)
    st.title("Emotion Dashboard")
    st.markdown("The numbers below show events that are recorded in each student's journal.")
 
    # Initialize variables
    teacher_id = st.session_state.role_id
    teacher_name = st.session_state.user_fullname
    teaching_class = st.session_state.teaching_class
    render_sidebar()
    
    student_list = show_student_filter()

    col1, col2 = st.columns(2)
    
    # Drop down selector
    with col1:
        student_class = set([student['class'] for student in student_list])
        selected_class = st.selectbox("Class", student_class)
 
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

        # Rowwise highlight
        st.dataframe(df.style.applymap(highlight_max,
            subset=['Concerning']),
            use_container_width=True)
        
    # Semantic search via expander
    with col2:
        with st.expander("Click here for Smart Search!"):
            st.markdown("""Select a student, date range, and ask a question about your student's journal entries. 
                        E.g. *how is my student doing recently?*
                        """)
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                selected_student_name = st.selectbox("Student name",
                                                      student_names_id_dict.keys())

            with s_col2:
                # Create date input for start and end date
                start_date = st.date_input('Start Date')

            with s_col3:
                end_date = st.date_input('End Date')

            question = st.text_input('Your Query')

            # If the query is not empty, process it
            if st.button('Submit'):

                # Check date
                if start_date < end_date:
                    if question:
                        st.write('Processing your query...')
                        try:
                            result = ss_query(selected_student_name, start_date, end_date, question)
                            print(result)
                            st.write('Answer:', result['answer'])
                            for i, entry in enumerate(result['source_documents']):
                                st.write(f'Journal Entry {i+1}')
                                st.write(f'Date:', result['source_documents'][i].metadata['journal_date'].split(' ')[0])
                                st.write(f'Journal Prompt:', result['source_documents'][i].metadata['journal_title'])
                                st.write(f'Journal Entry:', result['source_documents'][i].page_content)
                        except Exception as e:
                            print(e)
                            st.write("No records found during the period selected. Please expand the time period of search")
                else:
                    st.error('Error: End date must fall after start date.')
            else:
                st.write('Please enter a query.')
else:
    error_page_redirect()