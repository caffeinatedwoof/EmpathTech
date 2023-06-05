import streamlit as st
import os
import sys
from PIL import Image
from datetime import datetime, timedelta
from st_helper_func import connect_db, show_privacy_data_protection_footer
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from dbhandler import DBHandler

if "db" not in st.session_state:
    db = connect_db()
else:
    db = st.session_state.db

LVL_1_THRESHOLD = 1
LVL_2_THRESHOLD = 3
LVL_3_THRESHOLD = 8
LVL_4_THRESHOLD = 15

LVL_THRESHOLD = {
    "LVL_1": LVL_1_THRESHOLD,
    "LVL_2": LVL_2_THRESHOLD,
    "LVL_3": LVL_3_THRESHOLD,
    "LVL_4": LVL_4_THRESHOLD,
}

class journalPlant:
    def __init__(self, student_id, plant="default"):
        self.student_id = student_id
        self.entries = self._count_journals()
        self.level = self._calculate_lvl(self.entries)
        self.max_level = 4
        self.plant = plant
        

    def _calculate_lvl(self, entries):
        if entries >= LVL_4_THRESHOLD:
            return 4
        elif entries >= LVL_3_THRESHOLD:
            return 3
        elif entries >= LVL_2_THRESHOLD:
            return 2
        elif entries >= LVL_1_THRESHOLD:
            return 1
        else:
            return 0

    def get_level(self):
        return self.level

    def get_plant(self):
        return self.plant

    def set_level(self, level):
        self.level = level

    def set_plant(self, plant):
        self.plant = plant

    def _count_journals(self):
        journals = db.get_journal_entries(self.student_id)
        journal_list = [journal for journal in journals if journal['private'] == False]
        return len(journal_list)
    
    def _count_recent_journals(self):
        # find date two weeks ago from today
        today = datetime.now()
        two_weeks_ago = today - timedelta(days=14)
        journals = db.get_journal_entries(self.student_id)
        journal_list = [journal for journal in journals if journal['private'] == False and journal['date'] > two_weeks_ago]
        return len(journal_list)

    def show(self):
        current_plant = os.path.join(current, "images", f"plant{self.level}.png")
        image = Image.open(current_plant)
        st.image(image)
        if self.level < self.max_level:
            percentage_completion = self.entries/LVL_THRESHOLD[f"LVL_{self.level+1}"]*100
            progress_bar_label = f"{self.entries}/{LVL_THRESHOLD[f'LVL_{self.level+1}']}"
        else:
            percentage_completion = 100
            progress_bar_label = f'{LVL_THRESHOLD[f"LVL_{self.max_level}"]}/{LVL_THRESHOLD[f"LVL_{self.max_level}"]}'
    
        with open(os.path.join(current, 'gamification.css')) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
            st.markdown(f"""
                <div class="w3-light-grey w3-round-xlarge">
                <div class="w3-blue w3-round-xlarge" style='width:{percentage_completion}%'><p style='text-align:center'>{progress_bar_label}</p></div></div><h2 style='text-align:center'>Level {self.level} Plant</h2>
                <p style='text-align:center'>Total Entries: {self.entries}<br>
                Recent Entries: {self._count_recent_journals()}<br>
                Write more to grow your plant!</p> """, unsafe_allow_html=True)
        
def gamified_sidebar(student_id):
    
    with st.sidebar:
        sb_col1, sb_col2, sb_col3 = st.columns([0.1,1,0.1])
        with sb_col1:
            st.markdown(" ")
        with sb_col2:
            plant = journalPlant(student_id)
            plant.show()
        with sb_col3:
            st.markdown(" ")