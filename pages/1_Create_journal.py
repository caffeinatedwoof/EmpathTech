import streamlit as st
import os
import json
from st_helper_func import remove_top_space_canvas, navbar_edit, post_navbar_edit, hide_teacher_pages, error_page_redirect, connect_db, hide_streamlit_footer, hide_other_pages
from src.journal_utils import is_journal_entry
from src.journal_guidance import provide_journal_guidance
from src.sentiment_analysis import perform_sentiment_analysis
from streamlit_chat import message
from datetime import datetime
from src.sidebar import render_sidebar
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    # layout = "wide",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()
hide_teacher_pages()
hide_other_pages()
hide_streamlit_footer()
st.session_state.update(st.session_state)
render_sidebar()

###################
# Helper functions
##################
def map_labels(label):
    """Function that maps label categories to value equivalent

    Args:
        label (str): Either negative, neutral or positive

    Returns:
        int: Mapped value.
    """
    label = label.strip().lower()
    if label == "negative":
        return 0
    elif label == "neutral":
        return 1
    elif label == "positive":
        return 2
    
def clean_llm_output(llm_output):
    if "output:" in llm_output:
        llm_output = llm_output.replace("output:", "")
    elif "Output:" in llm_output:
        llm_output = llm_output.replace("Output:", "")

    cleaned_output = json.loads(llm_output)
    score = map_labels(cleaned_output['sentiment']["label"])
    cleaned_output['sentiment'].pop("label", None)
    cleaned_output['sentiment']["score"] = score
    return cleaned_output

def toggle_elements_disabled(state=False):
    if state == True:    
        st.session_state.title_disabled = True
        st.session_state.content_disabled = True
        st.session_state.feedback_disabled = True
        st.session_state.submit_disabled = True
        st.session_state.privacy_disabled = True
    else:    
        st.session_state.title_disabled = False
        st.session_state.content_disabled = False
        st.session_state.feedback_disabled = False
        st.session_state.submit_disabled = False
        st.session_state.privacy_disabled = False

def clear_messages():
    """Function that clears generated and past keys of session states to empty list.

    Args:
        None

    Returns:
        None
    """
    st.session_state.generated = []
    st.session_state.past = []


def clear_textboxes():
    """ empties the textboxes after entry is submitted """

    
# find student from username and cache it
@st.cache_data
def get_student(username):
    student = db.get_student(username=username)
    st.session_state.selected_student = student
    return student

def init_new_chatlog():
    """Function that initialise a new dictionary pertaining to chatlog info

    Args:
        None
    Returns:
        dict: Dictionary containing chatlog related information.
    """
    print("Initiating new chatlog")
    clear_messages()
    st.session_state.chatlog_id = None
    st.session_state.entry_value = ""
    st.session_state.date_value = datetime.today()
    st.session_state.title_value = ""
    st.session_state.create_journal_label = "Create your journal"
    chatlog = {
        "start_time": datetime.now(),
        "end_time": None,
        "student_id": student_id,
        "journal_id": None,
        "messages": []
    }
    toggle_elements_disabled(False)

    return chatlog

def save_journal(title, content, date, private):
    """Function that calls dbhandler's insert_journal_entry to store journal title, content, submission date and its privacy required to backend database.

    Args:
        title (str): 
            title of the journal entry
        content (str):
            content of the journal entry
        date (datetime):
            datetime object containing the date/time of entry creation
        privat (bool):
            Boolean status on whether entry is to be private
    Returns:
        ObjectId: _id of the journal entry
    """
    if current_chatlog['journal_id'] is None:
        journal_id = db.insert_journal_entry(student_id, title, content, date, private)
        return journal_id

def save_chatlog(chatlog):
    """Function that creates a chatlog entry or updates existing chatlog entries if applicable.

    Args:
        chatlog (dict): Dictionary containing chatlog details 
    Returns:
        None
    """
    if st.session_state.chatlog_id == None:
        chatlog_id = db.insert_chatlog(chatlog)
        st.session_state.chatlog_id = chatlog_id
    else:
        db.update_chatlog(st.session_state.chatlog_id, chatlog)

def switch_chatlog(chatlog_id):
    st.session_state.chatlog_id = chatlog_id
    chatlog_obj = db.get_chatlog(chatlog_id)
    chatlog = {
        "_id" : chatlog_id,
        "start_time": chatlog_obj['start_time'],
        "end_time": chatlog_obj["end_time"],
        "student_id": chatlog_obj["student_id"],
        "journal_id": chatlog_obj["journal_id"],
        "messages": chatlog_obj["messages"]
    }

    if chatlog['journal_id'] is not None:
        
        journal = db.get_journal_entry(chatlog['journal_id'])
        st.session_state.entry_value = journal['content']
        st.session_state.date_value = journal['date']
        st.session_state.title_value = journal['title']
        st.session_state.create_journal_label = "You have completed this journal"
        toggle_elements_disabled(True)

    else:
        st.session_state.entry_value = chatlog['messages'][-1]['student_msg']
        st.session_state.date_value = chatlog['start_time']
        st.session_state.title_value = ""
        st.session_state.create_journal_label = "Continue writing your journal"
        toggle_elements_disabled(False)

    clear_messages()
    for message in chatlog['messages']:
        st.session_state.past.append(message['student_msg'])
        st.session_state.generated.append(message['llm_msg'])

    return chatlog

