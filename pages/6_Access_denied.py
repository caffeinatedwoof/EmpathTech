import streamlit as st
import os
import toml
from st_helper_func import remove_top_space_canvas, navbar_edit, reset_session_state, clear_all_but_first_page
from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()

data = toml.load(os.path.join('.streamlit','pages.toml'))

LOGIN_PAGE = data['login_path_name']['name']

reset_session_state()

# Remove navbar on load
clear_all_but_first_page()

#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. So to make widget state persistent, the trick is to transform a widget state into a user-defined state. 
st.title("Access Denied. You are not logged in or you do not have permissions to view.")

# Display a button to go back home
switch_page(LOGIN_PAGE)
