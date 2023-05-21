from src.journal_utils import is_journal_entry
from src.journal_guidance import provide_journal_guidance
import streamlit as st
from streamlit_chat import message
from datetime import date, datetime

db = st.session_state.db
username = st.session_state.username

def toggle_elements_disabled(state=False):
    if state == True:    
        st.session_state.title_disabled = True
        st.session_state.content_disabled = True
        st.session_state.feedback_disabled = True
        st.session_state.submit_disabled = True
    else:    
        st.session_state.title_disabled = False
        st.session_state.content_disabled = False
        st.session_state.feedback_disabled = False
        st.session_state.submit_disabled = False

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def clear_messages():
    st.session_state.generated = []
    st.session_state.past = []

# find student from username and cache it
@st.cache_data
def get_student(username):
    student = db.get_student(username=username)
    st.session_state.selected_student = student
    return student

def init_new_chatlog():
    print("chatlog id does not exist")
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

def save_journal(title, content, date):
    if current_chatlog['journal_id'] is None:
        journal_id = db.insert_journal_entry(student_id, title, content, date)
        return journal_id

current_student = get_student(username)
student_name = current_student['name']
student_id = current_student['_id']
st.markdown(f"Hi, {student_name}!")

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

if 'chatlog_id' not in st.session_state or st.session_state.chatlog_id is None:
    current_chatlog = init_new_chatlog()

else:
    current_chatlog = switch_chatlog(st.session_state.chatlog_id)



def show_chatlog_filter(status='Incomplete'):
    if status=='Complete':
        return [chatlogs for chatlogs in db.get_all_chatlogs(student_id) if chatlogs['journal_id'] is not None]
    else:
        return [chatlogs for chatlogs in db.get_all_chatlogs(student_id) if chatlogs['journal_id'] is None]
    
def chatlog_list_format(chatlog_obj):
    return chatlog_obj['start_time'].strftime("%d %b %Y %H:%M")

# with st.sidebar.form(key="journal_selection"):
with st.sidebar:
    journal_type = st.radio("Journal type", ["Incomplete", "Complete"])
    if journal_type == "Complete":
        chatlog_list = show_chatlog_filter('Complete')
    else:
        chatlog_list = show_chatlog_filter()
        
    chatlog_selection = st.selectbox("Your journals", chatlog_list, format_func=chatlog_list_format)
    submit_button = st.button(label="Select journal")
    if submit_button:
        if chatlog_selection is None:
            current_chatlog = init_new_chatlog()
            print("Started a new chatlog")
        else:
            current_chatlog = switch_chatlog(chatlog_selection['_id'])
            print("Switched chatlog to", current_chatlog['_id'])

def save_chatlog(chatlog):
    if st.session_state.chatlog_id == None:
        chatlog_id = db.insert_chatlog(chatlog)
        st.session_state.chatlog_id = chatlog_id
    else:
        db.update_chatlog(st.session_state.chatlog_id, chatlog)

st.title(st.session_state.create_journal_label)
entry_title = st.text_input("Give your entry a title", value=st.session_state.title_value, key="journal_title", disabled=st.session_state.title_disabled)
st.markdown(f"Date: {st.session_state.date_value.strftime('%d %b %Y')}")

text_input = st.text_area("Type your journal entry here!", value=st.session_state.entry_value, disabled=st.session_state.content_disabled)

# Get feedback
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    if st.button("Get Feedback", disabled=st.session_state.feedback_disabled):
        with st.spinner('Checking entry...'):
            check = is_journal_entry(text_input)

        if check['journal_entry']:
            with st.spinner('Generating feedback...'):
                output = provide_journal_guidance(text_input)
        else:
            # output = check['explanation']
            output = "Please enter a valid journal entry."

        print(output)
        print("type of output", type(output))

        st.session_state.past.append(text_input)
        st.session_state.generated.append(output)
        current_chatlog['messages'].append({"student_msg": text_input, "llm_msg": output})
        current_chatlog['endtime'] = datetime.now()
        save_chatlog(current_chatlog)

with col2:
    if st.button("Submit Journal", disabled=st.session_state.submit_disabled):
        # Check if journal entry is valid
        with st.spinner('Checking entry before submission...'):
            check = is_journal_entry(text_input)

        # Save journal to db
        if check['journal_entry']:
            entry_date = current_chatlog['start_time']
            journal_id = save_journal(entry_title, text_input, entry_date)
            current_chatlog['journal_id'] = journal_id
            save_chatlog(current_chatlog)
            print(journal_id)

        # Submit journal for sentiment analysis


        # Save sentiment analysis to db
        
        pass

st.markdown("---")

for i in range(len(st.session_state["generated"])-1, -1, -1):
    message(st.session_state["generated"][i], key=str(i))
    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
    