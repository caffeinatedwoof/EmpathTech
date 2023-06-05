import streamlit as st
from st_helper_func import remove_top_space_canvas, disable_sidebar, hide_student_pages, hide_streamlit_footer

# Layout config 
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

remove_top_space_canvas()
disable_sidebar()
hide_student_pages()
hide_streamlit_footer()
# Ref: What’s the Difference Between a Data Protection Policy and a Privacy Policy? A privacy policy is a document that explains to customers how an organization collects and processes their data. It is made available to the public by organizations required to comply with privacy regulations. A data protection policy is an internal document created to establish data protection policies within the organization. It is made available to employees, as well as third parties, responsible for handling or processing sensitive data.

# Link: https://www.linkedin.com/pulse/difference-between-data-protection-policy-privacy-beverly-davis

_, colT2, _ = st.columns(3)

with colT2:
    st.title("PRIVACY POLICY")
st.markdown("----")

st.header("DEFINITIONS & INTERPRETATIONS")
st.markdown("""
    - "Admin", "We" or "Us" means the EmpathJot entity (or any person acting on behalf of and with the authority of the EmpathJot) who is providing the EmpathJot platform for journal entries, submissions and comments.

    - "Students" means the entity(ies) enrolled as a students of an institution.

    - "Teacher-In-Charge" means the entity(ies) serving or contracted as a member staff of an institution and serving in the capacity as the form-teacher or subject-teacher for "Students". 
     
    - "Users" means authorised entity(ties) belonging to either "Students" or "Teacher-In-Charge" of an instituion using EmpathJot Journaling platform.
""")
st.markdown("----")           

st.header("INTRODUCTION")
st.markdown("""
    EmpathJot ("we" or "us") takes the privacy of Users information seriously. This Privacy Policy applies to the https://shuylaw-empathtech-main-xvm9by.streamlit.app/ website (the "Website" or "Services") and governs data collection, processing and usage in compliance with the Personal Data Protection Act 2012 (No. 26 of 2012) of Singapore ("PDPA").
     
    By using the Website, you agree/consent to the data practices described in this statement.
""")
st.markdown("----")

st.header("Information Collected from All Visitors to our Website")
st.markdown("""
    We will obtain personal data about you when you visit us. When you visit us, we may monitor the use of this Website through the use of cookies and similar tracking devices. For example, we may monitor the number of times you visit our Website or which pages you go to. This information helps us to build a profile of our users. Some of this data will be aggregated or statistical, which means that we will not be able to identify you individually.

    This Privacy Policy applies to all visitors to our Website.
""")
st.markdown("----")

st.header("Additional Personal Information that May be Collected")
st.markdown("""
    EmpathJot may collect and process:

    1. Personally identifiable information, such as:
        1. Users e-mail address and name, when you contact us;
        2. Details contained in the relevant document that were captured by  when you use our Services. These details may include your name, information on Teacher-In-Charge teaching class and their Students (“Personal Information”)
    2. Information about your computer hardware and software when you use our Website. The information can include: your IP address, browser type, domain names, access times and referring website addresses. This information is used by FWP for the operation of the Services, to maintain quality of the Services, and to provide general statistics regarding use of the Website.
""")
st.markdown("----")

st.header("Use of Personal Information")
st.markdown("""
    EmpathJot uses the collected information:

    1. To operate the Website and deliver the Services;
    2. To process, and where necessary, respond to your submitted contents and responses;
    3. To monitor, improve and administer the Website or Services, and to provide general statistics regarding user of the Website;
    4. To update you on changes to the Website and Services.
""")
st.markdown("----")

st.header("Non-disclosure of Personal Information")
st.markdown("""
    EmpathJot does not sell, rent, lease, or release your Personal Information to third parties. EmpathJot may, from time to time, contact you on behalf of external business partners about a particular offering that may be of interest to you. In those cases, your unique Personal Information is not transferred to the third party without your explicit consent. In addition, EmpathJot may share data with trusted partners to help us perform statistical analysis, send you email or provide customer support. All such third parties are prohibited from using your personal information except to provide these services to EmpathJot, and they are required to maintain the confidentiality of your Personal Information.
""")
st.markdown("----")

