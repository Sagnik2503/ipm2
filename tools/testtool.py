# import os
# from typing import Type, List, Dict
# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool
# from langchain_tavily import TavilySearch


# class TavilyScrapeToolInput(BaseModel):
#     """Input schema for TavilyScrapeTool."""
#     urls: List[str] = Field(..., description="A list of URLs to scrape content from.")


# class TavilyScrapeTool(BaseTool):
#     name: str = "Tavily Website Scraper"
#     description: str = (
#         "Uses the TavilySearch tool to scrape content from a list of provided URLs. "
#         "Returns the title, URL, content snippet, and raw content for each webpage."
#     )
#     args_schema: Type[BaseModel] = TavilyScrapeToolInput

#     def _run(self, urls: List[str]) -> List[Dict[str, str]]:
#         """
#         Scrapes content from the provided list of URLs.

#         Args:
#             urls (list): A list of URLs to scrape.

#         Returns:
#             list[dict]: A list of dictionaries with the scraped content.
#         """
#         if not urls:
#             return [{"error": "No URLs provided for scraping."}]

#         # Initialize Tavily Search Tool
#         tavily_tool = TavilySearch(
#             api_key=os.getenv("TAVILY_API_KEY"),
#             max_results=5,
#             topic="general",
#             include_raw_content=True
#         )

#         scraped_results = []

#         for url in urls:
#             try:
#                 # Perform the search with the URL as a query
#                 response = tavily_tool.invoke({"query": url})
#                 results = response.get("results", [])

#                 if not results:
#                     scraped_results.append({"url": url, "message": "No content found."})
#                     continue

#                 # Append the results for each URL
#                 for result in results:
#                     scraped_results.append({
#                         "url": url,
#                         "title": result.get("title", "No Title"),
#                         "link": result.get("url", "No Link"),
#                         "snippet": result.get("content", "No Snippet"),
#                         "raw_content": result.get("raw_content", "No Raw Content"),
#                     })
#             except Exception as e:
#                 scraped_results.append({"url": url, "error": str(e)})

#         return scraped_results


# # ✅ MAIN FUNCTION FOR TESTING
# if __name__ == "__main__":
#     # Ensure the Tavily API key is set
#     if not os.getenv("TAVILY_API_KEY"):
#         raise ValueError("⚠️ TAVILY_API_KEY not found in environment. Please set it in your .env file.")

#     # Create an instance of the tool
#     scraper_tool = TavilyScrapeTool()

#     # Define your test input
#     test_urls = [
#         "https://example.com",
#         "https://www.wikipedia.org",
#         "https://www.openai.com"
#     ]

#     # Run the tool with the input
#     print("\n🔍 Scraping content for URLs:\n")
#     result = scraper_tool._run(urls=test_urls)

#     # Display results
#     print("📰 Returned Results:\n")
#     print(result)
#     print("\n📦 Type of returned data:", type(result))


#Try 2
# import os
# from dotenv import load_dotenv
# from typing import Type, List, Dict
# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool
# from langchain_tavily import TavilySearch

# # Load environment variables
# load_dotenv()

# class TavilySearchAndScrapeToolInput(BaseModel):
#     """Input schema for TavilySearchAndScrapeTool."""
#     query: str = Field(..., description="Search query to find relevant URLs.")
#     num_results: int = Field(10, description="Number of URLs to retrieve and scrape.")

# class TavilySearchAndScrapeTool(BaseTool):
#     name: str = "Tavily Search and Scrape Tool"
#     description: str = (
#         "Uses TavilySearch to search for URLs based on a query and then scrapes content "
#         "from the retrieved URLs. Returns detailed information about the scraped content."
#     )
#     args_schema: Type[BaseModel] = TavilySearchAndScrapeToolInput

#     def _run(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
#         """
#         Searches for URLs based on the query and scrapes the retrieved URLs for content.

#         Args:
#             query (str): The search query.
#             num_results (int): The number of URLs to scrape.

#         Returns:
#             list[dict]: A list of dictionaries with search and scrape results.
#         """
#         if not query:
#             return [{"error": "No query provided for search."}]

#         # Initialize Tavily Search Tool
#         tavily_tool = TavilySearch(
#             api_key=os.getenv("TAVILY_API_KEY"),
#             max_results=num_results,
#             topic="general",
#             include_raw_content=True
#         )

#         # Step 1: Search for URLs using TavilySearch
#         try:
#             search_response = tavily_tool.invoke({"query": query})
#             search_results = search_response.get("results", [])
#         except Exception as e:
#             return [{"error": f"Search failed with error: {str(e)}"}]

#         if not search_results:
#             return [{"error": "No search results found for the query."}]

#         # Extract URLs from search results
#         urls_to_scrape = [result.get("url") for result in search_results if result.get("url")]

#         if not urls_to_scrape:
#             return [{"error": "No valid URLs found to scrape."}]

#         # Step 2: Scrape content from the retrieved URLs using TavilySearch
#         scraped_results = []
#         for url in urls_to_scrape:
#             try:
#                 # Perform scraping with the URL
#                 response = tavily_tool.invoke({"query": url})
#                 results = response.get("results", [])

#                 if not results:
#                     scraped_results.append({"url": url, "message": "No content found."})
#                     continue

