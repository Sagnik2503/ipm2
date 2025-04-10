import requests
import json
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
from dotenv import load_dotenv
load_dotenv()

# class SerperNewsToolInput(BaseModel):
#     """Input schema for Serper News Tool."""
#     query: str = Field(
#         description="A brief or overview of the project"
#     )

# class SerperNewsTool(BaseTool):
#     name: str = "Serper News Extraction Tool"
#     description: str = (
#         "Retrieves the most recent and relevant news articles related to the project description using the Serper API."
#     )
#     args_schema: Type[BaseModel] = SerperNewsToolInput
#     _api_key: str = PrivateAttr()  # Private attribute for the API key

#     def __init__(self, api_key: str = None):
#         """
#         Initialize the tool with an API key.
#         If no key is provided, it attempts to read from the environment variable.
#         """
#         super().__init__()
#         self._api_key = api_key or os.getenv("SERPER_API_KEY")
#         if not self._api_key:
#             raise ValueError("Serper API key is required. Set SERPER_API_KEY environment variable.")

#     def _run(self, query: str):
#         """Fetch news articles using the Serper API and return JSON data."""
#         print(f"🧪 Running SerperNewsTool with query: {query}")
#         gl = "in"   # Country code (India)
#         tbs = "qdr:w"  # Time range (last week)

#         url = "https://google.serper.dev/news"
#         payload = json.dumps({
#             "q": query,
#             "gl": gl,
#             "tbs": tbs,
#             "num": 15
#         })
#         headers = {
#             'X-API-KEY': self._api_key,
#             'Content-Type': 'application/json'
#         }

#         response = requests.post(url, headers=headers, data=payload)

#         # Handle response errors
#         if response.status_code != 200:
#             error_message = {
#                 "error": f"Received {response.status_code} from API",
#                 "details": response.text
#             }
#             print(json.dumps(error_message, indent=2))
#             return error_message

#         data = response.json()
#         news_articles = data.get("news", [])

#         # Format and return news articles
#         if not news_articles:
#             print("No news articles found.")
#             return []

#         # formatted_results = []
#         # for article in news_articles:
#         #     formatted_article = (
#         #         f"📌 **{article['title']}**\n"
#         #         f"🔗 [Read More]({article['link']})\n"
#         #         f"🗞 Source: {article['source']} | 📅 Date: {article['date']}\n"
#         #         f"📝 {article['snippet']}\n"
#         #     )
#         #     formatted_results.append(formatted_article)

#         return news_articles


# # ✅ MAIN FUNCTION FOR TESTING
# if __name__ == "__main__":
#     # Make sure you have SERPER_API_KEY set in your environment
#     news_tool = SerperNewsTool(api_key=os.getenv('SERPER_API_KEY'))
#     news_results = news_tool._run(query="market trends and financial news")

#     print("\n\nReturned Results:\n")
#     print(news_results)
#     print("\n\nType of returned data:", type(news_results))

import requests
import json
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class SerperNewsToolInput(BaseModel):
    """Input schema for SerperNewsTool."""
    query: str = Field(..., description="A short and concise search query to find recent news about a topic.")


class SerperNewsTool(BaseTool):
    name: str = "Serper News Tool"
    description: str = (
        "Uses the Serper.dev API to retrieve the most recent news articles based on a provided query. "
        "Returns only the 'news' list from the response."
    )
    args_schema: Type[BaseModel] = SerperNewsToolInput

    def _run(self, query: str) -> list:
        print(f"🧪 Running SerperNewsTool with query: {query}")
        url = "https://google.serper.dev/news"
        payload = json.dumps({
            "q": query,
            "tbs": "qdr:w",
            "num": 20,
            "gl": "in",  
            "page": 2
        })
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code != 200:
            return {
                "error": f"Failed with status {response.status_code}",
                "details": response.text
            }

        data = response.json()

        # ✅ Return only the 'news' key
        return data.get("news", [])

# ✅ MAIN FUNCTION FOR TESTING
if __name__ == "__main__":
    # Ensure your environment variable is set
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        raise ValueError("⚠️ SERPER_API_KEY not found in environment. Please set it in your .env file.")

    # Create an instance of the tool
    news_tool = SerperNewsTool()

    # Define your test query
    test_query = "Apple Inc market trends"

    # Run the tool with the query
    print(f"\n🔍 Querying news for: {test_query}\n")
    result = news_tool._run(query=test_query)

    # Display results
    print("📰 Returned Results:\n")
    print(result)
    print("\n📦 Type of returned data:", type(result))
