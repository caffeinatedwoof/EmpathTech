import streamlit as st
from st_helper_func import remove_top_space_canvas, navbar_edit, hide_teacher_pages, error_page_redirect, connect_db
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime

# Layout config 
st.set_page_config(
    # layout = "wide",
    initial_sidebar_state = 'expanded'
)

remove_top_space_canvas()
navbar_edit()
hide_teacher_pages()

# st.session_state.update(st.session_state)

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

# Iterate cursor
for entry in entries:
    subcol1, subcol2, subcol3 = st.columns([0.5,2,0.8])
    with subcol2:
        content = entry['content']
        content = content[:100] + "..." if len(content) > 100 else content
        st.markdown(f"{content}")

    with subcol1:

        # format entry datetime to dd/mm/yyyy
        entry_date = datetime.strftime(entry['date'], "%d/%m/%Y")
        st.markdown(f"{entry_date}")

    with subcol3:
        if st.button("View full entry", key=f"{entry['_id']}_btn"):
            chatlog = db.chatlogs.find_one({"journal_id": entry['_id']})
            st.session_state.chatlog_id = chatlog['_id']
            switch_page("View Journal")
        pass

else:
    error_page_redirect()