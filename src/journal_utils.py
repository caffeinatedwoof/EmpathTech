"""
journal_utils

This module provides utility functions related to journal entries, including determining if a given text is a genuine student's journal entry.

Functions:
- is_journal_entry(entry): Determines if the given text is a journal entry.
"""
import json

from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import streamlit as st

language_model = OpenAI(model_name='gpt-3.5-turbo',
                        temperature=0,
                        max_tokens=2048,
                        openai_api_key=st.secrets.OPENAI_API_KEY)

IS_JOURNAL_ENTRY_PROMPT_TEMPLATE = """
Please determine if the text is a genuine student's journal entry or not.
Provide a brief explanation for your answer.

Note: This app is intended for personal reflection and growth purposes only and should not be used to complete homework or assignments.

Output should be in JSON format with keys 'journal_entry' and 'explanation'. 
'journal_entry' should contain a boolean of whether the given text is a journal entry or not.
'explanation' should contain text explaining why the text was determined to be a journal entry or not.

Text: <{entry}>
"""

is_journal_entry_prompt = PromptTemplate(
    input_variables=["entry"],
    template=IS_JOURNAL_ENTRY_PROMPT_TEMPLATE,
)

chain = LLMChain(llm = language_model, prompt=is_journal_entry_prompt)

def clean_llm_output(llm_output):
    if "output:" in llm_output:
        llm_output = llm_output.replace("output:", "")
    elif "Output:" in llm_output:
        llm_output = llm_output.replace("Output:", "")

    return llm_output


def is_journal_entry(entry):
    """
    Determine if the given text is a genuine student's journal entry.

    Args:
        entry (str): The text to evaluate.

    Returns:
        dict: A dictionary with the following key-value pairs:
            - 'journal_entry' (bool): True if the text is a journal entry, False otherwise.
            - 'explanation' (str): Brief explanation for the language model's answer.
    """
    llm_output = chain.run(entry)
    print("original journal check output", llm_output)
    llm_output = clean_llm_output(llm_output)
    print("cleaned journal check output:", llm_output)
    result_dict = json.loads(llm_output)
    return result_dict
