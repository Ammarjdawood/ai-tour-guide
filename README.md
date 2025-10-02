# 🏛️ AI-Powered Smart Tour Guide for Museums and Archaeological Sites

This repository contains the code and documentation for an AI-driven mobile application designed to enhance the visitor experience at museums and archaeological sites. The "Smart Tour Guide" transforms a user's phone camera into an intelligent assistant that can instantly recognize, translate, and digitally restore artifacts.

## ✨ Project Idea

The goal of this project is to create an **AI-driven mobile application** that acts as a comprehensive tour guide. By simply capturing an image of an artifact, the user can receive rich historical context, real-time translation of ancient scripts, and a glimpse of the artifact's original, complete form through digital reconstruction.

## 🚀 Key Features and Deliverables

The project focuses on three primary AI capabilities:

1.  **Artifact Recognition Model (Computer Vision):**
    * **Function:** Identifies and classifies the type of artifact from a user-captured image.
    * **Output:** Retrieves and displays relevant historical metadata from the knowledge base.

2.  **Script Recognition & Translation (OCR + NLP):**
    * **Function:** Detects and extracts ancient scripts (e.g., hieroglyphics) from images.
    * **Output:** Translates the extracted symbols or text into a modern language (e.g., English/Arabic).

3.  **Digital Restoration Model (Generative AI):**
    * **Function:** Uses image-to-image or 3D reconstruction techniques to digitally restore broken or incomplete artifacts.
    * **Output:** Shows a visualization of the artifact's original form.

The final application is hosted via a **Streamlit App** to demonstrate the full end-to-end Machine Learning Pipeline.

## 💻 Technology Stack

The project utilizes a powerful combination of tools across Computer Vision, Natural Language Processing, and 3D visualization.

| Component | Tool/Library | Purpose |
| :--- | :--- | :--- |
| **Machine Learning** | **TensorFlow/Keras** | Training and deploying core CV/Generative AI models. |
| **Computer Vision** | **OpenCV** | Image preprocessing (denoising, resizing, segmentation). |
| **OCR** | **Tesseract OCR** | Initial detection and character recognition of scripts. |
| **NLP/Translation** | **Hugging Face Transformers** | Advanced translation models for ancient scripts. |
| **Digital Reconstruction** | **Unity3D** | Potential platform for displaying real-time 3D reconstructions. |
| **Knowledge Base** | **Database / Graph DB** | Storing artifact metadata, reconstructions, and translations. |
| **Web Interface** | **Streamlit** | Building the final interactive demo application. |

## 🛠️ Project Pipeline

The user input follows a sequential pipeline to generate the results:

1.  **INPUT:** User captures an artifact image via the mobile app (simulated via Streamlit).
2.  **PREPROCESSING (OpenCV):** Image denoising, resizing, and segmentation to prepare for models.
3.  **SCRIPT OCR (Tesseract):** Detects and converts symbols in the image to text format.
4.  **ARTIFACT RECOGNITION (CV Model):** Classifies the artifact type and retrieves metadata.
5.  **TRANSLATION MODEL (Hugging Face):** Translates recognized scripts into modern text.
6.  **ARTIFACT RECONSTRUCTION (Generative AI/Unity3D):** Generates image or 3D view of the complete artifact.
7.  **KNOWLEDGE BASE:** Stores and retrieves all related data (metadata, translations, reconstructions).
8.  **RESULTS (Streamlit/Web):** Display of artifact facts, translated text, and the reconstructed image/model.

## 👥 Project Team

This project is a collaborative effort by the following team members:

| Name | Role / Contribution |
| :--- | :--- |
| **Ammar Jamal Dawood** | Team Leader |
| Ammar Ashraf Moawad | Artifact Recognition Model (CV) |
| Belal Mohsen Mosbah | Artifact Recognition Model (CV) |
| Mariam Mohamed Abdelmoneim | Digital Artifact Restoration (Generative AI) |
| Salwa Mustafa Mohamed | Digital Artifact Restoration (Generative AI) |
| Mohamed Hamada Saad Shoaib | *Role to be finalized (e.g., NLP, Knowledge Base)* |

## 📂 Dataset Sources

The models are trained using the following data:

* Artifact images (for Recognition and Restoration).
* Artifact metadata (for the Knowledge Base).
* Ancient script texts and their corresponding modern translations (for OCR and Translation Models).

***

## ⚙️ Setup and Installation

*Detailed setup instructions (dependencies, environment setup, model weights download, and running the Streamlit app) will be added here upon completion of the initial development phases.*
