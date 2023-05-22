import streamlit as st
import os
import toml
import time

from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = "collapsed"
)

data = toml.load(os.path.join('.streamlit','pages.toml'))

LOGIN_PAGE = data['main_page']['name']

# Remove navbar on load
#clear_all_but_first_page()

#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. So to make widget state persistent, the trick is to transform a widget state into a user-defined state. 
st.title("Access Denied. You are not logged in or you do not have permissions to view. Redirecting you to login page")

# Clear cache
st.runtime.legacy_caching.clear_cache()

# Simulate redirect using sleep
time.sleep(2)

switch_page(LOGIN_PAGE)