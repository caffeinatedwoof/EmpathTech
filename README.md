# EmpathTech
EmpathTech is a platform that uses speech-to-text technology and language models to help students record their experiences and emotions, and provide teachers with meaningful insights and analysis. This repository contains the source code and documentation, including the ML/AI models, front-end interface, and backend architecture.


# About this branch
This branch is created for the purpose of UI/UX development of envisiioned EmpathTech platform prototype.

# Other notes:
- Delete pages.json before starting streamlit. This is to ensure a fresh page reference is used by streamlit, as well as script_path will be updated to your current directory of this cloned repo. For developers, this is particularly important if new pages(.py) are added to pages subdirectory
- A secrets.toml is required in .streamlit folder indicating login credentials to backend MongoDB in order for the frontend to work properly.
    - key values required:
        - MONGODB_PW
        - CONNECT_STR
        - OPENAI_API_KEY 
- For developers: Please note that streamlit sessions do not persist and gets reset so long an widget is added via function call(e.g logout)

# Fix for errors:
- Occurrence of Pymongo.errors `SSL: CERTIFICATE_VERIFY_FAILED` error when connecting to MongoDB is due to the non-existence of pem file "https://letsencrypt.org/certs/lets-encrypt-r3.pem" in the OS which you are operating. 
    - To resolve: This can be following the steps as suggested by the user: https://www.linkedin.com/pulse/ssl-certificateverifyfailed-while-python-tried-retrieve-sanjeev-kumar

- ERROR when installing chromadb library: Could not build wheels for hnswlib, which is required to install pyproject.toml-based projects (For Windows 11).
    - To resolve: You need to download https://visualstudio.microsoft.com/visual-cpp-build-tools/ first. Find MSVC v143 - VS 2022 C++ x64/x86 build tools (latest) - VS and Windows 11 SDK (10.0.22621.0)