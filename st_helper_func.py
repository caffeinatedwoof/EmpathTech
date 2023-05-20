#Helper functions to facilitate certain streamlit frontend implementation
from pathlib import Path
import os
import json
import streamlit as st
import toml
import dbhandler
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page

#CONFIG
data = toml.load(os.path.join('.streamlit','pages.toml'))
LOGIN_PAGE = data['login_path_name']['name']
ACCESS_DENY = data['accessed_denied']['name']


#@st.cache_resource
def connect_db():
    db = dbhandler.DBHandler()
    st.session_state.db = db
    return db

def navbar_edit():
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
            [data-testid="stSidebar"] {
                padding: 1rem 1rem 1rem 1rem;
                font-size: 3rem;
                position: sticky;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Welcome to EmpathTech Platform";
                display: inline;
            }

            ul {
                font-size: 2rem;
                position: sticky;
            }
        </style>
        
        """,
        unsafe_allow_html=True,
    )
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
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)
    return None

def gridbuilder_config_setup(df):
    """Helper function that specifies and construct a streamlit AgGrid for a dataframe with fixed settings for the purpose of displaying dataframe content and allowing interaction.

    Args:
        df (dataframe): 
            Dataframe of interest which gridbuilder is to be used on.
    Returns:
        streamlit_gridresponse object for display on streamlit UI 

    Raise:
        None
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5) #Add pagination
    gb.configure_default_column(selectable=False)
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple',
                            use_checkbox=True,
                            groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='FILTERED', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='streamlit', #Add theme color to the table
        enable_enterprise_modules=True,
        domLayout='autoHeight',
        #height=350, 
        width='100%',
        reload_data=False, # Dont reload on each interaction
    )

    #data = grid_response['data']
    #selected = grid_response['selected_rows'] 
    #df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

    return grid_response

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
        saved_default_pages = json.loads(pages_path.read_text(encoding='utf-8'), encoding='utf-8')
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4), encoding='utf-8')

    return saved_default_pages

# clear all page but not login page
def clear_all_but_first_page():
    """Function that retrieves all pages info by utilising streamlit's get_pages function and writes to a json file on such information. Otherwise, it reads existing pages.json. This is called during the loading of page.

    Returns:
        None
    """
    current_pages = get_pages(LOGIN_PAGE)

    if len(current_pages.keys()) == 1:
        return

    # Update to session state
    st.session_state.page_info = get_all_pages()

    # Extract current page information prior to removing all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
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

    student_pages_name_list = ["Access_denied",
                               'Login',
                               "View_past_journals",
                               "Create_journal"]

    # Hide listed pages
    for pages in student_pages_name_list:
        current_pages = hide_page(pages, current_pages)
    

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
    teacher_pages_name_list = ["Access_denied",
                               "Dashboard_summary",
                               "Login",
                               "Teaching_classes",
                               "View_student_journals"
                               ]

    for pages in teacher_pages_name_list:
        current_pages = hide_page(pages, current_pages)

    _on_pages_changed.send()

    return None

def reset_session_state():
    """Function that resets streamlit session state involving username, logged_in state, role_id, user_full_name and form

    Returns:
        None
    """
    st.session_state.username = ''
    st.session_state.logged_in = False
    st.session_state.role_id = ''
    st.session_state.user_fullname = ''
    st.session_state.form = ''
    return None

def display_logout_button():
    """Function that triggers display of logout function when session state for logged in is currently True, indicating actual log in.

    Args:
        None
    Returns:
        None
    """
    # Case when user is logged in
    if st.session_state.logged_in == True:
        logout = st.sidebar.button(label='Log Out', on_click=reset_session_state())
        if logout:
            update_current_pages()
            switch_page(LOGIN_PAGE)
    
    return None

def error_page_redirect():
    if 'logged_in' not in st.session_state or st.session_state.logged_in == False:
        update_current_pages()
        switch_page(ACCESS_DENY)

