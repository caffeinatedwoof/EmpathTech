import streamlit as st
import pymongo
import dbhandler
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)
from st_pages import show_pages_from_config, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

show_pages_from_config()

# def delete_page(main_script_path_str, page_name):

#     current_pages = get_pages(main_script_path_str)

#     for key, value in current_pages.items():
#         if value['page_name'] == page_name:
#             del current_pages[key]
#             break
#         else:
#             pass
#     _on_pages_changed.send()

# def add_page(main_script_path_str, page_name):
    
#     pages = get_pages(main_script_path_str)
#     main_script_path = Path(main_script_path_str)
#     pages_dir = main_script_path.parent / "pages"
#     script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
#     script_path_str = str(script_path.resolve())
#     pi, pn = page_icon_and_name(script_path)
#     psh = calc_md5(script_path_str)
#     pages[psh] = {
#         "page_script_hash": psh,
#         "page_name": pn,
#         "icon": pi,
#         "script_path": script_path_str,
#     }
#     _on_pages_changed.send()

# delete_page("login.py", "teachertest")

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
        print("user is", user)
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        print(login)
        if login:
            st.success(f"You are logged in as {username.upper()}")
            st.session_state.logged_in = True
            st.session_state.username = username

            if user['role'] == 'teacher':
                curr_teacher = db.teachers.find_one({'_id' : user['teacher_id']})
                st.session_state.user_fullname = curr_teacher['name']
                st.session_state.role_id = user['teacher_id']

                # add_page("login.py", "teachertest")
                switch_page("teachertest")
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


# if st.session_state.logged_in:
#     switch_page("page2")