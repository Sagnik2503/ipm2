from crewai import Agent, LLM
from dotenv import load_dotenv
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from tools.testtool import TavilySearchTool, TavilyScrapeTool
from tools.word_count import WordCounterTool
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
    goal="Analyze documents provided in the knwledge directory, extract critical information, and deliver actionable insights in a clear and comprehensive report.",
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

# Market Analysis Agent
market_analysis = Agent(
    role="Market Analyst",
    goal="Analyze the latest market trends and news relevant to the project's description by gathering insights from various sources and identifying key trends and risks.",
    backstory=(
        "You are a seasoned market analyst with extensive experience in identifying "
        "industry trends, competitive landscapes, and emerging market opportunities. "
        "You specialize in leveraging real-time news data to provide informed strategic recommendations."
    ),
    verbose=True,
    tools=[TavilySearchTool()],
    max_rpm=30
)

# 🕸 Web Scraper Agent (scrapes full content)
news_scraper = Agent(
    role="Web Content Scraper",
    goal="Scrape and summarize full content from provided news URLs using the Tavily Scrape Tool.",
    backstory=(
        "You are a web scraping expert who excels at extracting meaningful data from "
        "online articles, even on dynamic websites. You specialize in turning raw data "
        "into actionable insights for strategic decision-making."
    ),
    verbose=True,
    tools=[TavilyScrapeTool()],
    max_rpm=30
)

risk_assessment_agent = Agent(
    role="Enterprise Risk Analyst",
    goal="Identify, categorize, and evaluate risks for large-scale digital platform projects to help stakeholders plan mitigations effectively.",
    backstory=(
        "You are a seasoned enterprise risk consultant with over a decade of experience helping tech companies assess strategic, operational, and technical risks. "
        "You specialize in cloud-native platform initiatives, agile development environments, and third-party vendor integrations. "
        "You are meticulous in risk identification and renowned for offering actionable mitigation strategies that reduce uncertainty and enhance project stability."
    ),
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

# Final Integration Agent
final_integration_agent = Agent(
    role="Strategic Insights Synthesizer",
    goal=(
        "Integrate insights from various analyses, including document queries, market trends, scraped content, "
        "and risk assessments, to produce a comprehensive, actionable report tailored for executive decision-making."
    ),
    backstory=(
        "You are a highly skilled strategist specializing in synthesizing complex datasets into clear, "
        "insightful deliverables. With a knack for identifying patterns and aligning recommendations with strategic goals, "
        "you excel at delivering reports that empower stakeholders to make informed decisions."
    ),
    verbose=True,
    llm=llm,  # Replace with your LLM configuration, e.g., OpenAI, Anthropic, etc.
    tools=[WordCounterTool()],  # Add any necessary tools, if needed
)