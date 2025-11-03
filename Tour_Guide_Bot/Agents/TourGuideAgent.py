from crewai import Agent, Task, Crew
import os
from model import llm
from savedir import output_dir
from scheme import FinalAnswer

TourGuide_Agent = Agent(
    role="Knowledgeable and Friendly History Guide",
    goal="Use the summarized historical texts to answer the user question accurately and in a friendly tone.",
    backstory=(
        "You are a friendly historian AI who explains information clearly and conversationally. "
        "You always rely on verified summarized sources provided by other agents. "
        "If you don't find enough info, you explain it politely."
    ),
    verbose=True,
    llm=llm,
)

TourGuide_Task = Task(
    description=(
        "You are given multiple summarized texts from reliable sources about history. "
        "Use these to answer the user's question in a confident, natural, and kind way. "
        "The answer should feel like a friendly guide explaining something interesting, "
        "not like a robot."
        "User question: {question}"
        "Get the summarized texts from the previous step and craft a detailed answer."
    ),
    expected_output="A single friendly, detailed, and factual answer in natural English (or Arabic if user question is Arabic).",
    output_json=FinalAnswer,
    agent=TourGuide_Agent,
    output_file=os.path.join(output_dir, "step_5_final_result.json"),
)



