# Custom class import

from pathlib import Path
from st_pages import show_pages_from_config, add_page_title
from streamlit_extras.switch_page_button import switch_page
from st_helper_func import remove_top_space_canvas, navbar_edit, reset_session_state, update_current_pages, clear_all_but_first_page

#from streamlit.source_util import _on_pages_changed, get_pages
# import json
import time
import streamlit as st
import dbhandler

# GLOBAL VARIABLE ON PAGES
LOGIN_PAGE = "home.py"
TEACHER_LANDING_PAGE = "teacher_teaching_class"
STUDENT_LANDING_PAGE = "student_view_journal"
ERROR_PAGE = "error_access_denied"

#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. To make widget state persistent, the trick is to transform a widget state into a user-defined state. 

#st.session_state.update(st.session_state)

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()

#@st.cache_resource
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


def main():
    # Main function
    
    # Reset all session state
    reset_session_state()

    # Remove navbar on load
    clear_all_but_first_page()

    # Init connect to database, which will set session state
    db = connect_db()
    
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
            update_current_pages()
            user = db.auth.find_one({'username' : username, 'password' : user_pas})
            if user:
                if login_submit:
                    st.success(f"You are logged in as {username.upper()}, a {user['role']}")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    
                    # Clear variable to prevent info storage
                    del user_pas
                    # Once update state, switch to relevant page
                    if user['role'] == 'teacher':
                        curr_teacher = db.teachers.find_one({'_id' : user['teacher_id']})
                        st.session_state.user_fullname = curr_teacher['name']
                        st.session_state.role_id = user['teacher_id']

                        # Route to teaching page
                        switch_page(TEACHER_LANDING_PAGE)


                    elif user['role'] == 'student':
                        # Route to Student View Journal page
                        switch_page(STUDENT_LANDING_PAGE)

                    else:
                        # Route to 404 error
                        switch_page(ERROR_PAGE)

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