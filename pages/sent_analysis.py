import streamlit as st

db = st.session_state.db
username = st.session_state.username
current_student = db.get_student(username=username)


all_summaries = db.get_all_summaries(current_student['_id'])
st.title(f"{current_student['name']}'s Sentiment Analysis")
for summary in all_summaries:
    st.markdown(f"The sentiment score for journal with id {summary['journal_id']} is {summary['sentiment']['score']}")
    st.markdown(f"Reasons: {summary['sentiment']['explanation']}")
    st.markdown(f"""
    Positive: {summary['events']['positive']}

    Negative: {summary['events']['negative']}

    Neutral: {summary['events']['neutral']}

    Concerning: {summary['events']['concerning']}

    """)
    st.divider()
    print(summary)
