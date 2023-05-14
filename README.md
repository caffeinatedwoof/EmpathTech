# EmpathTech
EmpathTech is a platform that uses speech-to-text technology and language models to help students record their experiences and emotions, and provide teachers with meaningful insights and analysis. This repository contains the source code and documentation, including the ML/AI models, front-end interface, and backend architecture.


# About this branch
This branch is created for the UI development of EmpathTech platform which aims to provide the look and feel of the platform.

# Other notes:
- A secrets.toml is required in .streamlit folder indicating login credentials to backend MongoDB in order for the frontend to work properly.
- Occurrence of Pymongo.errors `SSL: CERTIFICATE_VERIFY_FAILED` error when connecting to MongoDB is due to the non-existence of pem file "https://letsencrypt.org/certs/lets-encrypt-r3.pem" in the OS which you are operating. This can be following the steps as suggested by the user: https://www.linkedin.com/pulse/ssl-certificateverifyfailed-while-python-tried-retrieve-sanjeev-kumar