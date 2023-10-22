<div align="center">
  <h1>EmpathJot</h1>
</div>

## About

This repository is developed by a like-minded team (EmpathTech) of people who participated and were awarded 2nd-runner-up in HackSingapore 2023 (organised by AngelHack) Digital Empowerment theme with the focus: "Optimising the use of digital technologies to create opportunities for underserved individuals so that they can better participate and express themselves".

Team members:

- Chia Wei Han
- Law Shu Ying
- Ong Zhi Xuan
- Quek Zhi Qiang


## The problem statement

There has been a growing concern pertaining to youth mental-well being nowadays which is evidenced by newsreport published on various news outlet such as the report from Singapore's Straits Time article: [About 1 in 3 young people in Singapore has mental health symptoms: Study](https://www.straitstimes.com/singapore/about-1-in-3-youths-in-singapore-has-mental-health-symptoms-study) and a research article from NUS Medicine, [NUS Youth Epidemiology and Resilience Study (2023)](https://medicine.nus.edu.sg/news/building-resilience-is-key-to-good-mental-health-nus-youth-epidemiology-and-resilience-study). If left unchecked, it may result in a lost productivity as a result of anxiety and depression, which is estimated to cost Singapore 2.9% of its GDP, or close to $26bn annually. [Prevalence and economic burden of depression and anxiety symptoms among Singaporean adults: results from a 2022 web panel. BMC Psychiatry 23, 104 (2023)](https://doi.org/10.1186/s12888-023-04581-7)

EmpathTech's journaling tool, EmpathJot, leverages Large Language Models to empower teachers and students in classroom settings, offering a guided journaling experience, sentiment analysis for tracking well-being, a teacher dashboard for sentiment scores, natural language querying, and guardrails for identifying concerning events.

All the source code and documentation, including the ML/AI models, front-end interface, and backend architecture are contained in the repository.

---

The link to the deployed Streamlit app is: https://shuylaw-empathtech-main-xvm9by.streamlit.app/

---
## Video Demo

---

https://github.com/caffeinatedwoof/EmpathTech/assets/20638685/c19b397d-d971-463b-aa9c-c2683758339f

---

## Usage

Log-in credentials for both teacher-user and student-user are provided in the submission form for HackSingapore 2023 under the Project Description.

Please note that our current Minimum Viable Product (MVP) version of the app may experience technical issues if multiple users attempt to log in simultaneously. This can lead to unexpected behavior and potential disruptions in the app's functionality.

To ensure a smooth and optimal experience, we kindly request users not to log in with multiple accounts at the same time during the demo period. This will help us avoid any unintended conflicts and maintain the integrity of the app's performance.

### Teacher's Interface ###

Log in using the teacher's credentials to access the following functions:

1. Dashboard Summary, including sentiment scores, guardrails (flagging concerning events) and semantic search over student's journal entries
2. View Student Journal, including emotion history and teacher feedback on individual journal entries

### Student's Interface ###

Log in using the student's credentials to access the following functions:

1. Create Journal, including use of AI Journaling Assistant
2. View Past Journals

---

## Other notes ##

- Delete pages.json before starting streamlit. This is to ensure a fresh page reference is used by streamlit, as well as script_path will be updated to your current directory of this cloned repo. For developers, this is particularly important if new pages(.py) are added to pages subdirectory
- A secrets.toml is required in .streamlit folder indicating login credentials to backend MongoDB in order for the frontend to work properly.
    - key values required:
        - MONGODB_PW
        - CONNECT_STR
        - OPENAI_API_KEY 
- For developers: Please note that streamlit sessions do not persist and gets reset so long an widget is added via function call(e.g logout)

---

## Fix for errors ##

- Occurrence of Pymongo.errors `SSL: CERTIFICATE_VERIFY_FAILED` error when connecting to MongoDB is due to the non-existence of pem file "https://letsencrypt.org/certs/lets-encrypt-r3.pem" in the OS which you are operating. 
- To resolve: This can be following the steps as suggested by the user: https://www.linkedin.com/pulse/ssl-certificateverifyfailed-while-python-tried-retrieve-sanjeev-kumar

- ERROR when installing chromadb library: Could not build wheels for hnswlib, which is required to install pyproject.toml-based projects (For Windows 11).
- To resolve: You need to download https://visualstudio.microsoft.com/visual-cpp-build-tools/ first. Find MSVC v143 - VS 2022 C++ x64/x86 build tools (latest) - VS and Windows 11 SDK (10.0.22621.0)
