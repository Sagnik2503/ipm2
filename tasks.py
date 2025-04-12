from crewai import Task
from models import Report,OrganicResult,SerperSearchResults
from pydantic import BaseModel, Field
from typing import List, Dict
# from agents import news_scraper, market_analysis, document_info_agent, risk_assessment_agent
from app import document_info_agent, market_analysis, news_scraper, risk_assessment_agent, final_integration_agent
class NewsSearchResults(BaseModel):
    """Schema for the output of market analysis task."""
    query: str = Field(..., description="Search query used to find the news articles.")
    urls: List[str] = Field(..., description="List of URLs retrieved by the search tool.")

document_query_task = Task(
    description=(
        "Your task is to analyze the provided document and extract all the relevant information "
        "based on the Report model schema. Focus particularly on accurately extracting team members, their roles, "
        "and responsibilities from the 'Project Team & Responsibilities' section. Ensure that each extracted field "
        "is comprehensive and adheres to the schema."
    ),
    expected_output=(
        "A structured JSON file with all the details extracted from the document, formatted precisely according to "
        "the Report model schema. Pay special attention to the 'team_members' and 'responsibilities' fields: "
        "'team_members' should be formatted as 'Name (Role)', and 'responsibilities' should list each name with "
        "their detailed responsibilities."
        "Contain limitations, future_scope, dependencies, assumptions, constraints operational_thresholds" "communication_protocols" "tools_used" "change_management" "approval_matrix"
        "DO not miss any section that is mentioned in the Report model schema."
        "the budget should contain both the total budget section wise and the budget cap"
        
    ),
    output_pydantic=Report,
    agent=document_info_agent,
    output_file="output/project_overview.json"
)




market_analysis_task = Task(
    description=(
        "You are a market analyst performing research on a specific project.\n\n"
        "Your job is to analyze the latest market news, risks, and opportunities relevant to the project summary provided below.\n"
        "To do this, you must use the 'TavilySearchTool', which retrieves the most recent news articles.\n\n"
        "Instructions:\n"
        "1. Convert the project description into a concise, relevant search query.\n"
        "2. Call the `TavilySearchTool` using the query. Example input: `query='AI startup in healthcare'`.\n"
        "3. Use the returned news articles to identify key trends, competitor activity, and potential risks.\n"
        "4. Return the final result as structured JSON with the search query and list of URLs.\n\n"
        "Project Summary:\n"
        "{document_query_task}"
    ),
    expected_output="A structured JSON containing the search query and URLs for further analysis.",
    output_pydantic=NewsSearchResults,
    agent=market_analysis,
    context=[document_query_task],
    output_file="output/market_analysis.json"
)


analyze_scraped_content_task = Task(
    description=(
        "You are tasked with producing a comprehensive Market Intelligence Report "
        "based on the full article content scraped from high-authority sources.\n\n"
        "Instructions:\n"
        "- Scrape the full content of each website URL provided in the input.\n"
        "- Extract key trends, risks, and opportunities discussed across all sources.\n"
        "- Structure the insights into a well-formatted markdown report.\n\n"
        "### Expected Structure of the Markdown Report:\n\n"
        "1. **Executive Summary**\n"
        "   - A high-level summary for decision-makers summarizing the key insights.\n\n"
        "2. **Market Trends**\n"
        "   - List and describe key market trends with examples.\n"
        "   - Format: `- **Trend Name**: Description`\n\n"
        "3. **Risks**\n"
        "   - Identify potential risks and describe their impact.\n"
        "   - Format: `- **Risk Name**: Description`\n\n"
        "4. **Opportunities**\n"
        "   - Highlight growth opportunities with explanations.\n"
        "   - Format: `- **Opportunity Name**: Description`\n\n"
        "5. **Competitors**\n"
        "   - List notable competitors and their strengths.\n"
        "   - If no competitors are found, state: 'No competitors identified.'\n\n"
        "6. **Actionable Recommendations**\n"
        "   - Provide strategic recommendations based on the analysis.\n"
        "   - Format: `- Recommendation`\n\n"
        "7. **Sources**\n"
        "   - Include a bulleted list of all articles used, with titles and URLs.\n"
        "   - Format: `- [Title](URL)`\n\n"
        "### Formatting Guidelines:\n"
        "- Use proper markdown syntax for headings and bullets.\n"
        "- Maintain a formal and professional tone.\n"
        "- Ensure clarity and conciseness for C-suite decision-makers.\n\n"
        "Input: List of URLs retrieved from the previous task.\n"
        "Output: A markdown-formatted market analysis report."
    ),
    expected_output="A markdown-formatted market analysis report with the specified structure. also contain the links that you have scraped",
    agent=news_scraper,
    context=[market_analysis_task],
    output_file="output/analysis_report.md"
)






