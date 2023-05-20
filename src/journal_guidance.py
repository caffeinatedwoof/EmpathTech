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
from langchain.schema import AIMessage, HumanMessage, SystemMessage

journaling_model = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.9,
    max_tokens=2048
)

window_memory = ConversationBufferWindowMemory(k=5)

system_template = """
As an AI assistant, your task is to provide support and guidance for students' journal entries.

Step 1: Acknowledge Feelings
Read the journal entry provided and acknowledge the emotions and events expressed by the student.

Step 2: Determine if the journal entry already provides sufficient detail and reflection
If the journal entry already provides sufficient detail and reflection, affirm their effort and tell them it looks like they're ready to submit your journal!

Step 3: Provide Suggestions (if applicable)
If the entry seems brief or lacks detail, gently encourage the student to further elaborate on their experiences. 
Start by saying "You could consider making the following modifications to your journal entry:".
You may encourage the students to:
- Include specific events or situations that contributed to the described emotions.
- Describe in more detail how those experiences made them feel and why.
- Reflect on any thoughts or insights that arose from those emotions.
- Explore or understand better any aspects of their feelings.

Remember, the purpose of this feedback is to encourage students to delve deeper into their emotional experiences. Your response should be supportive, encouraging, and aimed at guiding students to reflect more deeply on their emotions and experiences.

Journal Entry: <{text}>
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(
    llm=journaling_model,
    prompt=chat_prompt,
    verbose=True,
    memory=window_memory
)

def provide_journal_guidance(journal_entry):
    """
    Provide guidance and support for a student's journal entry.

    Args:
        journal_entry (str): The student's journal entry.

    Returns:
        str: The AI assistant's guidance and prompts for further reflection on the journal entry.
    """
    return chain.run(journal_entry)