if 'user_fullname' not in st.session_state:
    error_page_redirect()

lock_icon_path = os.path.join(os.getcwd(), 'src', 'images', 'lock-icon.png')
lock_image = Image.open(lock_icon_path)
unlock_icon_path = os.path.join(os.getcwd(), 'src', 'images', 'unlock-icon.png')
unlock_image = Image.open(unlock_icon_path)
if 'logged_in' in st.session_state and st.session_state.logged_in:
    # This is to facilitate reconnection
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()
    post_navbar_edit(st.session_state.user_fullname)

    
    # db = st.session_state.db
    username = st.session_state.username

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []


    current_student = get_student(username)
    student_name = current_student['name']
    student_id = current_student['_id']
    #print(student_id)

    # Temp variables to capture if get feed back, submit journal or make my journal entry private widgets are being clicked. Default setting is all false.
    get_feedback_state = False
    submit_journal = False
    make_journal_private = False

    if 'chatlog_id' not in st.session_state or st.session_state.chatlog_id is None:
        current_chatlog = init_new_chatlog()

    else:
        current_chatlog = switch_chatlog(st.session_state.chatlog_id)
        print("Switch to existing chatlog")

    init_new_chatlog()
    st.title(st.session_state.create_journal_label)
    post_navbar_edit(st.session_state.user_fullname)
    entry_title = st.text_input("Give your entry a title", key="journal_title",
                                placeholder="Eg. Interesting encounter, What a day today",
                                disabled=st.session_state.title_disabled)
    st.markdown(f"Date: {st.session_state.date_value.strftime('%d %b %Y')}")

    text_input = st.text_area("Type your journal entry here!",
                              placeholder="E.g Today, I encountered something which made me....",
                              disabled=st.session_state.content_disabled)

    checkbox_col1, checkbox_col2, _ = st.columns([3,1,4])

    with checkbox_col1:
        if st.checkbox("Make my journal entry private",
                    disabled=st.session_state.privacy_disabled):
            make_journal_private = True

    with checkbox_col2:
        if make_journal_private:
            st.image(lock_image, width=40)
        else:
            st.image(unlock_image, width=40)

    col1, col2, _ = st.columns([1, 1, 3])

    # Feedback button
    with col1:
        if st.button("Get Feedback", disabled=st.session_state.feedback_disabled):
            get_feedback_state = True

    # Submit journal
    with col2:
        if st.button("Submit Journal", 
                     disabled=st.session_state.submit_disabled):
            submit_journal = True

    # Case when get feedback
    if get_feedback_state:
        with st.spinner('Checking entry...'):
            check = is_journal_entry(text_input)
            # print(check)

        if check['journal_entry']:
            with st.spinner('Generating feedback...'):
                output = provide_journal_guidance(text_input)
        else:
            # output = check['explanation']
            output = "Please enter a valid journal entry."
        st.session_state.past.append(text_input)
        st.session_state.generated.append(output)
        current_chatlog['messages'].append({"student_msg": text_input, "llm_msg": output})
        current_chatlog['endtime'] = datetime.now()
        save_chatlog(current_chatlog)

    # Case when journal submitted
    if submit_journal:
        # Check if journal entry is valid
        with st.spinner('Checking entry before submission...'):
            check = is_journal_entry(text_input)

            # Save journal to db
            if check['journal_entry']:
                entry_date = current_chatlog['start_time']

                # Uses function to call db.insert_journal_entry
                journal_id = save_journal(entry_title,
                                          text_input,
                                          entry_date, private=make_journal_private)
                
                current_chatlog['journal_id'] = journal_id
                save_chatlog(current_chatlog)
                print(journal_id, "has been saved to db")

                # Submit journal for sentiment analysis
                sent_analysis_results = perform_sentiment_analysis(text_input)
                cleaned_output = clean_llm_output(sent_analysis_results)
                db.insert_summary(journal_id, cleaned_output)
                init_new_chatlog()
                st.session_state["success_message"] = "Your journal has been submitted!"
                switch_page("View past journals")
                
            else:
                st.error("Please enter a valid journal entry.")
            
    st.markdown("---")

    for i in range(len(st.session_state["generated"])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

    # Reset temp states when done
    get_feedback_state = False
    submit_journal = False
    make_journal_private = False

else:   
    error_page_redirect()