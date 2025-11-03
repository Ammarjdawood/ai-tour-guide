from crewai import Crew, Process
from Agents.QuereAgent import Query_Agent, Query_Task
from Agents.SearchAgent import Search_Agent, Search_Task
from Agents.ScrappingAgent import Scrapping_Agent, Scrapping_Task
from Agents.SummaryAgent import Summarizer_Agent, Summarizer_Task
from Agents.TourGuideAgent import TourGuide_Agent, TourGuide_Task


history_crew = Crew(
    agents=[
        Query_Agent,
        Search_Agent,
        Scrapping_Agent,
        Summarizer_Agent,
        TourGuide_Agent,

    ],
    tasks=[
        Query_Task,
        Search_Task,
        Scrapping_Task,
        Summarizer_Task,
        TourGuide_Task,
    ],
    process=Process.sequential,

)
def run_history_crew(user_question):
    crew_results = history_crew.kickoff(
        inputs={
            "question": user_question,
            "no_keywords": 3,
            "score_th": 0.50,
            "num_queries": 2,
        }
     )
    return crew_results

run_history_crew("How did the Nile River influence the development of ancient Egypt?")