st.header("Disclosure of Personal Information and Contents posted")
st.markdown("""
    EmpathJot will disclose or share your Personal Information and contents posted, without notice, only if required to do so by law or in the good faith belief that any such action is necessary to: 
        (a) comply with any legal requirements or comply with legal process served on the Website;
        (b) protect and defend the rights or property of EmpathJot; and
        (c) act under exigent circumstances to protect the personal safety of users of Webite, or the general public.

    We may disclose your personal information to third parties: (a) in the event that we sell or buy any business or assets, in which case we may disclose your personal data to the prospective seller or buyer of such business or assets; and (b) if singaporelegaladvice.com or substantially all of its assets are acquired by a third party, in which case personal data held by it about its customers will be one of the transferred assets.
""")
st.markdown("----")

st.header("Use of Cookies")
st.markdown("""
    The Website uses “cookies” to help you personalize your online experience. A cookie is a text file that is placed on your hard drive by a web page server. Cookies cannot be used to run programs or deliver viruses to your computer. Cookies are uniquely assigned to you, and can only be read by a web server in the domain that issued the cookie to you.

    Cookies on the Website may be used to ensure a smooth user experience, perform analytics, and for showing relevant advertisements. Please note that third parties (such as analytics software) may also use cookies, over which we have no control. These cookies are likely to be analytical/performance cookies or targeting cookies. The Website uses Google Analytics. Please refer to http://www.google.com/policies/privacy/partners to find out more about how Google uses data when you use our website and how to control the information sent to Google.

    Most Web browsers automatically accept cookies, but you can usually modify your browser setting to decline cookies if you prefer. If you choose to decline cookies, you may not be able to access all or parts of our Website or to fully experience the interactive features of the FWP services or websites you visit.
""")
st.markdown("----")

st.header("Security Of Your Personal Information")
st.markdown("""
    We strive to maintain the safety of your Personal Information. Any payment transactions will be encrypted using SSL technology. Unfortunately, no internet-based service is completely secure. Although we will do our best to protect your personal data, we cannot guarantee the security of your data transmitted to our site; any transmission is at your own risk. Once we have received your information, we will use strict procedures and security features to try to prevent unauthorised access.
""")
st.markdown("----")

st.header("Access to, Updating, and Non-Use of Your Personal Information")
st.markdown("""
    Subject to the exceptions referred to in section 21(2) of PDPA, you have the right to request a copy of the information that we hold about you. If you would like a copy of some or all of your personal information, please send an email to admin@singaporelegaladvice.com. We may make a small charge for this service.

    We want to ensure that your Personal Information is accurate and up to date. If any of the information that you have provided to FWP changes, for example if you change your email address, name or contact number, please let us know the correct details by sending an email to admin@singaporelegaladvice.com. You may ask us, or we may ask you, to correct information you or we think is inaccurate, and you may also ask us to remove information which is inaccurate.

    You have the right to ask us not to collect, use, process, or disclose your Personal Information in any of the manner described herein. We will usually inform you (before collecting your Personal Information) if we intend to use your Personal Information for such purposes or if we intend to disclose your Personal Information to any third party for such purposes. You can give us notice of your intention to halt the collection, use, processing, or disclosure of your Personal Information at any time by contacting the institution Data Protection Officer (DPO) at:
    
    DPO: TBC
    Address: TBC
    Email Address: TBC
    Contact number: TBC
""")   
st.markdown("----")

st.header("Links to Other Websites")
st.markdown("""
    Our Website may contain links to other websites. This Privacy Policy only applies to this website so when you link to other websites you should read their own privacy policies.
""")
st.markdown("---")

st.header("Changes To This Statement")
st.markdown("""
    EmpathJot will occasionally update this Privacy Policy to reflect customer feedback. EmpathJot encourages you to periodically review this Privacy Policy to be informed of how FWP is protecting your information.
""")    
st.markdown("---")

st.header("Contact Information")
st.markdown("""
    EmpathJot welcomes your comments regarding this Privacy Policy. If you believe that https://shuylaw-empathtech-main-xvm9by.streamlit.app/ has not adhered to this Privacy Policy, please contact the institution Data Protection Officer (DPO) at:
    
    - DPO: TBC

    - Address: TBC

    - Email Address: TBC

    - Contact number: TBC
""")    
st.markdown("---")