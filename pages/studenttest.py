import streamlit as st

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