#                 # Append the results for each URL
#                 for result in results:
#                     scraped_results.append({
#                         "searched_url": url,
#                         "title": result.get("title", "No Title"),
#                         "link": result.get("url", "No Link"),
#                         "snippet": result.get("content", "No Snippet"),
#                         "raw_content": result.get("raw_content", "No Raw Content"),
#                     })
#             except Exception as e:
#                 scraped_results.append({"url": url, "error": str(e)})

#         return scraped_results


# # ✅ MAIN FUNCTION FOR TESTING
# if __name__ == "__main__":
#     # Ensure the Tavily API key is set
#     if not os.getenv("TAVILY_API_KEY"):
#         raise ValueError("⚠️ TAVILY_API_KEY not found in environment. Please set it in your .env file.")

#     # Create an instance of the tool
#     search_and_scrape_tool = TavilySearchAndScrapeTool()

#     # Define your test input
#     test_query = "Artificial Intelligence trends"
#     num_results = 5

#     # Run the tool with the input
#     print(f"\n🔍 Searching and Scraping for: {test_query}\n")
#     result = search_and_scrape_tool._run(query=test_query, num_results=num_results)

#     # Display results
#     print("📰 Returned Results:\n")
#     print(result)
#     print("\n📦 Type of returned data:", type(result))


# Try 3

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type, List, Dict
from crewai.tools import BaseTool
from langchain_tavily import TavilySearch

# Load environment variables
load_dotenv()

# -----------------------------------------
# Tavily Search Tool
# -----------------------------------------

class TavilySearchToolInput(BaseModel):
    """Input schema for TavilySearchTool."""
    query: str = Field(..., description="Search query to find relevant URLs.")
    num_results: int = Field(10, description="Number of URLs to retrieve.")

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search Tool"
    description: str = (
        "Uses TavilySearch to find relevant URLs based on a query. "
        "Returns a list of URLs and related metadata."
    )
    args_schema: Type[BaseModel] = TavilySearchToolInput

    def _run(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Searches for URLs based on the query.

        Args:
            query (str): The search query.
            num_results (int): The number of URLs to retrieve.

        Returns:
            list[dict]: A list of dictionaries with search results.
        """
        if not query:
            return [{"error": "No query provided for search."}]

        # Initialize Tavily Search Tool
        tavily_tool = TavilySearch(
            api_key=os.getenv("TAVILY_API_KEY"),
            max_results=num_results,
            topic="general",
            include_raw_content=False  # Not needed for search-only
        )

        try:
            # Perform the search
            response = tavily_tool.invoke({"query": query})
            search_results = response.get("results", [])

            if not search_results:
                return [{"error": "No search results found for the query."}]

            # Extract URLs and metadata
            return [
                {"title": result.get("title", "No Title"), "url": result.get("url", "No URL")}
                for result in search_results
            ]
        except Exception as e:
            return [{"error": f"Search failed with error: {str(e)}"}]

# -----------------------------------------
# Tavily Scrape Tool
# -----------------------------------------

class TavilyScrapeToolInput(BaseModel):
    """Input schema for TavilyScrapeTool."""
    urls: List[str] = Field(..., description="A list of URLs to scrape content from.")

class TavilyScrapeTool(BaseTool):
    name: str = "Tavily Scrape Tool"
    description: str = (
        "Uses TavilySearch to scrape content from a list of provided URLs. "
        "Returns the title, URL, content snippet, and raw content for each webpage."
    )
    args_schema: Type[BaseModel] = TavilyScrapeToolInput

    def _run(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Scrapes content from the provided list of URLs.

        Args:
            urls (list): A list of URLs to scrape.

        Returns:
            list[dict]: A list of dictionaries with the scraped content.
        """
        if not urls:
            return [{"error": "No URLs provided for scraping."}]

        # Initialize Tavily Search Tool
        tavily_tool = TavilySearch(
            api_key=os.getenv("TAVILY_API_KEY"),
            max_results=5,
            topic="general",
            include_raw_content=True
        )

        scraped_results = []

        for url in urls:
            try:
                # Perform scraping with the URL
                response = tavily_tool.invoke({"query": url})
                results = response.get("results", [])

                if not results:
                    scraped_results.append({"url": url, "message": "No content found."})
                    continue

                # Append the results for each URL
                for result in results:
                    scraped_results.append({
                        "url": url,
                        "title": result.get("title", "No Title"),
                        "snippet": result.get("content", "No Snippet"),
                        "raw_content": result.get("raw_content", "No Raw Content"),
                    })
            except Exception as e:
                scraped_results.append({"url": url, "error": str(e)})

        return scraped_results

# -----------------------------------------
# Test Script
# -----------------------------------------

if __name__ == "__main__":
    # Ensure the Tavily API key is set
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("⚠️ TAVILY_API_KEY not found in environment. Please set it in your .env file.")

    # Step 1: Test the Search Tool
    search_tool = TavilySearchTool()
    search_query = "Artificial Intelligence trends"
    search_results = search_tool._run(query=search_query, num_results=5)

    print("\n🔍 Search Results:\n")
    print(search_results)

    # Step 2: Test the Scrape Tool (using URLs from search results)
    if isinstance(search_results, list) and "url" in search_results[0]:
        urls_to_scrape = [result["url"] for result in search_results]
        scrape_tool = TavilyScrapeTool()
        scrape_results = scrape_tool._run(urls=urls_to_scrape)

        print("\n📰 Scraped Results:\n")
        print(scrape_results)
