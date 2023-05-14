# Custom class import
# from streamlit_extras.switch_page_button import switch_page
from pathlib import Path
from st_pages import show_pages_from_config, add_page_title
from st_helper_func import remove_top_space_canvas, navbar_edit
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages
from pathlib import Path



import json
import time
import streamlit as st
import dbhandler

LOGIN_PAGE = "home.py"

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()


# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar

# all pages request
def get_all_pages():
    """Function that retrieves all pages info by utilising streamlit's get_pages function and writes to a json file on such information. Otherwise, it reads existing pages.json.

    Returns:
        dict: Dictionary with strings as keys, and dictionaries containing details about that page.
    """

    # Returns a dictionary with strings as keys, and dictionaries containing details about that page
    default_pages = get_pages(LOGIN_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text(encoding='utf-8'))
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4), encoding='utf-8')

    st.session_state.pages = saved_default_pages
    return saved_default_pages

# clear all page but not login page
def clear_all_but_first_page():
    """Function that retrieves all pages info by utilising streamlit's get_pages function and writes to a json file on such information. Otherwise, it reads existing pages.json.

    Returns:
        dict: Dictionary with strings as keys, and dictionaries containing details about that page.
    """
    current_pages = get_pages(LOGIN_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Extract current page information prior to removing all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    # Send event change signal
    _on_pages_changed.send()

# show all pages
def update_current_pages():
    """This function updates current pages by comparing with known information
    """
    current_pages = get_pages(LOGIN_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()

# Hide default page
def hide_page(name):
    """Function that hides only the stated page name

    Args:
        name (str): Page name to hide

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()

            # Update session state pages
            st.session_state.pages = current_pages
            break
    
    return None

def hide_student_pages():
    """Function that hides pages related to student view, namely: error_access_denied, student_view_journal, student_create_journal

    Args:
        None

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)

    student_pages_name_list = ["error_access_denied",
                               "student_view_journal",
                               "student_create_journal"]

    for key, val in current_pages.items():
        if val["page_name"] in student_pages_name_list:
            del current_pages[key]
        #    _on_pages_changed.send()
        else:
            continue
    
    # Update session state pages
    st.session_state.pages = current_pages

    _on_pages_changed.send()

def hide_teacher_pages():
    """Function that hides pages related to teacher view, namely: error_access_denied, teacher_dashboard, teacher_teaching_class, teacher_view_student_journal

    Args:
        None

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)

    teacher_pages_name_list = ["error_access_denied",
                               "teacher_dashboard",
                               "teacher_teaching_class",
                               "teacher_view_student_journal"
                               ]

    for key, val in current_pages.items():
        if val["page_name"] in teacher_pages_name_list:
            del current_pages[key]
        #    _on_pages_changed.send()
        else:
            continue

    # Update session state pages
    st.session_state.pages = current_pages

    _on_pages_changed.send()

    return None

@st.cache_resource
def connect_db():
    db = dbhandler.DBHandler()
    st.session_state.db = db
    return db

def user_update(name):
    """Function that updates streamlit session username with input name

    Args:
        name (str): Name of user
    """
    st.session_state.username = name

    return None

def reset_session_state():
    """Function that resets streamlit session state involving username, logged_in state, role_id, user_full_name and form

    Returns:
        None
    """
    st.session_state.username = ''
    st.session_state.logged_in = False
    st.session_state.role_id = ''
    st.session_state.user_fullname = ''
    st.session_state.form = ''
    return None



# calling only default(login) page  
clear_all_but_first_page()

# Preset all session states
if 'logged_in' not in st.session_state:
    reset_session_state()

# Init connect to database, which will set session state
db = connect_db()

def main():
    # Main function

    if st.session_state.username == '':
        # Authenticate with database information, provides additional detail on the role of the login
        st.title("Welcome to Empathtech!")
        st.subheader("Login into your account")

        login_form = st.form(key='signin_form', clear_on_submit=True)
        username = login_form.text_input(label='Enter Username')
        user_pas = login_form.text_input(label='Enter Password', type='password')
        # SHould place after text input before connect db
        login_submit = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        
        if login_submit and username and user_pas:
            # Init connect to database
            user = db.auth.find_one({'username' : username, 'password' : user_pas})
            if user:
                if login_submit:
                    st.success(f"You are logged in as {username.upper()}, a {user['role']}")
                    st.session_state.logged_in = True
                    if st.session_state["logged_in"]:
                        get_all_pages()
                    st.session_state.username = username
                    
                    # Clear variable to prevent info storage
                    del user_pas
                    # Once update state, switch to relevant page
                    if user['role'] == 'teacher':
                        curr_teacher = db.teachers.find_one({'_id' : user['teacher_id']})
                        st.session_state.user_fullname = curr_teacher['name']
                        st.session_state.role_id = user['teacher_id']

                        # Hide student related pages
                        hide_student_pages()
                        # Route to teaching page
                        switch_page('teacher_teaching_class')

                    elif user['role'] == 'student':
                        # Hide student related pages
                        hide_teacher_pages()

                        # Route to Student View Journal page
                        switch_page('student_view_journal')
                    else:
                        # Route to 404 error
                        switch_page('Error404')

            # If no matching details or empty
            else:
                st.error("Username or Password is incorrect. Please try again or create an account.")
        # Click submit without username or password input
        elif login_submit and (not username or not user_pas):
            st.error("Please check if you have entered the username and user password. Reloading page")
            time.sleep(2)
            # Reload page
            st.experimental_rerun()

    # Case when user is logged in
    if st.session_state.logged_in == True:
        logout = st.sidebar.button(label='Log Out')
        if logout:
            reset_session_state()



if __name__ == "__main__":
    main()