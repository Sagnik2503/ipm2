import os
from crewai import Crew, Process
from agents import document_info_agent, market_analysis, news_scraper, risk_assessment_agent
from tasks import document_query_task, market_analysis_task, analyze_scraped_content_task, project_risk_assessment_task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
# Make sure output folder exists
os.makedirs("output", exist_ok=True)

for file in [
    'output/project_overview.json',
    'output/market_analysis.json',
    "output/analysis_report.md",
    "output/risk_register.md"
]:
    if os.path.exists(file):
        os.remove(file)   
knowledge=PDFKnowledgeSource(file_paths="Apollo Project Report.pdf")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
crew=Crew(
    agents=[document_info_agent, market_analysis, news_scraper, risk_assessment_agent],
    tasks=[document_query_task, market_analysis_task, analyze_scraped_content_task, project_risk_assessment_task],
    process=Process.sequential,
    knowledge_sources=[knowledge],
    verbose=True,
    embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
    }
    
    
    
)
try:
    crew.kickoff()
    

except Exception as e:
    print("💥 CrewAI execution failed!")
    print(e)

