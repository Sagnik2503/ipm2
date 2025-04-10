from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Union
class Report(BaseModel):
    title: str = Field(..., description="The official title of the project report.")
    project_summary: str = Field(..., description="A brief overview of the project, including its background and objectives.")
    objectives: List[str] = Field(..., description="A list of specific goals that the project aimed to achieve.")
    methodology: str = Field(..., description="Detailed explanation of the methods, technologies, or strategies used in the project.")
    technologies_used: List[str] = Field(..., description="List of tools, programming languages, or platforms used in the implementation.")
    system_architecture: Optional[str] = Field(None, description="Description or diagram of the system architecture.")
    modules: Optional[List[str]] = Field(None, description="Names or descriptions of different modules or components developed as part of the project.")
    results: str = Field(..., description="Summary of the key results or outputs of the project.")
    limitations: Optional[str] = Field(None, description="Any limitations, challenges, or issues faced during the project.")
    future_scope: Optional[str] = Field(None, description="Suggestions for future enhancements or extensions of the project.")
    conclusion: str = Field(..., description="Final remarks summarizing the overall experience and outcome of the project.")
    references: Optional[List[str]] = Field(None, description="List of external sources, papers, or documentation referred to in the report.")
    appendix: Optional[str] = Field(None, description="Any additional data, code snippets, or supporting content provided at the end of the report.")