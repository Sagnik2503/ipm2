from crewai import Task

# Document Query Task
document_query_task=Task(
    description=(
        "Your task is to go through the provided document and extract relevant information "
        "according to the FinalReport model schema."
    ),
    expected_output=(
        "A structured JSON data containing the project details according to the FinalReport model schema."
    ),
    agent="researcher_agent",
)



# Market Analysis Task
market_analysis_task = Task(
    description=(
        "Conduct a comprehensive market analysis for the given project. "
        "Utilize the latest industry news, competitor strategies, and risk assessments to provide insights.\n\n"
        "IT IS VERY IMPORTANT to base your research on the **project description** extracted from "
        "the output of the `document_query_task` stored in `output/project_overview.json`.\n\n"
        "Steps:\n"
        "  1. **Extract the project description** from the `document_query_task` output and turn it into a small query that best describes the project description.\n"
        "  2. Pass this query to the SerperNewsTool to get the most relevant information."
    ),
    expected_output=(
        "A structured JSON data containing the TOOL OUTPUT according to the NewsData model schema."
    ),
    agent="market_analysis_agent",
    context=["document_query_task"]
)

# Stock Analysis Task
stock_analysis_task = Task(
    description=(
        "Conduct a comprehensive stock market analysis using data extracted from prior tasks.\n\n"
        "**Data Sources:**\n"
        "- Extract **project details** from `document_query_task` output.\n"
        "- Scrape **market analysis** insights from `market_analysis_task` using the Website Scrape Tool.\n"
        "- Retrieve **real-time financial news** using the ExaSearchTool.\n\n"
        "**Objective:**\n"
        "Structure the analysis strictly according to the `StockTrendAnalysisResult` model.\n\n"
        "**Analysis Requirements:**\n"
        "- Summarize recent stock market fluctuations.\n"
        "- Identify job market trends impacting financial stability.\n"
        "- Extract and assess major economic news affecting investments.\n"
        "- Provide sector-wise performance insights.\n"
        "- Recommend data-driven investment strategies."
    ),
    expected_output=(
        "Your final report **must strictly follow** this structured format to align with the StockTrendAnalysisResult model."
    ),
    agent="stock_analysis_agent",
    context=["document_query_task", "market_analysis_task"]
)



# Assess Risk Task
assess_risk_task = Task(
    description=(
        "Examine the provided documents and text files to determine a risk score based on "
        "content analysis. The risk levels are defined as:\n"
        "- Low Risk: 0-3\n"
        "- Medium Risk: 4-6\n"
        "- High/Critical Risk: 7-10\n\n"
        "Analyze the data thoroughly and provide a detailed summary, including the final risk level."
    ),
    expected_output=(
        "A risk score report that includes:\n"
        "- Document names analyzed\n"
        "- Key findings from each document\n"
        "- Final risk score with its classification (Low, Medium, or High/Critical)\n"
        "- Recommendations for risk mitigation."
    ),
    agent="risk_assessor"
)