project_risk_assessment_task = Task(
    description=(

         "You are responsible for conducting a comprehensive risk assessment of a digital platform initiative.\n\n"
        "You will receive detailed input documents, including:\n"
        "- A project report outlining architectural decisions, integration points, tooling dependencies, and development methodologies.\n"
        "- A market analysis containing industry-specific risks and trends.\n"
        "- Content scraped from relevant websites to understand the competitive landscape and user expectations.\n\n"
        "### *Guardrails*\n"
        "1. *Strict Input-Driven Analysis*:\n"
        "   - Your assessment must be based *strictly and exclusively* on the information in the input documents.\n"
        "   - Do *not* introduce risks, insights, or assumptions that are not explicitly supported by the provided data.\n"
        "   - If a category or framework point lacks input data, explicitly state that it could not be assessed due to insufficient information.\n\n"
        "2. *Role-Specific Analysis Only*:\n"
        "   - Roles (e.g., 'Product Manager', 'Operations Manager') included in the risk register must be *strictly derived* from the input documents.\n"
        "   - If a role is not mentioned in the project report, market analysis, or scraped content, *do not assign risks to that role*.\n"
        "   - Example: If the input documents do not reference a 'Financial Manager' or 'Compliance Officer,' these roles must not appear in the risk register.\n\n"
        "3. *No Hallucinations*:\n"
        "   - Avoid any generic, templated, or fabricated risks or conclusions.\n"
        "   - The final report must align directly with the evidence and context provided in the input documents.\n\n"
        "4. *Traceable and Documented Justification*:\n"
        "   - For every risk identified, include a note about which document (project report, market analysis, or scraped content) provided the supporting evidence.\n"
        "   - Example: ⁠ This risk was identified in the project report, Section 2: Tooling Dependencies. ⁠\n\n"
        "5. *Category-Based Completeness Check*:\n"
        "   - If any category from the provided framework (e.g., Strategic, Technical, Operational, etc.) has no identified risks due to lack of input data, include a note stating:\n"
        "     ⁠ No risks identified in this category due to insufficient input data. ⁠\n\n"
        "### *Risk Analysis Framework*\n"
        "*1. Strategic Risks*\n"
        "- Misalignment with business goals\n"
        "- Scope creep or changing stakeholder priorities\n\n"
        "*2. Technical Risks*\n"
        "- API reliability or third-party service dependency (e.g., Stripe, Twilio)\n"
        "- Scalability and availability risks in cloud-native deployments\n"
        "- Performance under load, latency, and failure tolerance\n\n"
        "*3. Operational Risks*\n"
        "- Delayed procurement of critical tools (e.g., Figma, Datadog)\n"
        "- Skill shortages or bandwidth constraints in cross-functional teams\n"
        "- QA and compliance process delays\n\n"
        "*4. Resource & Financial Risks*\n"
        "- Overrun of $110K budget cap\n"
        "- Underestimation of resource requirements for CI/CD, DevOps, or UX testing\n\n"
        "*5. Organizational & Compliance Risks*\n"
        "- Lack of stakeholder involvement in key agile ceremonies\n"
        "- Changes to external regulations (e.g., GDPR, WCAG)\n\n"
        "*6. Assumptions & Constraints Validation*\n"
        "- Identify if any listed assumptions could break\n"
        "- Reevaluate the impact of stated constraints\n\n"
        "*Risk Scoring Formula*\n"
        "To prioritize risks systematically, use the following formula to calculate the risk score:\n\n"
        "*Risk Score = Likelihood Weight × Impact Weight*\n\n"
        "- Likelihood Weight: Assign values based on the probability of occurrence:\n"
        "  - Low = 1\n"
        "  - Medium = 2\n"
        "  - High = 3\n"
        "- Impact Weight: Assign values based on the severity of the impact:\n"
        "  - Low = 1\n"
        "  - Medium = 2\n"
        "  - High = 3\n\n"
        "*Risk Thresholds*:\n"
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
        "- Owner / Responsible Party (only if the role is mentioned in the input documents)\n"
        "- Supporting Document and Reference (mandatory)\n\n"
        "*Important:* Any failure to adhere to these guardrails will result in an invalid report."

    ),
    expected_output=(
               "A full risk register in markdown table format or JSON, following the framework above. "
        "Each risk entry must include title, category, likelihood, impact, risk score, mitigation, residual risk, and supporting document references. "
        "Roles for owners/responsible parties must only include those explicitly mentioned in the input documents. "
        "The report must be based strictly on the input documents provided."



    ),
    context=[analyze_scraped_content_task],
    output_file="output/risk_register.md",
    #human_input=True,
    agent=risk_assessment_agent
)
# Final Integration Task
final_integration_task = Task(
    description=(
        "Your task is to synthesize insights from multiple sources and provide a comprehensive final deliverable for decision-makers.\n\n"

        "### 🔍 Inputs:\n"
        "- The **Project Document Details** extracted from the document query task.\n"
        "- **Market Trends, Risks, and Opportunities** from the market analysis task.\n"
        "- **Detailed Analysis of Scraped Content** summarizing insights from authoritative sources.\n"
        "- **Risk Assessment Findings** evaluating potential risks and mitigation strategies for the project.\n\n"

        "### 📋 Instructions:\n"
        "1. Carefully read and integrate the findings from each input context.\n"
        "2. Synthesize these inputs into a well-structured, professional-grade report that includes:\n"
        "- An **Executive Summary** of key findings and recommendations.\n"
        "- A detailed section on **Market Analysis and Trends** based on the news analysis and scraped content.\n"
        "- A **Risk Register** summarizing and categorizing risks with proposed mitigation strategies.\n"
        "- **Actionable Recommendations** tailored for the project's stakeholders.\n"
        "3. Ensure that all insights are explicitly grounded in the provided input contexts.\n\n"

        "### ✅ Required Structure:\n"
        "**1. Executive Summary**\n"
        "- High-level summary of findings and actionable recommendations.\n\n"

        "**2. Market Analysis**\n"
        "- Major trends, opportunities, and risks identified in the news and scraped content.\n"
        "- Data points or direct quotes with references where possible.\n\n"

        "**3. Risk Register**\n"
        "- Summarized risk analysis with clear categorization, likelihood, impact, and mitigation strategies.\n"
        "- Include a markdown table or structured JSON format.\n\n"

        "**4. Recommendations**\n"
        "- Specific, actionable recommendations based on synthesized findings.\n"
        "- Align these with the project's strategic goals and risks.\n\n"

        "**5. References and Citations**\n"
        "- Include a bulleted list of all referenced documents and articles.\n"
        "- Format references with hyperlinks in markdown.\n\n"
        "- include all the links that you have scraped"
    ),
    expected_output=(
        "A comprehensive, professional-grade report in markdown format, structured as outlined above."
        "Each section should be EXTREMLY ELABORATE and have proper well defined and well written paragraphs."
        "it should have a table of contents."
        "it should have a risk register table that contains the risks and the mitigation strategies with the respective goal and everything mentioned in the {description}."
        "**keep in mind that the report should be at least 1500 words.**"
        "it should have all the reference links of the scraped websites"
        "**Use the Word Count Tool to ensure the report is at least 1500 words.**"
        "Example structure: \n"
        
        "### ✅ Required Structure:\n"
        "**1. Executive Summary**\n"
        "- High-level summary of findings and actionable recommendations.\n\n"

        "**2. Market Analysis**\n"
        "- Major trends, opportunities, and risks identified in the news and scraped content.\n"
        "- Data points or direct quotes with references where possible.\n\n"

        "**3. Risk Register**\n"
        "- Summarized risk analysis with clear categorization, likelihood, impact, and mitigation strategies.\n"
        "- Include a markdown table or structured JSON format.\n\n"

        "**4. Recommendations**\n"
        "- Specific, actionable recommendations based on synthesized findings.\n"
        "- Align these with the project's strategic goals and risks.\n\n"

        "**5. References and Citations**\n"
        "- Include a bulleted list of all referenced documents and articles.\n"
        "- Format references with hyperlinks in markdown.\n\n"
        "- include all the links that you have scraped"

        "But you can make it more descriptive and more accurate from a business perspective"
    ),
    context=[
        document_query_task,
        market_analysis_task,
        analyze_scraped_content_task,
        project_risk_assessment_task,
    ],
    output_file="output/final_report.md",
    agent=final_integration_agent,
)

