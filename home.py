import streamlit as st
import pymongo
import dbhandler
# from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar

@st.cache_resource
def connect_db():
    return dbhandler.DBHandler()


def user_update(name):
    st.session_state.username = name


db = connect_db()
st.session_state.db = db


if 'username' not in st.session_state:
    st.session_state.username = ''
    st.session_state.logged_in = False
    st.session_state.role_id = ''
    st.session_state.user_fullname = ''

if 'form' not in st.session_state:
    st.session_state.form = ''

if st.session_state.username == '':
    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    user = db.auth.find_one({'username' : username, 'password' : user_pas})
    if user:
        print("user is", user, "with the role", user['role'])
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            st.success(f"You are logged in as {username.upper()}")
            st.session_state.logged_in = True
            st.session_state.username = username

            if user['role'] == 'teacher':
                curr_teacher = db.teachers.find_one({'_id' : user['teacher_id']})
                st.session_state.user_fullname = curr_teacher['name']
                st.session_state.role_id = user['teacher_id']
                del user_pas
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.error("Username or Password is incorrect. Please try again or create an account.")
else:
    logout = st.sidebar.button(label='Log Out')
    if logout:
        user_update('')
        st.session_state.form = ''