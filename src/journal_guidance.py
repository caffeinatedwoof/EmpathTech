from langchain import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import SimpleSequentialChain
import streamlit as st

journaling_model = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    max_tokens=2048,
    openai_api_key=st.secrets.OPENAI_API_KEY
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
"""

primary_template = """
You are given the journal guidance output by a language model. Your task is to simplify it so that it's comprehensible for a 7 year-old with a very elementary command of the English language.

For a 7-year-old:
- Simplify the language by using shorter sentences and familiar words.
- Use a playful and friendly tone to engage their attention.
- Make sure the instructions are clear and easy to follow.

{journal_guidance_output}
"""

secondary_template = """
You are given the journal guidance output by a language model. Your task is to simplify it so that it's comprehensible for a 13 year-old with a very elementary command of the English language.

For a 13-year-old:
- Simplify the language to make it more accessible, but maintain a mature tone.
- Break down complex concepts into simpler terms without losing the essence.
- Provide clear and concise instructions that they can understand and follow.

{journal_guidance_output}
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = "Journal Entry: {text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(
    llm=journaling_model,
    prompt=chat_prompt,
    verbose=True,
    memory=window_memory
)

def provide_journal_guidance(journal_entry, level=None):
    """
    Provide guidance and support for a student's journal entry.

    Args:
        level (str): "primary" or "secondary"
        journal_entry (str): The student's journal entry.

    Returns:
        str: The AI assistant's guidance and prompts for further reflection on the journal entry.
    """
    # Chain 1
    chain_one = LLMChain(
        llm=journaling_model,
        prompt=chat_prompt,
        verbose=True,
        memory=window_memory
        )
    if not level:
        return chain_one.run(journal_entry)

    # Chain 2
    elif level == "primary":
        chain_two = LLMChain(
            llm=journaling_model,
            prompt=ChatPromptTemplate.from_template(primary_template)
        )
    elif level == "secondary":
        chain_two = LLMChain(
            llm=journaling_model,
            prompt=ChatPromptTemplate.from_template(secondary_template)
        )
    overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                             verbose=True)
    return overall_simple_chain.run(journal_entry)