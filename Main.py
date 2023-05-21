# Custom class import
import os
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from st_helper_func import remove_top_space_canvas, navbar_edit, reset_session_state, update_current_pages, clear_all_but_first_page, connect_db

#from streamlit.source_util import _on_pages_changed, get_pages
# import json
import time
import streamlit as st
import toml


# GLOBAL VARIABLE ON PAGES
#LOGIN_PAGE = "Login.py"
#TEACHER_LANDING_PAGE = "Teaching_classes"
#STUDENT_LANDING_PAGE = "View_journal"
#ERROR_PAGE = "Access_denied"
# Load landing page info
data = toml.load(os.path.join('.streamlit','pages.toml'))

TEACHER_LANDING_PAGE = data['teacher']['classes']['name']
STUDENT_LANDING_PAGE = data['student']['view_past_journal']['name']

#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. To make widget state persistent, the trick is to transform a widget state into a user-defined state. 

#st.session_state.update(st.session_state)

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'collapsed'
)
remove_top_space_canvas()
navbar_edit()


def st_state_update(state, value):
    """Function that updates streamlit session states with given state and values info

    Args:
        state(str): Name of state
        value(any): Value for the state

    Returns:
        None
    """
    st.session_state[state]= value

    return None


def main():
    # Main function

    # Reset all session state
    reset_session_state()

    # Remove navbar on load
    clear_all_but_first_page()

    # Init connect to database, which will set session state
    db = connect_db()
    
    st.session_state.username = ''
    # Authenticate with database information, provides additional detail on the role of the login
    st.title("Welcome to Empathtech Platform!")
    st.subheader("Login into your account")

    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')

    # SHould place after text input before connect db
    login_submit = login_form.form_submit_button(label='Sign In')

    if login_submit and username and user_pas:
        st_state_update('username', True)
        # Init connect to database
        update_current_pages()

        # Check database for authentication
        user = db.auth.find_one({'username' : username, 'password' : user_pas})
        if user and login_submit:
            st.success(f"You are logged in as {username.upper()}, a {user['role']}")
            st_state_update('logged_in', True)
            st_state_update('username', username)            
            # Clear variable to prevent info storage
            del user_pas

            # Once update state, switch to relevant page
            if user['role'] == 'teacher':
                # Get info from teacher database which contains mapping of authentication info and profile.
                curr_teacher = db.teachers.find_one({'_id' : user['teacher_id']})
                st_state_update('user_fullname', curr_teacher['name'])
                st_state_update('role_id', user['teacher_id'])

                # If more class are taught, curr_teacher['class'] would be a list instead of a string
                st_state_update('teaching_class', curr_teacher['class'])

                # Route to teaching page
                switch_page(TEACHER_LANDING_PAGE)

            elif user['role'] == 'student':
                # Get info from student database which contains mapping of authentication info and profile
                curr_student = db.students.find_one({'_id' : user['student_id']})
                st_state_update('user_fullname', curr_student['name'])
                st_state_update('class', curr_student['class'])
                st_state_update('role_id', user['student_id'])

                # Route to Student View Journal page
                switch_page(STUDENT_LANDING_PAGE)

            else:
                # Route to error page if login has some unknown issue
                st.error("Error in retrieving your role for account. Please relogin")
                # Reload page
                st.experimental_rerun()

        # If no matching details or empty
        else:
            st.error("Username or Password is incorrect. Please try again or create an account.")
    # Click submit without username or password input
    elif login_submit and (not username or not user_pas):
        st.error("Please check if you have entered the username and user password. Reloading page")
        time.sleep(2)
        # Reload page
        st.experimental_rerun()



if __name__ == "__main__":
    main()