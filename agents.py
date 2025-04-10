from crewai import Agent, LLM
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, SeleniumScrapingTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
load_dotenv()
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model=os.getenv("MODEL"),
    api_key=GEMINI_API_KEY,
    temperature=0,
    max_retries=3
    # stop=["###"]
)
knowledge=PDFKnowledgeSource(file_paths="Apollo Project Report.pdf")

document_info_agent=Agent(
    role="Document Analyst",
    goal="Analyze documents provided in the root directory, extract critical information, and deliver actionable insights in a clear and comprehensive report.",
    backstory="You are a highly skilled professional in document analysis, specializing in extracting valuable insights from complex materials such as PDFs, reports, and contracts. You excel at synthesizing findings and presenting them in a concise, actionable format.",
    verbose=True,
    llm=llm,
    embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            },
    knowledge_sources=[knowledge]
)

market_analysis=Agent(
    role="Market Analyst",
    goal="Analyze the latest market trends and news relevant to the project's description by gathering insights from various sources and identifying key trends and risks.",
    backstory="You are a seasoned market analyst with extensive experience in identifying industry trends, competitive landscapes, and emerging market opportunities. You specialize in leveraging real-time news data to provide informed strategic recommendations.",
    verbose=True,
    llm=llm,
    tools=[SerperDevTool()]
)

# 🕸 Web Scraper Agent (scrapes full content)
news_scraper = Agent(
    role="Web Content Scraper",
    goal="Scrape and summarize full content from provided news URLs using Selenium scraping.",
    backstory="You are a web scraping expert who excels at extracting meaningful data from online articles, even on dynamic websites.",
    verbose=True,
    llm=llm,
    tools=[SeleniumScrapingTool()]
)