from crewai import Agent, Task
import os
from scheme import SearchResults
from model import llm
from savedir import output_dir
from tavily import TavilyClient
from crewai.tools import tool
from dotenv import load_dotenv
load_dotenv()


search_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))


@tool
def search_tool(query: str):
    """Useful for search-based queries. This tool returns a list of the most relevant URLs for a given query."""
    try:
        
        search_results = search_client.search(
            query=query, 
            search_depth="basic", 
            max_results=5    
        )
        
        urls = [result['url'] for result in search_results.get('results', [])]
        
        return urls
    except Exception as e:
        return f"An error occurred during search: {e}"



Search_Agent = Agent(
    role="Historical Web Search Agent",
    goal=(
        """
        Use the provided search queries to find relevant, trustworthy, and diverse web sources. 
        related to the user's historical question. Focus on retrieving results from reputable sources.
        Always respond in the same language used by the user.
        """
    ),
    backstory=(
        """
        You are an expert digital historian and research analyst. 
        You specialize in searching for high-quality historical information from reliable online sources. 
        Your job is to transform search queries into meaningful, credible web results that can later be used for historical content generation.
        """
    ),
    llm=llm,
    verbose=True,
    tools=[search_tool],
)

Search_Task = Task(
    description=(
        """
        Execute web searches using the provided search queries to gather relevant historical information.
        Ensure the results are from reputable and diverse sources.
        Ignore any search results with confidence score less than ({score_th}) or irrelevant to the historical question: "{question}".
        Take into account only the top {num_queries} search queries generated earlier.
        For each query, return only the **first most relevant URL**.
        """
    ),
     expected_output=(
        "A JSON object containing a list of search results. "
        "Each entry should include the query text and a list of related URLs."
    ),
    output_json=SearchResults,
    output_file=os.path.join(output_dir, "step_2_search_results.json"),
    agent=Search_Agent,
)
