from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class WordCounterInput(BaseModel):
    """Input schema for the WordCounterTool."""
    text: str = Field(..., description="The text to count words in.")
    
class WordCounterTool(BaseTool):
    name: str ="Word Count Tool"
    description: str = "Counts the number of words in a given text."
    args_schema: type[BaseModel] = WordCounterInput

    def _run(self, text: str) -> int:
        words = text.split()
        return len(words)
    