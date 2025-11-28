from crewai import Agent, Task
import os
from model import llm
from savedir import output_dir
from scheme import SummaryResults

Summarizer_Agent = Agent(
    role="Text Cleaning and Summarization Agent",
    goal="Clean and summarize messy web-scraped text into clear, factual summaries.",
    backstory=(
        "You are an expert text analyst who cleans raw scraped data and extracts the essential information "
        "into short, human-readable summaries."
    ),
    verbose=True,
    llm=llm,


)


Summarizer_Task = Task(
    description=(
        "Clean and summarize the following scraped web content. "
        "Remove any navigation menus, ads, or repeated phrases. "
        "Keep only the informative parts, and return a concise paragraph summary"
        "Remove any signs of poor formatting or irrelevant content."
    ),
    expected_output=(" A JSON object with a 'summary' field containing the cleaned and summarized text."),
    output_json=SummaryResults,
    output_file=os.path.join(output_dir, "step_4_summary_results.json"),
    agent=Summarizer_Agent,
)

