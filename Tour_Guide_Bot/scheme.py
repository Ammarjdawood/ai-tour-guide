from pydantic import BaseModel, Field
from typing import List

class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(..., title="Suggested search queries to be passed to the search engine",
                               min_items=1, max_items=10)
    
class SearchResultItem(BaseModel):
    query: str = Field(..., description="The original search query text.")
    link: str = Field(..., description="The first URL link relevant to the search query.")

class SearchResults(BaseModel):
    results: List[SearchResultItem] = Field(..., description="List of queries and their corresponding web search results.")

class ScrapedContentItem(BaseModel):
    url: str = Field(..., description="The URL of the webpage.")
    content: str = Field(..., description="The extracted clean text content from the webpage.")

class ScrapedContent(BaseModel):
    items: List[ScrapedContentItem] = Field(..., description="List of scraped content items.")
    

class SummaryResult(BaseModel):
    summary: str = Field(..., description="The cleaned and summarized text content from the webpage.")

class SummaryResults(BaseModel):
    summaries: List[SummaryResult] = Field(..., description="List of summarized results.")

class FinalAnswer(BaseModel):
    answer: str = Field(..., description="The final detailed and friendly answer to the user's question.")

    