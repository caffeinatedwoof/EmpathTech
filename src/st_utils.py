import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_teacher_pages, error_page_redirect, connect_db
from src.journal_utils import is_journal_entry
from src.journal_guidance import provide_journal_guidance
from src.sentiment_analysis import perform_sentiment_analysis
import json
from streamlit_chat import message
from datetime import datetime
import pymongo

import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from dbhandler import DBHandler

db = DBHandler()

def clear_messages():
    st.session_state.generated = []
    st.session_state.past = []


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

def init_new_chatlog(student_id):
    print("chatlog id does not exist")
    clear_messages()
    st.session_state.chatlog_id = None
    st.session_state.entry_value = ""
    st.session_state.date_value = datetime.today()
    st.session_state.journal_title = ""
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

def show_chatlog_filter(student_id, status='Incomplete'):
    if status=='Complete':
        return [chatlogs for chatlogs in db.get_all_chatlogs(student_id) if chatlogs['journal_id'] is not None]
    else:
        return [chatlogs for chatlogs in db.get_all_chatlogs(student_id) if chatlogs['journal_id'] is None]
    
def chatlog_list_format(chatlog_obj):
    return chatlog_obj['start_time'].strftime("%d %b %Y %H:%M")

def save_chatlog(chatlog):
    if st.session_state.chatlog_id == None:
        chatlog_id = db.insert_chatlog(chatlog)
        st.session_state.chatlog_id = chatlog_id
    else:
        db.update_chatlog(st.session_state.chatlog_id, chatlog)

def get_student(username=None, student_name=None):
    if username is None:
        student = db.get_student(student_name=student_name)
    else:
        student = db.get_student(username=username)
    st.session_state.selected_student = student
    return student

def save_journal(title, content, date, current_chatlog, student_id):
    if current_chatlog['journal_id'] is None:
        journal_id = db.insert_journal_entry(student_id, title, content, date)
        return journal_id
    
def map_labels(label):
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

def get_journal_comments(journal_id):
    print(journal_id)
    if journal_id is not None and journal_id != "":
        entry = db.get_journal_entry(journal_id)
        comments = entry['comments']
        return comments
