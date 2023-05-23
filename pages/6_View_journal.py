import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, post_navbar_edit, hide_teacher_pages, error_page_redirect, connect_db, hide_student_pages
from src.journal_utils import is_journal_entry
from src.journal_guidance import provide_journal_guidance
from src.sentiment_analysis import perform_sentiment_analysis

from streamlit_chat import message
from datetime import datetime
import pymongo
from src.st_utils import switch_chatlog, show_chatlog_filter, chatlog_list_format, save_chatlog, get_student, save_journal, clean_llm_output, get_journal_comments


#######
#Helper function
#######
# st.session_state.update(st.session_state)
    # Render journal display / entry form
def render_comments():
    if comments is None:
        st.markdown("No comments yet!")
    elif len(comments) == 0:
            st.markdown("No comments yet!")
    else:
        for comment in comments:
            if (comment is None or type(comment) == str):
                st.markdown("No comments yet!")
            else:
                comment_col1, comment_col2 = st.columns(2)
                with comment_col1:
                    st.markdown(comment["comment"])
                with comment_col2:
                    comment_date = datetime.strftime(comment['date'], "%d/%m/%Y %H:%M")
                    teacher = db.get_teacher(comment["teacher_id"])
                    comment_string = f"By: {teacher['name']} on {comment_date}"
                    st.markdown(comment_string)
                st.markdown('---')
# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'collapsed'
)
remove_top_space_canvas()
navbar_edit()
post_navbar_edit(st.session_state.user_fullname)

# Since it is a common page viewed by student and teacher, hide navigation pages accordingly based on role
if st.session_state.role == 'student':
    hide_teacher_pages()
else:
    hide_student_pages()

# Set None as current student name by default if for some reason session state did not persist.
if "current_student_name" not in st.session_state:
    st.session_state["current_student_name"] = None

# Check if status is logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()
        
    username = st.session_state.username

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    if "current_student_name" not in st.session_state:
        current_student = get_student(username)
    else:
        current_student = db.get_student(student_name=st.session_state.current_student_name)


    student_name = current_student['name']
    student_id = current_student['_id']
    print(student_id)

    latest_chatlog = db.chatlogs.find_one({"student_id": student_id, "journal_id": None}, sort=[("start_time", pymongo.DESCENDING)])

    if latest_chatlog is None:
        latest_chatlog = db.chatlogs.find_one({"student_id": student_id}, sort=[("start_time", pymongo.DESCENDING)])

    if 'chatlog_id' not in st.session_state or st.session_state.chatlog_id is None:
        current_chatlog = switch_chatlog(latest_chatlog['_id'])

    else:
        current_chatlog = switch_chatlog(st.session_state.chatlog_id)

    # Render sidebar for View journals / journal selection
    with st.sidebar:
        journal_type = st.radio("Journal type", ["Incomplete", "Complete"], )
        if journal_type == "Complete":
            chatlog_list = show_chatlog_filter(student_id, 'Complete')
        else:
            chatlog_list = show_chatlog_filter(student_id)
            
        chatlog_selection = st.selectbox("Your journals", chatlog_list, format_func=chatlog_list_format)
        submit_button = st.button(label="Select journal")
        if submit_button:
            if chatlog_selection is None:
                # current_chatlog = init_new_chatlog()
                print("Started a new chatlog")
            else:
                current_chatlog = switch_chatlog(chatlog_selection['_id'])
                print("Switched chatlog to", current_chatlog['_id'])

    padding, container1, padding2, container2, padding3 = st.columns([0.5, 3, 0.5, 2, 0.5])

    # st.markdown(f"Hi, {student_name}!") # Display student name
    with padding:
        pass
    with container1:
        st.title(f"{student_name}'s Journal")
        st.session_state.label_visibility = "hidden"
        if st.session_state.is_teacher == False:
            st.header(st.session_state.create_journal_label)
            st.session_state.label_visibility = "visible"
        # entry_title = st.text_input("Give your entry a title", key="journal_title", disabled=st.session_state.title_disabled)
        st.markdown(f"Date: {st.session_state.date_value.strftime('%d %b %Y')}")

        text_input = st.text_area("Type your journal entry here!", value=st.session_state.entry_value, height=300, disabled=st.session_state.content_disabled, label_visibility=st.session_state.label_visibility)

        # Get feedback
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            feedback_btn_placeholder = st.empty()
            
        with col2:
            submit_btn_placeholder = st.empty()
        st.markdown("---")

        if current_chatlog['journal_id'] is not None:
            feedback_btn_placeholder.empty()
            submit_btn_placeholder.empty()

        else:
            with feedback_btn_placeholder.container():
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

            with submit_btn_placeholder.container():
                if st.button("Submit Journal", disabled=st.session_state.submit_disabled):
                    # Check if journal entry is valid
                    with st.spinner('Checking entry before submission...'):
                        check = is_journal_entry(text_input)

                        # Save journal to db
                        if check['journal_entry']:
                            entry_date = current_chatlog['start_time']
                            entry_title = "Freewriting"
                            journal_id = save_journal(entry_title, text_input, entry_date, current_chatlog, student_id)
                            current_chatlog['journal_id'] = journal_id
                            save_chatlog(current_chatlog)
                            print(journal_id, "has been saved to db")
                            st.success('Your journal has been submitted!', icon="✅")

                            # Submit journal for sentiment analysis
                            sent_analysis_results = perform_sentiment_analysis(text_input)
                            cleaned_output = clean_llm_output(sent_analysis_results)
                            db.insert_summary(journal_id, cleaned_output)
                                            
                        else:
                            st.error("Please enter a valid journal entry.")

        # Render chat messages if chat is available
        for i in range(len(st.session_state["generated"])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
    with padding2:
        pass
    with container2:
        st.header("Past comments on your current journal entry")
        comment_placeholder = st.empty()
        comments = get_journal_comments(current_chatlog['journal_id'])
        with comment_placeholder.container():
            render_comments()
            # if len(comments) == 0:
            #     st.markdown("No comments yet!")
            # print(comments)
            # for comment in comments:
            #     print(type(comment))
            #     if (comment is None or type(comment) == str):
            #         st.markdown("No comments yet!")
            #     else:
            #         comment_date = datetime.strftime(comment['date'], "%d/%m/%Y %H:%M")
            #         st.markdown(comment_date)
            #         st.markdown(comment["comment"])
            #         teacher = db.get_teacher(comment["teacher_id"])
            #         st.markdown(f"- {teacher['name']}")
        if st.session_state.is_teacher:
            comment_input = st.text_area("Add a comment", key="comment_input")
            submit_comment = st.button("Submit comment")
            if submit_comment:
                db.insert_comment(current_chatlog['journal_id'], comment_input, st.session_state.role_id)
                st.success("Comment submitted!")
                with comment_placeholder.container():
                    render_comments()

    with padding3:
        pass

else:
    error_page_redirect()