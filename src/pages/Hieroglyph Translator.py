import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Hieroglyph Translator", page_icon="📜")

# Custom CSS for styling with the specified palette
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #e6e3d2;
    }
    
    /* Title styling */
    h1 {
        color: #8B7355 !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    [data-testid="stSidebar"] {
        background-color: #8B7355;
            color: #e6e3d2;
    }
    .st-emotion-cache-12fmjuu{
            background-color: #e6e3d2;
            color: #8B7355;
            }
    /* Sidebar background color */
            [data-testid="stSidebarNav"] ul li div[role="button"],
    [data-testid="stSidebarNav"] ul li a {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
    }
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
    /* Subheader and text styling */
    .stMarkdown p, .stMarkdown div {
        color: #8B7355;
        font-size: 1.1rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #8B7355;
        border: 2px solid #8B7355;
        border-radius: 8px;
        color: #e6e3d2;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #e6e3d2;
        border: 2px solid #8B7355;
        border-radius: 8px;
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
    
    /* Image caption styling */
    .stImage > div > small {
        color: #8B7355;
        font-style: italic;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #e6e3d2;
        border-left: 5px solid #8B7355;
        color: #8B7355;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        color: #8B7355;
    }
    
    /* General text output styling */
    .stMarkdown pre, .stMarkdown code {
        background-color: #e6e3d2;
        color: #8B7355;
    }
</style>
""", unsafe_allow_html=True)



st.title("𓀁 Hieroglyph AI Translator 𓀁")
st.write("Upload a photo containing Egyptian hieroglyphs and get the translation in the language you want.")

languages = {
    "English": "English",
    "Arabic": "Arabic (العربية)",
    "French": "French (Français)",
    "German": "German (Deutsch)",
    "Spanish": "Spanish (Español)",
    "Italian": "Italian (Italiano)",
    "Chinese": "Chinese (中文)",
    "Japanese": "Japanese (日本語)",
    "Portuguese": "Portuguese (Português)",
    "Russian": "Russian (Русский)"
}


selected_lang = st.selectbox(
    "Choose translation language:",
    list(languages.values())
)

uploaded = st.file_uploader("Upload Hieroglyph Image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", width=400)

    if st.button("Translate"):
        with st.spinner("Analyzing image and translating..."):

            prompt =  f"""
                You are a friendly tour guide who explains Egyptian hieroglyphs in a simple, clear way for tourists.

                Your tasks:
                1. Look at the hieroglyphs in the image.
                2. Identify the symbols (only the important ones).
                3. Give a short, easy translation in {languages[selected_lang]}.
                4. Give a simple explanation of what the text means (1–3 sentences only).

                Rules:
                - Keep the translation short.
                - Keep the explanation simple (tourist level).
                - Don’t use academic terms unless necessary.
                - If something is unclear in the image, mention it briefly.

                Output format:
                - *Translation:* (short translation, and bold it)
                - *Meaning:* (1–3 sentence explanation)

                Start now.
                """

            response = model.generate_content(
                [
                    prompt,
                    img
                ]
            )

        st.success("Translation Complete!")
        st.write(response.text)