# AI-Powered Interactive Tourist Guide

An intelligent Streamlit application that enhances museum and historical site experiences using computer vision, multi-agent systems, and generative AI. 
The app serves as a smart tour guide capable of identifying artifacts, answering questions, restoring damaged statues, and interpreting hieroglyphics.

## Project Description, Demo & Presentation
- Here is the Description Document of the project: [Document](https://drive.google.com/file/d/113psCj3pjrRmhe8CFjGQfiJYptkd_0V2/view)

- Project Demo Video: [Demo](https://drive.google.com/drive/folders/1YsnyWHW0yyKepRSIB96RhbuLqZ117Qv6?usp=sharing)

- Project Presentation: [Presentation](https://www.canva.com/design/DAG6Y8wx7BM/NLbsndPC2p7f7U1gQpq7lw/edit?utm_content=DAG6Y8wx7BM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) 

## Features

### 1. Artifact Recognition (Fine-Tuned ResNet50)
- Fine-tuned a ResNet50 model on **22 classes of ancient artifacts**.
- Added custom layers and trained both new and pretrained layers.
- The model predicts the artifact from an uploaded image, then fetches detailed information from our database.
- **Training Data**: [Link](https://universe.roboflow.com/fatma-saeed-th9nx/egypt-landmarks/dataset/5)
- **Information Data for each Artifact and Model File**: [Data & Model](https://drive.google.com/drive/folders/1-DT8iBzUKuTwoIeFHDbPHjBeugTUZVmV?usp=sharing)


### 2. Multi-Agent Tourist Assistance
A 5-agent pipeline that helps tourists get well-researched answers:

1. **Query Generator** – Creates search queries from the user’s question.  
2. **Search Agent** – Performs web searches using each query.  
3. **Scraper Agent** – Extracts content from the collected links.  
4. **Cleaner & Summarizer** – Cleans and summarizes all scraped data.  
5. **Story Builder** – Combines summaries into an engaging, readable explanation.


### 3. Artifact Restoration (Stable Diffusion Inpainting)
- Tourists can upload a photo of a broken statue.
- They highlight the missing parts.
- Stable Diffusion inpainting reconstructs and displays a restored version of the artifact.


### 4. Hieroglyphic Interpretation (Gemini API)
- Users upload an image containing hieroglyphics.
- Gemini API explains the text clearly and in the user’s preferred language.


## Tech Stack
- **Environment Management: Conda**
- **Python**
- **Streamlit**
- **Tensorflow**
- **mlflow**
- **ResNet50**
- **Crewai**
- **Stable Diffusion Inpainting**
- **Gemini API**
- **BeautifulSoup**


## About the Project
This application blends historical education with AI, providing tourists with a personalized and immersive learning experience.

## Team
- Ammar Ashraf Moawad
- Ammar Jamal Dawood
- Belal Mohsen Mosbah
- Mariam Mohamed Abdelmoneim 
- Mohammed Hamada Saad Shoaib
- Salwa Mustafa Mohammed


##  How to Run  

1️⃣ Clone repo:
```bash
git clone <repo-link>
cd ai-tour-guide
```
2️⃣ Create a new environment:
```bash
conda create -n env-name python=3.10
```
3️⃣ Activate the environment:
```bash
conda activate env-name
```
4️⃣ Install the required packages
```bash
cd src
cp .env.example .env
pip install -r requirements.txt
```
5️⃣ Configure environment variables:
Edit the `.env` file with your API keys and configuration:

```env
MODEL_NAME = your_model_name
GOOGLE_API_KEY = your_google_api_key
TAVILY_API_KEY = your_tavily_api_key

```
6️⃣ Run streamlit app
```bash
streamlit run Home.py
```
