#Helper functions to facilitate certain streamlit frontend implementation
from pathlib import Path
import os
import json
import streamlit as st
import toml
import dbhandler
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page

#CONFIG
data = toml.load(os.path.join('.streamlit','pages.toml'))

LOGIN_PAGE = data['main_page']['name']
ACCESS_DENY = data['accessed_denied']['name']


#@st.cache_resource
def connect_db():
    db = dbhandler.DBHandler()
    st.session_state.db = db
    return db


def hide_other_pages():
    """Helper function to hide page tabs(Main, Data protection, Privacy policy) which is seen on side navigation bar.

    This is a css workaround to hide them instead of actual removal of info from pages information of the app get_pages function as such removal would cause errors in routing back to main page(login) or other page required.

    Args:
        None
    Returns:
        None
    Raise:
        None
    """
    # Hide Main page, Data Protection and Privacy Policy and buggy Main page
    html_string = """
        <style>
            .css-lrlib li:nth-child(1), .css-1oe5cao li:nth-child(1) {
                display: None;
            }

            .css-lrlib li:nth-child(9), .css-1oe5cao li:nth-child(9) {
                display: None;
            }

            .css-lrlib li:nth-last-child(3), .css-lrlib li:nth-last-child(4) {
                display: None;
            }

            .css-1oe5cao li:nth-last-child(3), .css-1oe5cao li:nth-last-child(4) {
                display: None;
            }

            a[href^="/Main"] {
              display: None;
            }
        </style>
    """
    
    st.markdown(html_string, unsafe_allow_html=True)

    return None


def post_navbar_edit(name_string=None):
    """Helper function to add text to the top of sidebar.

    Args:
        string (str): String to parse.
    Returns:
        None
    Raise:
        None
    
    """
    if name_string:
        hello_string = f'{name_string}'
    
    else:
        hello_string = None

    html_string = f"""
    <style>
        [kind="primary"] {{
            background-color: #19A7CE;
            border: 0px;
            border-radius: 1.5rem;
        }}
        [kind="primary"]:hover {{
            background-color: #5B8FB9;
            border: 0px
        }}
        [kind="secondary"] {{
            background-color: #5B8FB9;
            color: #ffffff;
            border: 1px;
            border-radius: 1.5rem;
        }}
        [kind="secondary"]:hover {{
            background-color: #19A7CE;
            color: #ffffff;
            border: 1px
        }}
        [kind="secondary"]:active {{
            background-color: #19A7CE;
            color: #000000;
            border: 1px
        }}
        [kind="secondary"]:focus {{
            background-color: #19A7CE;
            color: #000000;
            border: 1px
        }}
        [data-testid="stSidebar"] {{
            padding: 0rem 1rem 1rem 1rem;
            font-size: 1.5rem;
            overflow: hidden;
        }}
        .css-lrlib, .css-1oe5cao {{
            padding-top: 1rem;
        }}

        ul {{
            font-size: 1rem;
            position: sticky;
            margin: auto;
        }}
    </style>
    """
    st.markdown(html_string, unsafe_allow_html=True)
    return None

def navbar_edit():
    """Helper function to add text to the top of sidebar.

    Args:
        None
    Returns:
        None
    Raise:
        None
    
    """
    html_string = """
    <style>
        [data-testid="stSidebar"] {
            padding: 0rem 1rem 1rem 1rem;
            font-size: 1.5rem;
        }
        [data-testid="stSidebarNav"]::before {
            content: "";
            display: inline;
        }
        .css-lrlib, .css-1oe5cao {
            padding-top: 1rem;
        }

        ul {
            font-size: 1rem;
            position: sticky;
            margin: auto;
        }
    </style>
    """
    
    st.markdown(html_string, unsafe_allow_html=True)

    return None

def adjust_filter_font():
    """Helper function to add text to the top of sidebar.

    Args:
        None
    Returns:
        None
    Raise:
        None
    
    """
    st.markdown(
        """
        <style>
            p {
                font-size: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    return None

def remove_top_space_canvas():
    """Helper function to remove excess space in canvas section of page.

    Args:
        None
    Returns:
        None
    Raise:
        None

    """
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem; 
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
        """, unsafe_allow_html=True
    )
    return None

