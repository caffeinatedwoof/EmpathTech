import streamlit as st
from langchain import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

st.title("Mental Health Check-in")
messages = []

def run_conversation():
    chat = ChatOpenAI(model_name = 'gpt-3.5-turbo',
                      temperature=0.5,
                      max_tokens=256)
    window_memory = ConversationBufferWindowMemory(k=5)
    system_template =  """
    You are a mental health professional who works with adolescents aged 12-17 in Singapore. 
    You will perform a mental health check-in with your client. 
    You will always refer to yourself as "Mental Health Buddy". 
    If your client gives you incomprehensible responses in the context of a mental health check-in, ask clarifying questions in a professional manner. 
    """
    system_message_prompt=SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{text}"
    human_message_prompt=HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    window_memory = ConversationBufferWindowMemory(k=5)
    chain = LLMChain(llm=chat, 
                 prompt=chat_prompt,
                 verbose=True,
                 memory=window_memory)
    user_input = st.text_input("Your message:", "")
    if st.button("Send"):
        response = chain.run(text = user_input)
        messages.append(user_input)
        messages.append(response)
        conversation_history = "\n".join(messages)
        st.text_area("Conversation:", conversation_history)
run_conversation()
