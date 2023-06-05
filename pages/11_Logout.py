import streamlit as st
import os
import toml
from streamlit_extras.switch_page_button import switch_page
from st_helper_func import disable_sidebar, hide_streamlit_footer

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = "collapsed"
)

data = toml.load(os.path.join('.streamlit','pages.toml'))

LOGIN_PAGE = data['main_page']['name']

# Remove navbar on load
hide_streamlit_footer()
disable_sidebar()
#Internally, Streamlit manages two different states : user-defined states (used when you store values like so: st.session_state.my_state = "hey"), and widget states (when you use a key parameter). These two states work a little bit differently. User-defined states are completely persistent after multiple runs. However if a widget with a key assigned disappear (when your page changes for example), its associated widget state will be cleared. So to make widget state persistent, the trick is to transform a widget state into a user-defined state. 
st.title("Logging out of your account ...")

# Clear cache
st.runtime.legacy_caching.clear_cache()

switch_page(LOGIN_PAGE)