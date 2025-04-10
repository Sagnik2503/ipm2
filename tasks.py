from crewai import Task
from models import Report,OrganicResult,SerperSearchResults, NewsSearchResults
from agents import news_scraper, market_analysis, document_info_agent, risk_assessment_agent

# Document Query Task
document_query_task=Task(
    description=(
        "Your task is to go through the provided document and extract relevant information "
        "according to the Report model schema."
    ),
    expected_output=(
        "A structured JSON data containing the project details according to the Report model schema."
    ),
    output_pydantic=Report,
    agent=document_info_agent,
    output_file="output/project_overview.json"
)



# Market Analysis Task
market_analysis_task = Task(
    description=(
    "You are a market analyst performing research on a specific project.\n\n"
        "Your job is to analyze the latest market news, risks, and opportunities relevant to the project summary provided below.\n"
        "To do this, you **must use the 'Serper News Extraction Tool'**, which retrieves the most recent news articles.\n\n"
        "Instructions:\n"
        "1. Carefully read the project details below.\n"
        "2. Convert the project description into a **concise, relevant search query**.\n"
        "3. Call the `Serper News Extraction Tool` using the query. Example input: `query='AI startup in healthcare'`.\n"
        "4. Use the returned news articles to identify key trends, competitor activity, and potential risks.\n"
        "5. Return the final result as a structured JSON following the `NewsSearchResults` model.\n\n"
        "---\n\n"
        "📄 Project Summary:\n"
        "{document_query_task}"
    ),
    expected_output=(
        "A structured JSON data containing the TOOL OUTPUT according to the SerperSearchResults model schema."
    ),
    output_pydantic=NewsSearchResults,
    agent=market_analysis,
    context=[document_query_task],
    output_file="output/market_analysis.json"
)
# You can create one like the others

