from crewai import Agent, Task
from model import llm
from scheme import SuggestedSearchQueries
import os
from savedir import output_dir


Query_Agent = Agent(
    role = "Search Queries Recommendation Agent",
    goal = (
        """
         Analyze the user's historical question carefully to generate a list of optimized and diverse search queries.
         Ensure that all generated queries are short, clear, and ready to be used directly in a search engine.
         Always respond in the same language the user uses when asking their question.
        """
    ),
    backstory = (
      """
      You are a highly skilled historical researcher and information strategist. 
      Your expertise lies in understanding complex historical questions and transforming them
      into precise, targeted search queries that help uncover accurate and diverse information sources.
        """),
    llm=llm,
    verbose=True,
)

Query_Task = Task(
    description = ("""
                     Analyze the following user question carefully:{question}
                     Generate a list of {no_keywords} optimized and diverse search queries that directly address the user's question.
                     Ensure that all generated queries are short, clear, and ready to be used directly in a search engine."""
                ),
    expected_output = "A JSON object containing a list of suggested search queries.",
    output_json=SuggestedSearchQueries,
    output_file=os.path.join(output_dir, "step_1_suggested_search_queries.json"),
    agent=Query_Agent
       )