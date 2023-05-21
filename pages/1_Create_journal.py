import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_teacher_pages, error_page_redirect, connect_db

#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()
hide_teacher_pages()
st.session_state.update(st.session_state)

if 'logged_in' in st.session_state and st.session_state.logged_in:

    if 'db' in st.session_state:
        db = st.session_state.db
    else:
        db = connect_db()

else:
    error_page_redirect()