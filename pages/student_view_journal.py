import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit
#from streamlit_extras.switch_page_button import switch_page

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = 'expanded'
)
remove_top_space_canvas()
navbar_edit()

db = st.session_state.db
if "selected_student" not in st.session_state:
    st.title("Student not yet selected")

elif st.session_state.selected_student:
    selected_student = st.session_state.selected_student
    st.title(f"Journal Entries for {selected_student['name']}")
    entries = db.get_journal_entries(selected_student['_id'])
    for entry in entries:
        st.markdown(f"**{entry['date']}**")
        st.markdown(f"{entry['title']}")
        st.markdown(f"{entry['content']}")
        st.markdown(f"---")
