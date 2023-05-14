#Helper functions to facilitate certain streamlit frontend implementation
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid

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