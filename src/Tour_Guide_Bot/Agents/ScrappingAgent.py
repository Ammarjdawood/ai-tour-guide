from crewai import Agent, Task
from dotenv import load_dotenv
import os
from crewai.tools import tool
from scheme import ScrapedContent
from model import llm
from savedir import output_dir
from bs4 import BeautifulSoup
import requests

load_dotenv()


def simple_scraper_tool(page_url: str):
    """
    Free simple web scraping tool that extracts clean text only.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # extract text
        text = soup.get_text(separator="\n")
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return {
            "page_url": page_url,
            "status": "ok",
            "clean_text": clean_text[:5000]
        }

    except Exception as e:
        return {
            "page_url": page_url,
            "status": "error",
            "error": str(e)
        }



@tool
def web_scraper(page_url: str):
    """
    Scrape and extract clean text content from a webpage given its URL.
    """
    return simple_scraper_tool(page_url)

Scrapping_Agent = Agent(
    role="Historical Data Scraper Agent",
    goal="Extract high-quality clean text content from webpages about the user question: {question}",
    backstory=(
        "This agent works like a digital tour guide assistant. "
        "It gathers factual and readable historical text from different pages about the user question: {question}, "
        "To be shown to tourists."
    ),
    llm=llm,
    verbose=True,
    tools=[web_scraper],
)

Scrapping_Task = Task(
    description="\n".join([
        "Extract clean historical content from multiple webpage URLs.",
        "Focus on retrieving factual, well-structured, and readable text relevant to the user question: {question}.",
        "Return the text content in clean, structured JSON format."
    ]),
    expected_output="A JSON object with each URL and its extracted text content.",
    output_json=ScrapedContent,
    output_file=os.path.join(output_dir, "step_3_scraping_results.json"),
    agent=Scrapping_Agent,
)
