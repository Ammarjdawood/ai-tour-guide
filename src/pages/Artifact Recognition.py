import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import pandas as pd
import os  
import sys


st.set_page_config(page_title="Egyptian Artifact Recognition", page_icon="🗿", layout="wide")

# Custom CSS with non-reddish hover color
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #e6e3d2;
    }
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


    /* Make the background of main content boxes match their border color */
.stFileUploader > div,
.stSelectbox > div > div,
.main .block-container {
    background-color: #e6e3d2 !important;
    border: 2px solid #e6e3d2 !important;
    border-radius: 8px;
}

/* Ensure the main content area has consistent background and border styling */
.main .block-container {
    background-color: #e6e3d2 !important;
    border: 2px solid #e6e3d2 !important;
    border-radius: 10px;
    padding: 1.5rem;
}

/* File uploader and selectbox containers */
.stFileUploader {
    border: 2px solid #e6e3d2;
    border-radius: 8px;
    background-color: #e6e3d2;
}

.stSelectbox > div > div {
    border: 2px solid #e6e3d2;
    background-color: #e6e3d2;
    border-radius: 8px;
}

/* Sidebar background color */
    [data-testid="stSidebarNav"] ul li div[role="button"],
    [data-testid="stSidebarNav"] ul li a {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
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
            

    /* Container styling with hieroglyphic borders */
    .main .block-container {
        background-color: rgba(230, 227, 210, 0.95);
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        border-radius: 10px;
        position: relative;
    }
    
    .main .block-container::before,
    .main .block-container::after {
        content: "𓀀 𓀁 𓀂 𓀃 𓀄 𓀅 𓀆 𓀇 𓀈 𓀉 𓀊 𓀋 𓀌 𓀍 𓀎 𓀏";
        position: absolute;
        left: 0;
        right: 0;
        font-size: 1.2rem;
        color: #D4A574;
        text-align: center;
        overflow: hidden;
        white-space: nowrap;
    }
    
    .main .block-container::before {
        top: -1.5rem;
    }
    
    .main .block-container::after {
        bottom: -1.5rem;
    }
    
    
    .subheader-text {
        font-size: 1.2rem;
        color: #6B5A4A;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Button styling with neutral hover color */
    .stButton > button {
        background-color: #D4A574;
        color: #2C1810;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(212, 165, 116, 0.3);
    }
    
    .stButton > button:hover {
        background-color: #E6C68A;  /* Pure golden hover without any red tones */
        box-shadow: 0 6px 16px rgba(212, 165, 116, 0.4);
        transform: translateY(-1px);
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #E8D8B9;
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #D4A574;
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

class_names = [
    'Akhenaten', 'Bent-pyramid-for-senefru', 'Colossal-Statue-of-Ramesses-II', 'Colossoi-of-Memnon',
    'Goddess-Isis-with-her-child', 'Hatshepsut', 'Hatshepsut-face', 'Khafre-Pyramid',
    'Mask-of-Tutankhamun', 'Nefertiti', 'Pyramid_of_Djoser', 'Ramessum',
    'Ramses-II-Red-Granite-Statue', 'Statue-of-King-Zoser', 'Statue-of-Tutankhamun-with-Ankhesenamun',
    'Temple_of_Isis_in_Philae', 'Temple_of_Kom_Ombo', 'The-Great-Temple-of-Ramesses-II',
    'amenhotep-iii-and-tiye', 'bust-of-ramesses-ii', 'menkaure-pyramid', 'sphinx'
]

def create_model():
    base_model = ResNet50(weights='imagenet', include_top=False, pooling='max')
    model = Sequential([
        base_model, BatchNormalization(),
        Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        Dropout(rate=0.5), Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        Dropout(rate=0.4), Dense(22, activation='softmax')
    ])
    return model

def preprocess_image(img):
    img_resized = img.resize((224, 224))
    img_array = image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@st.cache_data
def load_data():
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.dirname(__file__))
    # Construct the full path to the data file
    data_path = os.path.join(script_dir, "Artifact_Recognition", "data.csv")
    
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'data/data.csv' exists.")
        return None

@st.cache_resource
def load_model_with_weights():
    script_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(script_dir, "Artifact_Recognition", "best_resnet50.h5")
    try:
        model = create_model()
        model.load_weights(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model weights: {str(e)}")
        return None

def main():
    st.title("𓀂 Egyptian Artifact Recognition 𓀂")
    st.markdown('<p class="subheader-text">Upload an image to identify ancient Egyptian artifacts and access their historical information</p>', unsafe_allow_html=True)

    df = load_data()
    
    if "model" not in st.session_state:
        with st.spinner("Loading the trained model..."):
            model = load_model_with_weights()
            if model is not None:
                st.session_state.model = model
            else:
                st.error("Failed to load the model weights.")
                return
    
    model = st.session_state.model
    st.markdown("""
        <style>
            /* Ensure all artifact information buttons have uniform size */
            div[data-testid="column"] .stButton > button {
                width: 100% !important;
                height: 50px !important;
                min-height: 50px !important;
                padding: 0.5rem 0.75rem !important;
                box-sizing: border-box !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                font-size: 12px !important;
                white-space: normal !important;
                line-height: 1.2 !important;
            }
            
            /* Ensure consistent spacing between buttons */
            div[data-testid="column"] {
                padding: 0.25rem;
            }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader("Choose an image to classify", type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'])
        
        if uploaded_file is not None:
            image_pil = Image.open(uploaded_file)
            st.session_state['uploaded_image'] = image_pil

    with col2:
        if 'uploaded_image' in st.session_state:
            st.image(st.session_state['uploaded_image'], caption="Uploaded Image", width=400)

    if 'uploaded_image' in st.session_state:
        if st.button("Classify Artifact"):
            with st.spinner("Processing image and making prediction..."):
                processed_image = preprocess_image(st.session_state['uploaded_image'])
                predictions = model.predict(processed_image, verbose=0)
                predicted_class_idx = np.argmax(predictions[0])
                predicted_class = class_names[predicted_class_idx]
                
                st.session_state['predicted_class'] = predicted_class

    if 'predicted_class' in st.session_state:
        predicted_class = st.session_state['predicted_class']
        
    
        
        # Create a styled container for the prediction
        st.markdown(
            f"""
            <div style="
                width: 100%;
                padding: 1.5rem 2rem;
                background: linear-gradient(135deg, #E8D8B9, #F5E8C7);
                border-radius: 12px;
                border-left: 6px solid #D4A574;
                box-shadow: 0 6px 20px rgba(212, 165, 116, 0.25);
                text-align: center;
                margin-bottom: 2rem;
            ">
                <h3 style="
                    margin: 0 0 0.8rem 0; 
                    color: #8B7355; 
                    font-size: 1.4rem;
                ">
                    Identified Artifact
                </h3>
                <div style="
                    font-size: 1.8rem; 
                    color: #6B5A4A; 
                    font-weight: bold;
                ">
                    {predicted_class}
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
                
        row = df[df['Artifact'] == predicted_class]
        
        if not row.empty:
            st.subheader("Artifact Information")
            
            button_columns = st.columns(4)
            columns = df.columns[1:]
            
            for i, col in enumerate(columns):
                with button_columns[i % 4]:
                    toggle_key = f"toggle_{predicted_class}_{col}"
                    
                    if st.button(col, key=f"btn_{col}"):
                        current_state = st.session_state.get(toggle_key, False)
                        st.session_state[toggle_key] = not current_state
                    
                    if st.session_state.get(toggle_key, False):
                        value = row[col].values[0]
                        if pd.notna(value) and str(value).strip():
                            st.write(value)

if __name__ == "__main__":
    main()