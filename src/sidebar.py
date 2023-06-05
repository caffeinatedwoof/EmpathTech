import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.gamification import gamified_sidebar
from st_helper_func import show_privacy_data_protection_footer


def display_name():
    if "user_fullname" in st.session_state:
        name = st.session_state.user_fullname
        st.markdown(f"<div style='text-align:center; color: #00bbf0';> Hello {name}, <br> Welcome to EmpathJot </div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;'>Welcome to EmpathJot</div>", unsafe_allow_html=True)


def render_sidebar():
    st.markdown("""<style>
    .css-1oe5cao {
        display: None;
    }</style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        display_name()
        st.markdown("""<hr>""", unsafe_allow_html=True)
    if st.session_state.role == 'student':
        with st.sidebar:
            if st.button("Create journal", use_container_width=True, type="primary"):
                switch_page("Create Journal")
            if st.button("View Past Journals", use_container_width=True, type="primary"):
                switch_page("View past journals")
            if st.button("Logout", use_container_width=True, type="primary"):
                switch_page("Logout")
            student_id = st.session_state.role_id
            gamified_sidebar(student_id)
    elif st.session_state.role == 'teacher':
        with st.sidebar:
            if st.button("Teaching Classes", use_container_width=True, type="primary"):
                switch_page("Teaching_classes")
            if st.button("Sentiment Dashboard", use_container_width=True, type="primary"):
                switch_page("Dashboard_summary")
            if st.button("Browse Student Journals", use_container_width=True, type="primary"):
                switch_page("View_student_journal")
            if st.button("Logout", use_container_width=True, type="primary"):
                switch_page("Logout")
    with st.sidebar:
        show_privacy_data_protection_footer()