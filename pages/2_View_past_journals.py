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

    # Initialize variables
    student_id = st.session_state.role_id
    student_name = st.session_state.user_fullname

    st.title(f"Journal Entries for {student_name}")
    entries = db.get_journal_entries(student_id)
    for entry in entries:
        st.markdown(f"**{entry['date']}**")
        st.markdown(f"{entry['title']}")
        st.markdown(f"{entry['content']}")
        st.markdown(f"---")

else:
    error_page_redirect()