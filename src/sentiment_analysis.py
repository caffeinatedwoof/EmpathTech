import json
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

sentiment_analysis_engine = OpenAI(model_name='text-davinci-003',
                                   temperature=0,
                                   max_tokens=2048)

SENTIMENT_ANALYSIS_TEMPLATE = """
You will be provided with a student's journal entry delimited by <>. 
 
    Perform the following tasks: 
       a) Identify and create lists of all positive, neutral, and negative events described in the text 
       b) Generate an overall sentiment label for the text and provide a brief explanation for how you arrived at the answer. The sentiment label must either be negative, neutral or positive.
       c) Detect and flag any concerning events that may have been mentioned or alluded to in the entry, such as bullying or abuse. 
 
    The output should be in JSON format with keys 'sentiment', and 'events'. The 'sentiment' key should have sub-key 'label' and sub-key 'explanation'. The 'events' key should have sub-keys 'positive', 'neutral', 'negative', and 'concerning'. Each of these sub-keys should have sub-keys 'count' and 'list', where 'count' represents the number of events in the category and 'list' contains the text of each event. 

If something is listed as a concerning event, it should be listed as a negative event as well. 
 
    Journal Entry: <{entry}>
    """

sentiment_analysis_prompt = PromptTemplate(
    input_variables=["entry"],
    template=SENTIMENT_ANALYSIS_TEMPLATE,
)

chain = LLMChain(llm = sentiment_analysis_engine, prompt=sentiment_analysis_prompt)

def perform_sentiment_analysis(entry):
    """
    Perform sentiment analysis on a student's journal entry.

    Args:
        entry (str): The student's journal entry.

    Returns:
        dict: A dictionary containing sentiment analysis results with the keys 'sentiment' and 'events'.
              The 'sentiment' key has sub-keys 'score' and 'explanation'. The 'events' key has sub-keys
              'positive', 'neutral', 'negative', and 'concerning', each with sub-keys 'count' and 'list'.
    """
    return chain.run(entry)