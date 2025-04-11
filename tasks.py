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
    
    "⚠️ Due to token or character limits, you **may not be able to scrape all articles at once**. "
        "In such cases, you must scrape them **in batches**.\n"
        "After scraping a batch, **continue to scrape the remaining articles automatically**, without needing human input.\n\n"

    "You are given a list of recent news articles:\n"
        "{market_analysis_task}\n\n"

    "Your report must synthesize this content into an insightful, strategic deliverable that informs leadership decisions and project planning.\n\n"

    "### 🔍 Instructions:\n"
    "- Carefully scrape the full content of each website url, not just summaries or titles.\n"
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


    "### FORMAT INSTRUCTIONS:\n ----->  THIS IS EXTREMELY IMPORTANT!!!\n" 
    "To use the scraper:\n"
    "Thought: I need to extract full text from this article.\n"
    "Action: Read website content\n"
    "Action Input: {\"website_url\": \"https://example.com\"}\n\n"
    "To finish:\n"
    "Thought: I now can give a great answer\n"
    "Final Answer: [a list of scraped article content or structured summary]\n\n"
    "❗Always include 'Action:' or 'Final Answer:', or the system will fail."
    
    
    "✅ Final output: A well-formatted, insight-rich **markdown report** that synthesizes all scraped content into a deliverable worthy of executive review and strategic planning."

)
,
    expected_output=(
        "A comprehensive, strategic market analysis report in markdown format."
    ),
    agent=news_scraper,
    context=[market_analysis_task],
    output_file="output/analysis_report.md",
    # human_input=True
)
project_risk_assessment_task = Task(
    description=(
        # "You are responsible for conducting a comprehensive risk assessment of the Project report provided to you in the knowledge directory.\n\n"
        # "You have the detailed project description containing architectural decisions, integration points, tooling dependencies, and development methodologies.\n\n"
        # "Your analysis should be structured and thorough, covering all major risk categories. For each risk, assess its likelihood, impact, and propose mitigation strategies.\n\n"
        # "Use the following framework:\n\n"
        # "**1. Strategic Risks**\n"
        # "- Misalignment with business goals\n"
        # "- Scope creep or changing stakeholder priorities\n\n"
        # "**2. Technical Risks**\n"
        # "- API reliability or third-party service dependency (e.g., Stripe, Twilio)\n"
        # "- Scalability and availability risks in cloud-native deployments\n"
        # "- Performance under load, latency, and failure tolerance\n\n"
        # "**3. Operational Risks**\n"
        # "- Delayed procurement of critical tools (e.g., Figma, Datadog)\n"
        # "- Skill shortages or bandwidth constraints in cross-functional teams\n"
        # "- QA and compliance process delays\n\n"
        # "**4. Resource & Financial Risks**\n"
        # "- Overrun of $110K budget cap\n"
        # "- Underestimation of resource requirements for CI/CD, DevOps, or UX testing\n\n"
        # "**5. Organizational & Compliance Risks**\n"
        # "- Lack of stakeholder involvement in key agile ceremonies\n"
        # "- Changes to external regulations (e.g., GDPR, WCAG)\n\n"
        # "**6. Assumptions & Constraints Validation**\n"
        # "- Identify if any listed assumptions could break\n"
        # "- Reevaluate the impact of stated constraints\n\n"
        # "🔚 Your final output must be a full Risk Register with:\n"
        # "- Risk Title\n"
        # "- Risk Category\n"
        # "-Likelihood (Low / Medium / High)\n"
        # "- Impact (Low / Medium / High)\n"
        # "- Mitigation Strategy\n"
        # "- Residual Risk Level\n"
        # "- Owner / Responsible Party (optional)\n"
        
#         """You are responsible for conducting a comprehensive risk assessment of the uploaded Project Report. 
#     The report contains detailed project descriptions, including architectural decisions, integration points, 
#     tooling dependencies, and development methodologies. Your analysis must be structured and thorough, 
#     covering all major risk categories using the provided evaluation framework.

#     Framework for Analysis:
#     1. Strategic Risks:
#        - Misalignment with business goals.
#        - Scope creep or changing stakeholder priorities.
  
#   2. Technical Risks:
#        - API reliability or third-party service dependency (e.g., Stripe, Twilio).
#        - Scalability, availability, performance under load, latency, and failure tolerance risks in cloud-native deployments.

#     3. Operational Risks:
#        - Delayed procurement of critical tools (e.g., Figma, Datadog).
#        - Skill shortages or bandwidth constraints in cross-functional teams.
#        - QA and compliance process delays.

#     4. Resource & Financial Risks:
#        - Overrun of the $110K budget cap.
#        - Underestimation of resource requirements for CI/CD, DevOps, or UX testing.

#     5. Organizational & Compliance Risks:
#        - Lack of stakeholder involvement in key agile ceremonies.
#        - Changes to external regulations (e.g., GDPR, WCAG).

#     6. Assumptions & Constraints Validation:
#        - Identify risks tied to assumptions that could break.
#        - Reevaluate the impact of stated constraints.

#     7. Time and Budget Risks:
#        - Assess potential time delays in the project schedule and their cascading impact on deliverables.
#        - Evaluate risks related to exceeding the allocated project budget and implications for resource planning.

#     Evaluation Criteria:
#     - Risk Title
#     - Risk Category
#     - Likelihood (Low / Medium / High)
#     - Impact (Low / Medium / High)
#     - Mitigation Strategy
#     - Residual Risk Level (Low / Medium / High)
#     - Potential Time Delay (if applicable)
#     - Potential Budget Overrun (if applicable)
#     - Owner / Responsible Party (Optional)

#     Risk Scoring System:
#     - Low Risk: 0-3
#     - Medium Risk: 4-6
#     - High/Critical Risk: 7-10
    
    
# #     take the context fromt"""
#      """Conduct a comprehensive risk assessment **strictly grounded** in two sources:
#         1. The official Project Report (provided as a PDFKnowledgeSource) in the knowledge directory.
#         2. The previously generated market analysis findings

#         You must not introduce any information not directly supported or implied in these two sources.
#         Do not hallucinate or infer risks from general knowledge.

#         Your analysis must follow this structured framework:

#         1. Strategic Risks
#         - Misalignment with business goals
#         - Scope creep or shifting stakeholder priorities

#         2. Technical Risks
#         - Dependency on external APIs or services (e.g., Stripe, Twilio)
#         - Scalability, uptime, and cloud-native system reliability
#         - Performance under load, fault tolerance, and latency challenges

#         3. Operational Risks
#         - Procurement delays for key tools (e.g., Figma, Datadog)
#         - Gaps in team skillsets or availability across cross-functional squads
#         - QA bottlenecks or compliance hold-ups

#         4. Resource & Financial Risks
#         - Breaching the $110K budget cap
#         - Underestimation of resourcing for CI/CD, security, or UX testing

#         5. Organizational & Compliance Risks
#         - Lack of stakeholder participation in agile ceremonies
#         - Impact of changes in external regulations (GDPR, WCAG, etc.)

#         6. Assumptions & Constraints Validation
#         - Identify any assumptions that may no longer hold
#         - Reevaluate the effect of stated budget/timeline constraints

#         🚫 Avoid hypothetical risks. Ground every point in content from the project documentation or market research.

         "You are responsible for conducting a comprehensive risk assessment of a digital platform initiative.\n\n"
        "You will receive detailed input documents, including:\n"
        "- A project report outlining architectural decisions, integration points, tooling dependencies, and development methodologies.\n"
        "- A market analysis containing industry-specific risks and trends.\n"
        "- Content scraped from relevant websites to understand the competitive landscape and user expectations.\n\n"
        "### **Guardrails**\n"
        "1. **Strict Input-Driven Analysis**:\n"
        "   - Your assessment must be based **strictly and exclusively** on the information in the input documents.\n"
        "   - Do **not** introduce risks, insights, or assumptions that are not explicitly supported by the provided data.\n"
        "   - If a category or framework point lacks input data, explicitly state that it could not be assessed due to insufficient information.\n\n"
        "2. **No Hallucinations**:\n"
        "   - Avoid any generic, templated, or fabricated risks or conclusions.\n"
        "   - The final report must align directly with the evidence and context provided in the input documents.\n\n"
        "3. **Traceable and Documented Justification**:\n"
        "   - For every risk identified, include a note about which document (project report, market analysis, or scraped content) provided the supporting evidence.\n"
        "   - Example: `This risk was identified in the project report, Section 2: Tooling Dependencies.`\n\n"
        "4. **Category-Based Completeness Check**:\n"
        "   - If any category from the provided framework (e.g., Strategic, Technical, Operational, etc.) has no identified risks due to lack of input data, include a note stating:\n"
        "     `No risks identified in this category due to insufficient input data.`\n\n"
        "### **Risk Analysis Framework**\n"
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
        "**Risk Scoring Formula**\n"
        "To prioritize risks systematically, use the following formula to calculate the risk score:\n\n"
        "**Risk Score = Likelihood Weight × Impact Weight**\n\n"
        "- Likelihood Weight: Assign values based on the probability of occurrence:\n"
        "  - Low = 1\n"
        "  - Medium = 2\n"
        "  - High = 3\n"
        "- Impact Weight: Assign values based on the severity of the impact:\n"
        "  - Low = 1\n"
        "  - Medium = 2\n"
        "  - High = 3\n\n"
        "**Risk Thresholds**:\n"
        "- Low Risk: Score ≤ 2\n"
        "- Medium Risk: 3 ≤ Score ≤ 6\n"
        "- High Risk: Score ≥ 7\n\n"
        "🔚 Your final output must be a full Risk Register with:\n"
        "- Risk Title\n"
        "- Risk Category\n"
        "- Likelihood (Low / Medium / High)\n"
        "- Impact (Low / Medium / High)\n"
        "- Risk Score\n"
        "- Mitigation Strategy\n"
        "- Residual Risk Level\n"
        "- Owner / Responsible Party (optional)\n"
        "- Supporting Document and Reference (mandatory)\n\n"
        "**Important:** Any failure to adhere to these guardrails will result in an invalid report."
    ),
    expected_output=(
               "A full risk register in markdown table format or JSON, following the framework above. "
        "Each risk entry must include title, category, likelihood, impact, risk score, mitigation, residual risk, and supporting document references. "
        "The report must be based strictly on the input documents provided."


    ),
    context=[analyze_scraped_content_task],
    output_file="output/risk_register.md",
    human_input=True,
    agent=risk_assessment_agent
)


