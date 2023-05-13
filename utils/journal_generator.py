# Generates journal entries given a list of personas and prompts

import json
import datetime
from datetime import timedelta
import random
from langchain import OpenAI, LLMChain, PromptTemplate
from dotenv import load_dotenv
load_dotenv(dotenv_path = 'conf/.env', verbose = True)
import ast



STARTDATE = datetime.date(2023, 2, 2)
DURATION = 7*12
ARCHETYPES_DICT = {
    "Performing" : "Student with no behavioral issues and high academic performance",
    "Known Issues": "Student with known issues to the teacher (e.g. poor behavior in class, struggling academically)",
    "Issues Unknown": "Student who does not have outward manifestation of issues, but has some internal issues (e.g. dealing with bullying, body image issues, family challenges)",
}

with open('positive_prompts.json') as f:
    prompts_json = json.load(f)
    PROMPT_LIST = prompts_json['prompts']

with open('student_personas.json') as f:
    students_json = json.load(f)
    STUDENT_LIST = students_json['students']

    total_entries = 0
    for student in STUDENT_LIST:
        total_entries += int(student['journalEntries'])

    print(total_entries)
    print(len(STUDENT_LIST))


def date_randomizer(duration):
    start_date = STARTDATE
    end_date = start_date + timedelta(days=duration)

    random_date = start_date + (end_date - start_date) * random.random()
    print(random_date)
    return random_date


def datelist_generator(num_of_dates, duration):
    date_list = []
    for i in range(num_of_dates):
        date_list.append(date_randomizer(duration))
    date_list.sort()
    datestr_list = [date.strftime("%m/%d/%Y") for date in date_list]
    return datestr_list


def unique_prompt_list_generator(num_prompts):
    random_prompts = random.sample(PROMPT_LIST, num_prompts)
    return random_prompts


def entry_randomizer(total_entries, num_prompted):
    """ Generates a list of dates and assigns a unique prompt to each date up to prompted_entries_num and assigns the rest of the entries as freewriting """
    date_list = datelist_generator(total_entries, DURATION)
    prompt_list = unique_prompt_list_generator(num_prompted)
    formatted_prompt_list = [f"{prompt['title']}" for prompt in prompt_list]  # Did not include prompt desccription due to token limit
    freewriting_list = ["Freewriting" for i in range(total_entries - num_prompted)]
    formatted_prompt_list.extend(freewriting_list)
    random.shuffle(formatted_prompt_list)
    entries = dict(zip(date_list, formatted_prompt_list))
    return entries
    

def journal_prompt_maker(student):
    """ Generates a prompt with a custom list of journal entries for a student"""
    def load_LLM():
        """Logic for loading the chain you want to use should go here."""
        llm = OpenAI(temperature=0, max_tokens=3500)
        return llm

    persona = student['persona']
    persona_description = student['description']
    num_of_entries = int(student['journalEntries'])
    num_prompted_entries = int(student['promptedEntries'])
    archetype = ARCHETYPES_DICT[student['archetype']]
    entries = entry_randomizer(num_of_entries, num_prompted_entries)
    count = 0
    formatted_entries = []
    for entry in entries:
        count += 1
        formatted_entries.append(f'Entry #{count} {entry}:{entries[entry]}')

    formatted_entries = '\n'.join(formatted_entries)
    json_format = "{entry_date: '...'title: '...', entry: '...'}"
    template = """
    You are a Singaporean secondary school student with the following persona: {persona}:{persona_description}. You are a {archetype}. You wrote in a journaling app that allows your teacher to better understand you. If the title is Freewriting, it means you wrote about anything you wanted and you wrote about both good and bad events (if any). Otherwise, you wrote based on the topic given. Your teacher can read your journal so you did not include anything you didn't want your teacher to see.

    Generate JSON code for all the entries. Every entry should be unique. Please be realistic and not overly positive. Use "entry_date", "title", and "entry" as the JSON keys. Remember to write journal entries according to your persona. If it fits the persona, you are allowed to make grammatical mistakes and use Singlish.:
    {formatted_entries}
    """

    prompt = PromptTemplate(
    input_variables=["persona", "persona_description", "archetype", "formatted_entries"],
    template=template,)

    print(prompt)

    llm = load_LLM()

    final_prompt = prompt.format(persona=persona, persona_description=persona_description, archetype=archetype, formatted_entries=formatted_entries)
    response = llm(final_prompt)

    return response


def filename_formatter(student):
    filename = student['persona'].replace("The ", "").replace(" ", "_").lower()
    print(filename)
    return filename

def get_journal_entries(student):
    response = journal_prompt_maker(student)
    print(response)
    response = ast.literal_eval(response)
    response = {"entries" : response}
    filename = filename_formatter(student)
    with open(f'journals/{filename}.json', 'w') as f:
        json.dump(response, f)
        print(len(response))

    return response

# read json and print entries
def read_journal_entries(student):
    filename = filename_formatter(student)
    with open(f'journals/{filename}.json') as json_file:
        data = json.load(json_file)
        print(data['entries'])
        print(len(data['entries']))


for i in range(21, len(STUDENT_LIST)):
    get_journal_entries(STUDENT_LIST[i])