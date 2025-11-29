import streamlit as st
import json
import os
from Tour_Guide_Bot.run_crew import run_history_crew


avatar = os.path.join("Tour_Guide_Bot", "icons", "eye-of-horus.png")
st.set_page_config(page_title="History Tour Guide", page_icon=avatar, layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #fdf6ec;
    }
    .main-title {
        text-align: center;
        color: #6b4f23;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #a37e2c;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .stChatMessage {
        border-radius: 15px !important;
        padding: 10px 15px !important;
    }
    .stChatMessage.user {
        background-color: #fff5da !important;
    }
    .stChatMessage.assistant {
        background-color: #f4e1c1 !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🏺History Tour Guide</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ask your friendly guide about ancient times, civilizations, and wonders!</div>', unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_bot_msg" not in st.session_state:
    st.session_state.last_bot_msg = ""



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



user_input = st.chat_input("Ask me about ancient Egypt...")
avatar_1 = os.path.join("Tour_Guide_Bot", "icons", "cobra.png")

if user_input:

   
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=avatar_1):
        st.markdown(user_input)

    run_history_crew(user_input)
    file_path = os.path.join("Tour_Guide_Bot", "ai-agents-artifacts", "step_5_final_result.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bot_response = data.get("answer", data)

    avatar_2 = os.path.join("Tour_Guide_Bot", "icons", "pharaoh.png")

   
    with st.chat_message("assistant", avatar=avatar_2):
        st.markdown(bot_response)

    
    st.session_state.last_bot_msg = bot_response

   
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

