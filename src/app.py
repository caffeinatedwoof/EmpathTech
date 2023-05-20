import streamlit as st
from journal_utils import is_journal_entry
from journal_guidance import provide_journal_guidance
from sentiment_analysis import perform_sentiment_analysis

def main():
    st.title("Journal Entry")

    # Text input
    text_input = st.text_area("Type your journal entry here!")

    # Get feedback
    if st.button("Get feedback"):
        check = is_journal_entry(text_input)
        if check['journal_entry']:
            st.write(provide_journal_guidance(text_input))
        else:
            st.write(check['explanation'])

    # Submit button
    if st.button("Submit"):
        # Process the submitted text
        ## Return sentiment analysis output
        st.write("Your journal entry has been submitted!")

if __name__ == "__main__":
    main()
