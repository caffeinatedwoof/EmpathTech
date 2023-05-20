import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_student_pages, hide_teacher_pages
from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()

LOGIN_PAGE = "home.py"
hide_student_pages()
hide_teacher_pages()
st.session_state.update(st.session_state)

#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. So to make widget state persistent, the trick is to transform a widget state into a user-defined state. 
st.session_state.update(st.session_state)

st.title("Access Denied. You do not have permissions to view. ")

# Display a button to go back home
st.button("Click here to go to login page", on_click=switch_page(LOGIN_PAGE))