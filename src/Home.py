import streamlit as st
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from Tour_Guide_Bot.run_crew import run_history_crew


avatar = os.path.join("Tour_Guide_Bot", "icons", "eye-of-horus.png")
st.set_page_config(page_title="History Tour Guide", page_icon=avatar, layout="centered")

st.title("𓀀 Egyptian AI Tourist Guide 𓀀")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Hieroglyph Translator", use_container_width=True):
        st.switch_page("pages/Hieroglyph Translator.py") 

with col2:
    if st.button("Artifact Recognition", use_container_width=True):
        st.switch_page("pages/Artifact Recognition.py")
with col3:
    if st.button("Artifact Restoration", use_container_width=True):
        st.switch_page("pages/Artifact Restoration.py")


st.markdown("""
    <style>
    .stApp {
        background-color: #e6e3d2;
    }
    h1 {
    color: #8B7355 !important;
    text-align: center;
    margin-bottom: 1.5rem;
    }
            
    [data-testid="stSidebarNav"] ul li div[role="button"],
    [data-testid="stSidebarNav"] ul li a {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
    }
    
            /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #8B7355;
            color: #e6e3d2;
    }
    /* Box around each page link with background color */
    [data-testid="stSidebarNav"] li {
        background-color: #e6e3d2;  /* Box background color */
        border-radius: 8px;
        margin: 8px;
        padding: 4px;
        text-align: center;
    }
    
    /* Optional: Hover effect */
    [data-testid="stSidebarNav"] li:hover {
        background-color: #d4ca96;  /* Hover box color */
    }
    
    /* Optional: Active/selected page styling */
    [data-testid="stSidebarNav"] li[aria-selected="true"] {
        background-color: #d4ca96;  /* Selected page box color */
    }
        
    .st-emotion-cache-12fmjuu{
            background-color: #e6e3d2;
            color: #8B7355;
            }
    .main-title {
        text-align: center;
        color: #d4af37;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 0px 0px 12px #0a2a66;
        font-family: "Georgia", serif;
        letter-spacing: 3px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #0a2a66;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }

    .stChatMessage {
        border-radius: 15px !important;
        padding: 12px 18px !important;
        border: 2px solid #d4af37 !important;
        background: rgba(255,255,255,0.7) !important;
        font-weight: 500;
        font-size: 16px;
        color: #3b2f16;
    }

    .stChatMessage.user {
        background: rgba(255, 235, 168, 0.8) !important;
        border-color: #e3c466 !important;
        box-shadow: 0 0 8px #e3c466;
    }

    .stChatMessage.assistant {
        background: rgba(187, 205, 233, 0.75) !important;
        border-color: #0a2a66 !important;
        box-shadow: 0 0 8px #0a2a66;
    }

    .stTextInput input {
        border: 2px solid #d4af37 !important;
        background: #fff9e6 !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        padding: 10px !important;
    }
    .st-emotion-cache-uhkwx6{
            background-color: #e6e3d2;
            color: #8B7355;
            }

    /* Button styling */
    button[kind="secondary"] {
        background-color: #8B7355 !important;
        color: #e6e3d2 !important;
        border-radius: 10px !important;
        border: 2px solid #d4af37 !important;
        font-weight: bold;
        transition: 0.3s;
    }
    button[kind="secondary"]:hover {
        background-color: #e6e3d2 !important;
        color: #8B7355 !important;
    }

    </style>
""", unsafe_allow_html=True)


# st.markdown('<div class="main-title">🏺History Tour Guide</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-title">Ask your friendly guide about ancient times, civilizations, and wonders!</div>', unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_bot_msg" not in st.session_state:
    st.session_state.last_bot_msg = ""



for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "Tour_Guide_Bot", "icons")

user_input = st.chat_input("Ask me about ancient Egypt...")
avatar_1 = os.path.join(ICONS_DIR, "cobra.png")

if user_input:

   
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": avatar_1})
    with st.chat_message("user", avatar=avatar_1):
        st.markdown(user_input)

    # run_history_crew(user_input)
    file_path = os.path.join(BASE_DIR, "ai-agents-artifacts", "step_5_final_result.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bot_response = data.get("answer", data)

    avatar_2 = os.path.join(ICONS_DIR, "pharaoh.png")

   
    with st.chat_message("assistant", avatar=avatar_2):
        st.markdown(bot_response)

    
    st.session_state.last_bot_msg = bot_response

   
    st.session_state.messages.append({"role": "assistant", "content": bot_response, "avatar": avatar_2})

