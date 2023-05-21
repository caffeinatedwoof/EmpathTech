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

    # Consolidate results and reverse their order. Not needed if we can use pymongo to sort based on dates itself
    entries_list = [i for i in entries][::-1]

    # Iterate cursor
    for entry in entries_list:
        subcol1, subcol2, subcol3, subcol4= st.columns([2,0.5,0.5,1.5])
        with subcol1:
            st.markdown(f"{entry['title']}")
            st.markdown(f"{entry['content']}")

        with subcol2:
            st.markdown(f"Date submitted")
            st.markdown(f"**{entry['date']}**")

        with subcol3:
            st.markdown("Sentiment")
            st.markdown("TBC")

        with subcol4:
            with st.expander("Click to provide comments"):
                sentence = st.text_area('Input your text here:', key=str(entry['_id'])+'_text_student') 
                button = st.button('Click to submit', key=str(entry['_id'])+'_button_student')
            with st.expander("Click to view past comments"):
                st.write("No comments available")
        st.markdown("----")

else:
    error_page_redirect()