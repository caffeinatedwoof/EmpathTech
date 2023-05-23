from dbhandler import DBHandler

from langchain.prompts.chat import (ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate,)
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

def filter_journal_entries(student_name, start_date, end_date):

    db_handler = DBHandler()

    # Initialize empty lists to store all journal entries and metadatas
    metadatas = []
    journal_entries = []
    
    # Initialize student attributes
    student = db_handler.get_student(student_name)
    student_id = student['_id']  # Name of the student
    class_ = student['class'] # Student's class 

    journals = db_handler.get_journal_entries(student_id)

    # Iterate over all journal entries for the student
    for journal in journals:
        journal_id = journal['_id'] # ID of the journal entry
        journal_title = journal['title']
        journal_content = journal['content']
        date = journal['date'].date()

        # Check if the journal entry falls within the date range
        if start_date <= date <= end_date:
            # Append to our journal entries list
            metadatas.append({
                'student_id': str(student_id),
                'student_name': student_name,
                'class': class_,
                'source': str(journal_id),
                'journal_title': journal_title,
                'journal_date': str(date)
            })

            # Append content only
            journal_entries.append(journal_content)

    return journal_entries, metadatas

def convert_journal_entries_to_vectors(journal_entries, metadatas):
    # Instantiate OpenAIEmbeddings
    openai_embeddings = OpenAIEmbeddings(model='gpt-3.5-turbo')
    vector_store = Chroma.from_texts(journal_entries, 
                                 embedding=openai_embeddings, 
                                 metadatas=metadatas)
    return vector_store

def process_query(question, vector_store, student_name):
    system_template = f"The student's name is {student_name} All the documents below are {student_name}'s journal entries. any question that asks abut student, or {student_name}, is referring to {student_name}" + """Use the following pieces of context to answer the user's question.\
    No matter what the question is, you should always answer it in the context of the journal entries provided.\
    If possible, point the user to the journal entry where you obtained the information from. \
    Even if the question does not end in a question mark, you should still answer it as if it were a question.\
    If the question is not related to the student in question, reply "Please ask me questions about the student in question".\
    ----------------
    {summaries}"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    language_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) 

    chain_type_kwargs = {"prompt": prompt}

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=language_model,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_type="similarity"),
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )

    result = chain(question)

    return result

def ss_query(student_name, start_date, end_date, question):
    """Function that takes in students credentials of interest and search query and conducts a semantic search using langchain API

    Args:
        student_name (str): Name of student
        start_date (str): Start date
        end_date (str): End date
        question (str): Question to assist in query

    Returns:
        dict : Dictionary of response
    """
    journal_entries, metadatas = filter_journal_entries(student_name,
                                                        start_date,
                                                        end_date)
    vector_store = convert_journal_entries_to_vectors(journal_entries, metadatas)
    return process_query(question, vector_store, student_name)
    