def disable_sidebar():
    """Helper function that disable sidebar

    Args:
        None
    Returns:
        None
    Raise:
        None
    """
    no_sidebar_style = """
        <style>
            div[data-testid="collapsedControl"] {
                display: none
            }
        </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)
    return None

def add_space_param():
    """Function that add 2 line spaces.
    Args:
        None.
    Returns:
        None.
    Raise:
        None.
    """
    st.text("")
    st.text("")
    return None

# all pages request
def get_all_pages():
    """Function that retrieves all pages info by utilising streamlit's get_pages function and writes to a json file on such information if does not exist. Otherwise, it reads existing pages.json.

    Returns:
        dict: Dictionary with strings as keys, and dictionaries containing details about that page.
    """

    # Returns a dictionary with strings as keys, and dictionaries containing details about that page

    default_pages = get_pages(LOGIN_PAGE)

    pages_path = Path("pages.json")

    # To remove any old pages.json, especially for deveklopment where changes to naming or new/removal of existing file.
    #pages_path.unlink(missing_ok=False)
    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages

# clear all page but not login page
def clear_all_but_first_page():
    """Function that retrieves all pages info by utilising streamlit's get_pages function and writes to a json file on such information. Otherwise, it reads existing pages.json. This is called during the loading of page.

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)
    st.write(current_pages)

    if len(current_pages.keys()) == 1:
        return

    # Update to session state
    st.session_state.page_info = get_all_pages()

    # Extract current page information prior to removing all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()

    # Append only necessary page
    current_pages[key] = val

    # Send event change signal
    _on_pages_changed.send()
    return None

# show all pages
def update_current_pages():
    """This function updates current pages by comparing with known information
    """
    current_pages = get_pages(LOGIN_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()

# Hide default page
def hide_page(name, current_pages):
    """Function that hides the stated page name by deleting information on provided dictionary of navigatable pages based on the first instance info was found.

    Code adopted from https://discuss.streamlit.io/t/hide-show-pages-in-multipage-app-based-on-conditions/28642/5

    Args:
        name (str): Page name to hide
        current_pages (dict): Dictionary containing pages information based on some reference script path.

    Returns:
        dict: updated page info.
    """
    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            break
        else:
            pass

    _on_pages_changed.send()

    return current_pages

def hide_student_pages():
    """Function that hides pages related to student view, namely: error_access_denied, student_view_journal, student_create_journal

    Args:
        None

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)

    # Exclude main page as we need to do logout
    student_pages_name_list = ["Access_denied",
                               "View_past_journals",
                               "Create_journal",
                               "View_journal"
                               "Sentiment_analysis",
                               "Chatbot",
                               "About_Empathjot",
                               ]

    # Hide listed pages
    for pages in student_pages_name_list:
        current_pages = hide_page(pages, current_pages)
    
    # Workaround to hide main page tab without removing from current page
    hide_other_pages()
    _on_pages_changed.send()

def hide_teacher_pages():
    """Function that hides pages related to teacher view, namely: error_access_denied, teacher_dashboard, teacher_teaching_class, teacher_view_student_journal

    Args:
        None

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)
    # Hide listed pages
    # Exclude main page as we need to do logout
    teacher_pages_name_list = ["Access_denied",
                               "Dashboard_summary",
                               "Teaching_classes",
                               "View_student_journal",
                               "View_journal"
                               "Chatbot",
                               "Sentiment_analysis",
                               ]

    for pages in teacher_pages_name_list:
        current_pages = hide_page(pages, current_pages)

    _on_pages_changed.send()

    return None

def reset_session_state():
    """Function that resets streamlit session state involving username, logged_in state, role_id, user_full_name and form

    Args:
        None

    Returns:
        None
    """
    st.session_state.username = ''
    st.session_state.logged_in = False
    st.session_state.role_id = ''
    st.session_state.user_fullname = ''
    st.session_state.form = ''
    st.session_state.is_teacher = False
    return None

def error_page_redirect():
    """Function that offers redirect to access deny page when triggered in some situations as part of browsing flow.

    Args:
        None

    Returns:
        None
    """
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        update_current_pages()
        switch_page(ACCESS_DENY)

    return None

def hide_st_table_row_index():
    """Function to hide dataframe index row when display with st.table wrapper.
    Args:
        None

    Returns:
        None
    """
    hide_table_row_index = """
        <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
        </style>
        """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    return None

def hide_streamlit_footer():
    """Function to hide "Made with Streamlit" Footer display on webpage
    Args:
        None

    Returns:
        None
    """
    hide_streamlit_style = """
        <style>
        #MainMenu { 
            visibility: hidden;
        }
        footer { 
            visibility: hidden;
        }
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    return None

def show_privacy_data_protection_footer():
    """Function to show privacy and data protection footer links to privacy and data protection pages.
    Args:
        None

    Returns:
        None
    """
    
    data_policy_footer="""
        <style>
                .footer {
                    bottom: 0;
                    margin-left: 0rem;
                    text-align: center;
                    font-size: 0.9rem;
                }
                a {
                    line-height: 1em;
                    display: inline-block;
                    margin: 0.5rem;
                }
        </style>

        <div class="footer">
            <a href="./Data_protection" target="_blank">Data Protection Policy</a>
            <a href="./Privacy_policy" target="_blank">Privacy Policy</a>
        </div>
        """

    st.markdown(data_policy_footer, unsafe_allow_html=True)
    return None