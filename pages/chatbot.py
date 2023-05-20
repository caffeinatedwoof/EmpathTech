from src.journal_utils import is_journal_entry
from src.journal_guidance import provide_journal_guidance
import streamlit as st
from streamlit_chat import message

def generate_chat():
    for i in range(0, len(st.session_state["generated"]) - 1, 1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
        message(st.session_state["generated"][i], key=str(i))
        

st.title("Journal Guidance")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

if "sources" not in st.session_state:
    st.session_state["sources"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    placeholder = st.empty()

else:
    placeholder = st.empty()
    # with placeholder.container():
    #     if st.session_state["generated"]:
    #         generate_chat()

text_input = st.text_area("Type your journal entry here!")

# Get feedback
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    if st.button("Get Feedback"):
        with st.spinner('Checking entry...'):
            check = is_journal_entry(text_input)

        if check['journal_entry']:
            with st.spinner('Generating feedback...'):
                output = provide_journal_guidance(text_input)
        else:
            # output = check['explanation']
            output = "Please enter a valid journal entry."

        print(output)
        print("type of output", type(output))

        st.session_state['chat_history'].append((text_input, output))
        st.session_state.past.append(text_input)
        st.session_state.generated.append(output)

with col2:
    if st.button("Submit Journal"):
        # Submit journal for sentiment analysis
        pass

with placeholder.container():
    if st.session_state["generated"]:
        generate_chat()
