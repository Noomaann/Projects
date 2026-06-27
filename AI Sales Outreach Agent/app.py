import streamlit as st
import requests

st.set_page_config(page_title="AI Outreach Agent", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4158D0 0%, #7240E4 45%, #C850C0 100%); min-height: 100vh; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #3B4FD0 0%, #5A38D4 50%, #8030C8 100%); padding: 20px; }
    h1, h2, h3, p, label, .stMarkdown { color: white !important; }
    .stExpander { background-color: rgba(255, 255, 255, 0.12) !important; border: 1px solid rgba(255, 255, 255, 0.25) !important; border-radius: 14px !important; backdrop-filter: blur(8px) !important; }
    .stButton > button { background: linear-gradient(90deg, #7240E4 0%, #C850C0 100%) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Lead Generation Agent")

st.sidebar.header("Add New Lead")

name = st.sidebar.text_input("Name", key="name_input")
email = st.sidebar.text_input("Email", key="email_input")
company = st.sidebar.text_input("Company", key="company_input")

if st.sidebar.button("Add Lead"):
    response = requests.post("http://127.0.0.1:8000/leads/", json={
        "name": st.session_state.name_input, 
        "email": st.session_state.email_input, 
        "company": st.session_state.company_input
    })
   

st.header("Your Prospect List")
try:
    leads = requests.get("http://127.0.0.1:8000/leads/").json()

    for lead in leads:
        with st.expander(f"👤 {lead['name']} | 🏢 {lead['company']}"):
            st.write(f"**Email:** {lead['email']}")
            
            if st.button(f"Generate Personalized Email", key=f"gen_{lead['id']}"):
                with st.spinner("AI is crafting your email..."):
                    email_res = requests.post(f"http://127.0.0.1:8000/leads/{lead['id']}/generate-email")
                    if email_res.status_code == 200:
                        st.session_state[f"email_{lead['id']}"] = email_res.json()["generated_email"]
                        st.rerun()
                    else:
                        st.error("Failed to generate email.")
            
            if f"email_{lead['id']}" in st.session_state:
                email_text = st.text_area("Generated Email (Edit before sending):", st.session_state[f"email_{lead['id']}"], height=200, key=f"text_{lead['id']}")
                
                if st.button("🚀 Send Email", key=f"send_{lead['id']}"):
                    with st.spinner("Sending email..."):
                        send_res = requests.post(
                            f"http://127.0.0.1:8000/leads/{lead['id']}/send-email",
                            json={"email_content": email_text}
                        )
                        if send_res.status_code == 200:
                            st.success("Email successfully sent! ✅")
                        else:
                            st.error(f"Failed to send: {send_res.text}")
except Exception as e:
    st.error("Could not connect to the backend.")