analyze_scraped_content_task = Task(
    description=(
    "You are tasked with producing a comprehensive, professional-grade **Market Intelligence Report** based on the full article content scraped from high-authority sources.\n\n"

    "You are given a list of recent news articles:\n"
        "{market_analysis_task}\n\n"

    "Your report must synthesize this content into an insightful, strategic deliverable that informs leadership decisions and project planning.\n\n"

    "### 🔍 Instructions:\n"
    "- Carefully analyze the full content of each article, not just summaries or titles.\n"
    "- Extract key trends, risks, and opportunities discussed across all sources.\n"
    "- Where available, use direct quotes, data points, or named technologies/competitors from the articles.\n"
    "- Explicitly cite which article each insight came from using markdown links (see Sources section).\n\n"

    "### 📋 Required Structure of the Report:\n\n"

    "**1. Executive Summary**\n"
    "- A high-level overview summarizing key trends, opportunities, threats, and takeaways.\n"
    "- Make it actionable and tailored for decision-makers.\n\n"

    "**2. Market Trends**\n"
    "- List and explain 5–7 major market trends that are shaping the digital transformation or enterprise platform landscape.\n"
    "- Include trends like AI automation, cloud-native adoption, DevSecOps, low-code/no-code, IoT, and quantum computing if present in the source content.\n"
    "- For each trend, provide a short explanation and real-world example if available.\n\n"

    "**3. Risk Landscape**\n"
    "- Identify and describe 5–10 relevant risks discussed or implied in the articles.\n"
    "- Categorize risks as Technical, Strategic, Regulatory, Operational, or Financial.\n"
    "- Include mitigation suggestions where possible.\n\n"

    "**4. Opportunities**\n"
    "- Identify 3–5 growth or innovation opportunities that Apollo can explore.\n"
    "- This may include emerging technologies, underserved markets, or integration pathways (e.g., IoT or low-code partnerships).\n"
    "- Each opportunity should include justification from the scraped sources.\n\n"

    "**5. Competitive Landscape**\n"
    "- List notable competitors mentioned in the articles (e.g., Microsoft Power Platform, ServiceNow, Salesforce, Mendix).\n"
    "- Include a brief note about their position, strengths, or market approach.\n"
    "- If no competitors are directly mentioned, infer logical ones based on context.\n\n"

    "**6. Actionable Recommendations**\n"
    "- Provide 5–7 strategic recommendations tailored for the Apollo team.\n"
    "- Base these on insights from the articles.\n"
    "- Each recommendation should be specific and supported by at least one cited source.\n\n"

    "**7. Strategic Fit with Apollo**\n"
    "- For each trend, risk, or opportunity, briefly explain how Apollo’s current direction aligns or where there may be gaps.\n"
    "- Use bullet points to indicate strategic strengths and weaknesses.\n\n"

    "**8. SWOT Analysis (optional but encouraged)**\n"
    "- Include a SWOT table (Strengths, Weaknesses, Opportunities, Threats) if enough data is available from the sources.\n"
    "- Use markdown formatting for the table.\n\n"

    "**9. Sources**\n"
    "- Include a bulleted list of all articles used.\n"
    "- Format as: `- [Article Title](https://example.com)`\n"
    "- Mention a 1-line summary or what each source contributed.\n"
    "- Include at least 5–10 relevant links if available.\n\n"

    "### ✅ Formatting Guidelines:\n"
    "- Use proper markdown syntax for headers, bullets, and links.\n"
    "- Use subheadings and bolding to enhance scanability.\n"
    "- Write in formal, professional, C-suite-friendly language.\n"
    "- Ensure the entire output is easily copy-pasteable into a markdown report generator or previewer.\n\n"

    "✅ Final output: A well-formatted, insight-rich **markdown report** that synthesizes all scraped content into a deliverable worthy of executive review and strategic planning."
)
,
    expected_output=(
        "A comprehensive, strategic market analysis report in markdown format, "
        "with no fewer than 1500 words, verified using the Word Count Tool."
    ),
    agent=news_scraper,
    context=[market_analysis_task],
    output_file="output/analysis_report.md",
    human_input=True
)
project_risk_assessment_task = Task(
    description=(
        "You are responsible for conducting a comprehensive risk assessment of a digital platform initiative.\n\n"
        "You will receive a detailed project description containing architectural decisions, integration points, tooling dependencies, and development methodologies.\n\n"
        "Your analysis should be structured and thorough, covering all major risk categories. For each risk, assess its likelihood, impact, and propose mitigation strategies.\n\n"
        "Use the following framework:\n\n"
        "**1. Strategic Risks**\n"
        "- Misalignment with business goals\n"
        "- Scope creep or changing stakeholder priorities\n\n"
        "**2. Technical Risks**\n"
        "- API reliability or third-party service dependency (e.g., Stripe, Twilio)\n"
        "- Scalability and availability risks in cloud-native deployments\n"
        "- Performance under load, latency, and failure tolerance\n\n"
        "**3. Operational Risks**\n"
        "- Delayed procurement of critical tools (e.g., Figma, Datadog)\n"
        "- Skill shortages or bandwidth constraints in cross-functional teams\n"
        "- QA and compliance process delays\n\n"
        "**4. Resource & Financial Risks**\n"
        "- Overrun of $110K budget cap\n"
        "- Underestimation of resource requirements for CI/CD, DevOps, or UX testing\n\n"
        "**5. Organizational & Compliance Risks**\n"
        "- Lack of stakeholder involvement in key agile ceremonies\n"
        "- Changes to external regulations (e.g., GDPR, WCAG)\n\n"
        "**6. Assumptions & Constraints Validation**\n"
        "- Identify if any listed assumptions could break\n"
        "- Reevaluate the impact of stated constraints\n\n"
        "🔚 Your final output must be a full Risk Register with:\n"
        "- Risk Title\n"
        "- Risk Category\n"
        "-Likelihood (Low / Medium / High)\n"
        "- Impact (Low / Medium / High)\n"
        "- Mitigation Strategy\n"
        "- Residual Risk Level\n"
        "- Owner / Responsible Party (optional)\n"
    ),
    expected_output=(
        "A full risk register in markdown table format or JSON, following the framework above. "
        "Each risk entry should include title, category, likelihood, impact, mitigation, and residual risk."
    ),
    context=[document_query_task, analyze_scraped_content_task],
    output_file="output/risk_register.md",
    agent=risk_assessment_agent,
)