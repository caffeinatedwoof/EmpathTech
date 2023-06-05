import streamlit as st
from st_helper_func import remove_top_space_canvas, hide_other_pages, hide_streamlit_footer, hide_teacher_pages, navbar_edit, post_navbar_edit, show_privacy_data_protection_footer, error_page_redirect

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = "expanded"
)

if 'user_fullname' not in st.session_state:
    error_page_redirect()

remove_top_space_canvas()
navbar_edit()
post_navbar_edit(st.session_state.user_fullname)
hide_other_pages()
hide_teacher_pages()
hide_streamlit_footer()

_, colT2, _ = st.columns(3)

with colT2:
    st.title("Note to Students")

st.markdown("""
    Welcome to EmpathJot!

    Your thoughts and feelings matter, and we are here to support you. We want you to feel safe and secure when using our app, so we want to share some important information about your privacy.

    Remember, EmpathJot is designed to be a place where you can freely express yourself. You have the option to choose whether to share your journal entry with your teacher or keep it private. Your privacy is important to us, and we respect your decision.

    However, we want to ensure your well-being and the well-being of others. If there's anything in your journal entry that indicates the following:

        1. If you mention breaking the law or planning to do so;

        2. If you express thoughts of self-harm or harm towards others, or;

        3. If you reveal that you have been or are being harmed,

    We have a responsibility to step in and ensure your safety. In these specific situations, your journal entry will be flagged for your teacher to see, so that they can provide the necessary support and help.

    Please remember that our utmost priority is your well-being. We are here to support and care for you. If you ever need assistance or have any concerns, don't hesitate to reach out to your teacher or a trusted adult.

    Thank you for choosing EmpathJot as your journaling companion. Together, we can create a safe and nurturing environment for everyone to express themselves and grow.

    **Do navigate to different pages using the navgiation bar on the left to start using this app.**

    Warm regards,

    The EmpathJot Team
    """)

st.markdown("---")

with st.sidebar:
    show_privacy_data_protection_footer()