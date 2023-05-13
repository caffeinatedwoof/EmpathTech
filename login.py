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

def delete_page(main_script_path_str, page_name):

    current_pages = get_pages(main_script_path_str)

    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass
    _on_pages_changed.send()

def add_page(main_script_path_str, page_name):
    
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()

delete_page("app.py", "page2")

@st.cache_resource
def connect_db():
    return dbhandler.DBHandler()


def user_update(name):
    st.session_state.username = name

db = connect_db()


if 'username' not in st.session_state:
    st.session_state.username = ''
    st.session_state.logged_in = False
if 'form' not in st.session_state:
    st.session_state.form = ''

if st.session_state.username == '':
    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    
    if db.auth.find_one({'log' : username, 'pass' : user_pas}):
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            st.success(f"You are logged in as {username.upper()}")
            st.session_state.logged_in = True
            st.session_state.username = username
            add_page("app.py", "page2")
            switch_page("page2")
            del user_pas
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.sidebar.error("Username or Password is incorrect. Please try again or create an account.")
else:
    logout = st.sidebar.button(label='Log Out')
    if logout:
        user_update('')
        st.session_state.form = ''


# if st.session_state.logged_in:
#     switch_page("page2")