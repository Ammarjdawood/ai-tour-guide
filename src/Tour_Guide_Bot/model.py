from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model=os.getenv("MODEL_ID"),
    api_key=os.getenv("GOOGLE_API_KEY"),  
    temperature=0.7
)
