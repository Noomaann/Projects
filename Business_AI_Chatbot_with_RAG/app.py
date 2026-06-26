import streamlit as st
import requests
import time

st.set_page_config(page_title="Business AI Chatbot", page_icon="🚀", layout="wide")
API_BASE_URL = "http://127.0.0.1:8000"


def apply_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        * { font-family: 'Inter', sans-serif; }

        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }

        [data-testid="stFileUploaderFile"] { display: none !important; }
        [data-testid="stUploadedFile"] { display: none !important; }


        [data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,0.04) !important;
            border: 2px dashed rgba(99, 179, 237, 0.5) !important;
            border-radius: 14px !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #63b3ed !important;
            background: rgba(99, 179, 237, 0.08) !important;
        }
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] p,
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] div {
            color: #a0aec0 !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border: none !important;
            border-radius: 8px !important;
            color: white !important;
        }
        [data-testid="stFileUploaderDropzone"] button p,
        [data-testid="stFileUploaderDropzone"] button span { color: white !important; }

        [data-testid="stSidebar"] button:not([data-testid="stFileUploaderDropzone"] button) {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        [data-testid="stSidebar"] button:not([data-testid="stFileUploaderDropzone"] button):hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        }
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div { color: white !important; }

        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarHeader"] {
            opacity: 1 !important;
            visibility: visible !important;
        }

        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

        [data-testid="stChatMessage"] {
            background: rgba(255,255,255,0.05) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 16px !important;
            padding: 16px !important;
            margin-bottom: 12px !important;
        }
        [data-testid="stChatMessage"] p { color: #e2e8f0 !important; }

        [data-testid="stBottom"] { background: transparent !important; }
        [data-testid="stBottom"] > div { background: transparent !important; }

        [data-testid="stChatInput"] {
            background: rgba(20, 20, 40, 0.7) !important; /* Dark glass effect */
            backdrop-filter: blur(15px) !important;
            border: 1.5px solid rgba(102, 126, 234, 0.5) !important;
            border-radius: 20px !important;
            padding: 5px 15px !important;
            margin-bottom: 25px !important; /* Push slightly up */
            box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        }

        [data-testid="stChatInput"] div {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        [data-testid="stChatInput"] textarea {
            background-color: transparent !important;
            color: #ffffff !important;
            caret-color: #ffffff !important; /* Blinking cursor color */
            font-size: 18px !important; /* ── FONT SIZE BORO KORA HOYECHE ── */
            min-height: 50px !important; /* Make it thicker */
            padding-top: 14px !important;
            padding-bottom: 14px !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: rgba(255,255,255,0.6) !important;
        }
        
        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border-radius: 50% !important;
            width: 42px !important;
            height: 42px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s ease !important;
            margin-top: 5px !important;
        }
        [data-testid="stChatInput"] button:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.6) !important;
        }
        [data-testid="stChatInput"] button svg {
            fill: white !important;
            color: white !important;
        }

        [data-testid="stAlert"] { border-radius: 12px !important; border: none !important; }

        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        header[data-testid="stHeader"] { background: transparent !important; }
        
        header[data-testid="stHeader"] *,
        [data-testid="collapsedControl"] * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
        ::-webkit-scrollbar-thumb { background: rgba(102,126,234,0.5); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style="text-align:center; padding: 30px 0 10px 0;">
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            padding: 12px 28px;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        ">
            <span style="font-size: 28px;">🚀</span>
            <span style="
                font-size: 28px;
                font-weight: 900;
                color: white;
                margin-left: 10px;
                letter-spacing: -0.5px;
            ">Business AI Chatbot</span>
        </div>
        <p style="
            color: rgba(255,255,255,0.5);
            font-size: 15px;
            font-weight: 500;
            margin: 0;
        ">Powered by RAG · LangChain · Gemini</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        
        st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <div style="
                background: linear-gradient(135deg, #667eea22, #764ba222);
                border: 1px solid rgba(102,126,234,0.3);
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 8px;
            ">
                <div style="font-size:18px; font-weight:800; color:#e2e8f0; margin-bottom:6px;">
                    ⚙️ Data Dashboard
                </div>
                <div style="font-size:13px; color:#a0aec0; line-height:1.5;">
                    Upload your business PDF documents to train the AI assistant.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

     
        st.markdown("""
        <div style="
            font-size: 12px;
            font-weight: 600;
            color: #a0aec0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        ">📎 Choose a PDF file</div>
        """, unsafe_allow_html=True)

    
        uploaded_file = st.file_uploader(
            label="upload",
            type=["pdf"],
            label_visibility="collapsed"
        )

     
        if uploaded_file:
            file_size_kb = round(len(uploaded_file.getvalue()) / 1024, 1)
            fname = uploaded_file.name
            display_name = fname if len(fname) <= 30 else fname[:27] + "..."

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1a365d, #2a4a7f);
                border: 1.5px solid #667eea;
                border-radius: 12px;
                padding: 12px 14px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 4px 15px rgba(102,126,234,0.25);
            ">
                <div style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 8px;
                    width: 36px; height: 36px;
                    display: flex; align-items: center; justify-content: center;
                    flex-shrink: 0; font-size: 18px;
                ">📄</div>
                <div style="overflow: hidden;">
                    <div style="
                        color: #ffffff;
                        font-weight: 700;
                        font-size: 13px;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    " title="{fname}">{display_name}</div>
                    <div style="color: #90cdf4; font-size: 11px; margin-top: 2px;">
                        {file_size_kb} KB · PDF
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("⏳ Indexing document..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    res = requests.post(f"{API_BASE_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success("✅ Document indexed successfully!")
                    else:
                        st.error("❌ Failed to process document.")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend server.")

        st.markdown("<div style='margin: 20px 0 10px 0;'></div>", unsafe_allow_html=True)
        st.divider()

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_empty_state():
    st.markdown("""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 20px;
        opacity: 0.7;
    ">
        <div style="font-size: 64px; margin-bottom: 16px;">💬</div>
        <div style="
            font-size: 22px;
            font-weight: 700;
            color: rgba(255,255,255,0.7);
            margin-bottom: 8px;
        ">Start a conversation</div>
        <div style="
            font-size: 14px;
            color: rgba(255,255,255,0.35);
            text-align: center;
            max-width: 320px;
            line-height: 1.6;
        ">
            Upload a PDF from the sidebar, then ask anything about your document below.
        </div>
    </div>
    """, unsafe_allow_html=True)


apply_styles()
render_header()
render_sidebar()


if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.messages:
    render_empty_state()
else:
    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])


user_query = st.chat_input("Ask anything about your documents...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Searching documents..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"question": user_query}
                )
                if response.status_code == 200:
                    bot_reply = response.json().get("answer", "No response.")
                else:
                    bot_reply = "⚠️ Server error occurred. Please try again."
            except requests.exceptions.ConnectionError:
                bot_reply = "⚠️ Backend server unreachable. Ensure FastAPI is running."

        placeholder = st.empty()
        typed = ""
        for word in bot_reply.split():
            typed += word + " "
            placeholder.markdown(typed + "▌")
            time.sleep(0.03)
        placeholder.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})