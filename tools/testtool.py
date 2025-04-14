import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Union, Optional
from crewai.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
import time
import random
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# -----------------------------------------
# Tavily Search Tool (URL List Only)
# -----------------------------------------

class TavilySearchToolInput(BaseModel):
    """Input schema for TavilySearchTool."""
    query: str = Field(..., description="Search query to find relevant URLs.")
    num_results: int = Field(10, description="Number of URLs to retrieve.")

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search Tool"
    description: str = (
        "Uses TavilySearch to find relevant URLs based on a query. "
        "Returns only a flat list of URLs."
    )
    args_schema: Type[BaseModel] = TavilySearchToolInput

    def _run(self, query: str, num_results: int = 10) -> List[str]:
        """
        Searches for URLs based on the query.

        Args:
            query (str): The search query.
            num_results (int): The number of URLs to retrieve.

        Returns:
            list[str]: A flat list of URLs.
        """
        if not query:
            return []

        # Initialize Tavily Search Tool
        tavily_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

        try:
            # Perform the search
            response = tavily_tool.invoke({"query": query, "max_results": num_results})
            if not response:
                return []

            # Return only URLs
            return [result.get("url") for result in response if result.get("url")]
        except Exception as e:
            return [f"Error: {str(e)}"]


# -----------------------------------------
# Advanced Web Scraper Tool
# -----------------------------------------

import json
import random
import time
from typing import List, Union, Dict, Set, Type
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class RecursiveWebScraperToolInput(BaseModel):
    urls: List[str] = Field(..., description="A list of starting URLs to scrape content recursively from.")
    max_depth: int = Field(1, description="Depth of recursive scraping. Depth=0 means only the initial page.")


class TavilyScrapeTool(BaseTool):
    name: str = "Recursive Web Scraper Tool"
    description: str = (
        "Recursively scrapes content from a list of URLs. "
        "Follows internal links up to a specified depth. "
        "Returns a list of dictionaries with title, URL, and content."
    )
    args_schema: Type[BaseModel] = RecursiveWebScraperToolInput

    def __init__(self):
        super().__init__()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self._visited: Set[str] = set()

    def _extract_content(self, url: str) -> Dict[str, str]:
        try:
            time.sleep(random.uniform(1, 2))
            response = requests.get(url, headers=self._headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"

            for tag in soup(["script", "style", "header", "footer", "nav", "form", "noscript"]):
                tag.decompose()

            selectors = ["main", "article", "#content", ".content", ".post", ".article"]
            content_area = next((soup.select_one(sel) for sel in selectors if soup.select_one(sel)), soup.body)

            content = content_area.get_text(separator="\n\n", strip=True) if content_area else "No Content Available"

            return {
                "url": url,
                "title": title,
                "content": content,
                "domain": urlparse(url).netloc
            }

        except Exception as e:
            return {
                "url": url,
                "title": "Error",
                "error": str(e),
                "content": "No Content Available",
                "domain": urlparse(url).netloc if url else "unknown"
            }

    def _get_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        domain = urlparse(base_url).netloc
        internal_links = set()

        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"]
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            if parsed_url.netloc == domain and full_url not in self._visited:
                internal_links.add(full_url)

        return list(internal_links)

    def _crawl(self, url: str, depth: int) -> List[Dict[str, str]]:
        if url in self._visited or depth < 0:
            return []

        self._visited.add(url)
        result = []

        try:
            time.sleep(random.uniform(1, 2))
            response = requests.get(url, headers=self._headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"

            for tag in soup(["script", "style", "header", "footer", "nav", "form", "noscript"]):
                tag.decompose()

            content_area = next((soup.select_one(sel) for sel in ["main", "article", "#content", ".content", ".post", ".article"]
                                if soup.select_one(sel)), soup.body)

            content = content_area.get_text(separator="\n\n", strip=True) if content_area else "No Content Available"

            result.append({
                "url": url,
                "title": title,
                "content": content,
                "domain": urlparse(url).netloc
            })

            if depth > 0:
                links = self._get_internal_links(soup, url)
                for link in links:
                    result.extend(self._crawl(link, depth - 1))

        except Exception as e:
            result.append({
                "url": url,
                "title": "Error",
                "error": str(e),
                "content": "No Content Available",
                "domain": urlparse(url).netloc if url else "unknown"
            })

        return result

    def _run(self, urls: List[str], max_depth: int = 1) -> List[Dict[str, str]]:
        self._visited = set()  # Reset visited for each run
        all_results = []

        for url in urls:
            if isinstance(url, str) and url.strip():
                all_results.extend(self._crawl(url.strip(), max_depth))

        return all_results




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

    # Step 2: Test the Web Scraper Tool
    if search_results:
        # Test with direct list of URLs
        scraper_tool = TavilyScrapeTool()
        scrape_results = scraper_tool._run(urls=search_results[:2])  # Just use first 2 URLs for testing
        
        print("\n📰 Scraped Results (direct URLs):\n")
        for result in scrape_results:
            print(f"URL: {result['url']}")
            print(f"Title: {result['title']}")
            print(f"Content Preview: {result['content'][:150]}...")
            print("-" * 50)
        
        # Test with JSON format that mimics your market analysis agent output
        test_json = json.dumps({
            "query": "test query",
            "urls": search_results[:2]
        })
        scrape_results_json = scraper_tool._run(urls=test_json)
        
        print("\n📰 Scraped Results (JSON input):\n")
        for result in scrape_results_json:
            print(f"URL: {result['url']}")
            print(f"Title: {result['title']}")
            print(f"Content Preview: {result['content'][:150]}...")
            print("-" * 50)