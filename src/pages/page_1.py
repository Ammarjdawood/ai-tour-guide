import streamlit as st
from PIL import Image
import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


st.set_page_config(page_title="Hieroglyph Translator", page_icon="📜")

st.title("📜 Hieroglyph AI Translator")
st.write("Upload a photo containing Egyptian hieroglyphs and get the translation in the language you want.")


languages = {
    "English": "English",
    "Arabic": "Arabic",
    "French": "French",
    "German": "German",
    "Spanish": "Spanish",
    "Italian": "Italian",
    "Chinese": "Chinese"
}

selected_lang = st.selectbox(
    "Choose translation language:",
    list(languages.keys())
)

uploaded = st.file_uploader("Upload Hieroglyph Image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", width=400)

    if st.button("Translate"):
        with st.spinner("Analyzing image and translating..."):

            prompt = f"""
            You are a professional Egyptologist specializing in ancient Egyptian writing.
            You will be given an image that contains hieroglyphs.
            Use the following reference: (https://en.wikipedia.org/wiki/Gardiner%27s_sign_list) to help identify hieroglyphs.
            Your task is:
            1. Identify and recognize each hieroglyph symbol.
            2. Translate them into: {languages[selected_lang]}.
            3. Provide a brief explanation of the meaning and context of the hieroglyphs.
            Provide your response in a clear and structured format.
            """

            response = model.generate_content(
                [
                    prompt,
                    img
                ]
            )

        st.success("Translation Complete!")
        st.write(response.text)

