from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import BaseModel
class Report(BaseModel):
    title: str = Field(..., description="The official title of the project report.")
    project_summary: str = Field(..., description="A brief summary of the project initiative.")
    objectives: List[str] = Field(..., description="Key objectives and goals of the project.")
    scope_in: List[str] = Field(..., description="Workstreams included in the project scope.")
    scope_out: List[str] = Field(..., description="Items explicitly excluded from the project scope.")
    methodology: str = Field(..., description="Development methodology and strategic approach used.")
    technologies_used: List[str] = Field(..., description="Technologies and tools used in the project.")
    system_architecture: str = Field(..., description="High-level system design and modular structure.")
    modules: List[str] = Field(..., description="Major modules or components of the platform.")
    team_members: List[str] = Field(..., description="Names and roles of team members involved in the project.")
    responsibilities: List[str] = Field(..., description="Key responsibilities assigned to each role.")
    budget_allocation: List[str] = Field(..., description="Summary of budget distribution across areas.")
    timeline_phases: List[str] = Field(..., description="Chronological phases with start and end dates.")
    milestones: List[str] = Field(..., description="Important deliverables and checkpoints.")
    deliverables: List[str] = Field(..., description="List of final outputs and documentation.")
    results: str = Field(..., description="Outcome and overall impact of the project.")
    limitations: Optional[str] = Field(None, description="Challenges or constraints faced.")
    future_scope: Optional[str] = Field(None, description="Potential enhancements or future extensions.")
    dependencies: List[str] = Field(..., description="Internal or external factors the project depends on.")
    assumptions: List[str] = Field(..., description="Assumptions made during planning.")
    constraints: List[str] = Field(..., description="Hard limitations like time, budget, compliance.")
    operational_thresholds: List[str] = Field(..., description="Defined performance and risk tolerance limits.")
    communication_protocols: List[str] = Field(..., description="Tools and routines used for team communication.")
    tools_used: List[str] = Field(..., description="Comprehensive list of software/tools used.")
    change_management: str = Field(..., description="Process for managing project changes.")
    approval_matrix: List[str] = Field(..., description="List of approvers and their responsibilities.")
    conclusion: str = Field(..., description="Final remarks and project summary.")

class OrganicResult(BaseModel):
    title: str
    link: str = Field(..., description="URL to the search result")
    snippet: Optional[str]
    position: Optional[int]

class SerperSearchResults(BaseModel):
    organic: List[OrganicResult]

class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the news article.")
    link: str = Field(..., description="Direct link to the news article.")
    snippet: str = Field(..., description="A short snippet or excerpt from the article.")
    date: str = Field(..., description="The publish date or relative time of the article.")
    source: str = Field(..., description="The source or publisher of the news.")
    imageUrl: str = Field(..., description="URL to the image associated with the news.")
    position: int = Field(..., description="The rank or position in the list of search results.")

class NewsSearchResults(BaseModel):
    news: List[NewsArticle] = Field(..., description="A list of structured news articles.")
