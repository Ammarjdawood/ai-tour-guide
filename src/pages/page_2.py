import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image


class_names = [
 'Akhenaten',
 'Bent-pyramid-for-senefru',
 'Colossal-Statue-of-Ramesses-II',
 'Colossoi-of-Memnon',
 'Goddess-Isis-with-her-child',
 'Hatshepsut',
 'Hatshepsut-face',
 'Khafre-Pyramid',
 'Mask-of-Tutankhamun',
 'Nefertiti',
 'No_Label',
 'Pyramid_of_Djoser',
 'Ramessum',
 'Ramses-II-Red-Granite-Statue',
 'Statue-of-King-Zoser',
 'Statue-of-Tutankhamun-with-Ankhesenamun',
 'Temple_of_Isis_in_Philae',
 'Temple_of_Kom_Ombo',
 'The-Great-Temple-of-Ramesses-II',
 'amenhotep-iii-and-tiye',
 'bust-of-ramesses-ii',
 'menkaure-pyramid',
 'sphinx'
]



@st.cache_resource
def load_my_model():
    model = load_model("best_resnet50.h5")
    return model

model = load_my_model()


st.title("Ancient Egypt Artifact Classifier")
st.write("Upload an image and the model will predict the artifact.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    
    preds = model.predict(img_array)
    pred_index = np.argmax(preds)
    pred_class = class_names[pred_index]
    pred_conf = np.max(preds)

    
    st.subheader("Prediction:")
    st.write(f"**{pred_class}**")
    st.write(f"Confidence: **{pred_conf:.2f}**")
