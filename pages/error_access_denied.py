import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit
from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "centered",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()


st.title("Access Denied. You do not have permissions to view. ")

# Display a button to go back home
st.button("Click here to go to login page", on_click=switch_page("home"))