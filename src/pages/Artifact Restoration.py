import streamlit as st
from PIL import Image
import numpy as np
import torch
from diffusers import StableDiffusionInpaintPipeline
from streamlit_drawable_canvas import st_canvas


st.set_page_config(page_title="Artifact Repair with AI", layout="wide")
# ------------------- Load Inpainting Model (once) -------------------
if torch.cuda.is_available():
    print(f"CUDA is available. GPU: {torch.cuda.get_device_name()}")
    device = "cuda"
    torch_dtype = torch.float16
else:
    print("CUDA is not available. Running on CPU.")
    device = "cpu"
    torch_dtype = torch.float32

@st.cache_resource
def load_pipe():
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        torch_dtype=torch_dtype,
        safety_checker=None
    )
    pipe = pipe.to(device)
    return pipe

pipe = load_pipe()


# ------------------- Streamlit UI ------------------- 
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

st.title('𓀀 From Broken Artifact To Perfect Artifact 𓀀')

uploaded_file = st.file_uploader("Upload photo of broken artifact", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # Resize for speed & canvas stability
    max_w = 768
    if image.width > max_w:
        ratio = max_w / image.width
        new_size = (max_w, int(image.height * ratio))
        image = image.resize(new_size, Image.LANCZOS)

    #st.image(image, caption="Original", use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Draw WHITE on broken areas** (black = good part)")
        canvas_result = st_canvas(
            fill_color="#e6e3d2",
            stroke_width=25,
            stroke_color="#FFFFFF",
            background_image=image,
            height=image.height,
            width=image.width,
            drawing_mode="freedraw",
            key="canvas",
        )
    with col2:
      st.write("**The Mask**")
      if canvas_result.image_data is not None:
          # Create binary mask
          mask_np = np.array(canvas_result.image_data)
          gray = np.mean(mask_np[:, :, :3], axis=2)
          mask = np.where(gray > 20, 255, 0).astype(np.uint8)
          mask_pil = Image.fromarray(mask, mode="L")

  
          st.image(mask_pil, caption="Your Mask (white = repair zone)")

          if st.button("Generate Fixed Artifact"):
              with st.spinner("AI is repairing the artifact..."):
                  # Run inpainting
                  result = pipe(
                      prompt="ancient broken artifact, realistic archaeological restoration, same material and color as the visible parts, highly detailed stone texture, and complete it.",
                      image=image,
                      mask_image=mask_pil,
                      strength=0.85,
                      guidance_scale=7.5,
                      num_inference_steps=50,
                  ).images[0]

              st.success("Done!")
              st.image(result, caption="Repaired Artifact")

              # Save & download
              result.save("repaired_artifact.png")
              with open("repaired_artifact.png", "rb") as f:
                  st.download_button(
                      "Download Repaired Image",
                      f,
                      "repaired_artifact.png",
                      "image/png"
                  )