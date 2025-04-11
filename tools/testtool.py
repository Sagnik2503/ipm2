from langchain_tavily import TavilySearch
import os

def scrape_website_content(urls: list[str]) -> list[dict]:
    """
    Scrapes website content using TavilySearch from the provided list of URLs.

    Args:
        urls (list[str]): A list of URLs to scrape content from.

    Returns:
        list[dict]: A list of dictionaries containing title, URL, content snippet, and raw content.
    """
    if not urls:
        return [{"error": "No URLs provided for scraping."}]

    # Initialize Tavily Search Tool
    tavily_tool = TavilySearch(
        max_results=5,  # Maximum number of results per query
        topic="general",  # General topic
        include_raw_content=True  # Include raw content from the web page
    )

    scraped_results = []

    for url in urls:
        try:
            # Perform the search with the URL as a query
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
                    "link": result.get("url", "No Link"),
                    "snippet": result.get("content", "No Snippet"),
                    "raw_content": result.get("raw_content", "No Raw Content"),
                })
        except Exception as e:
            scraped_results.append({"url": url, "error": str(e)})

    return scraped_results

def main():
    """
    Main function to test the scrape_website_content function.
    """
    # Example URLs to test
    urls = [
        "https://example.com",
        "https://www.wikipedia.org",
        "https://www.openai.com"
    ]

    print("Starting website scraping...\n")
    try:
        results = scrape_website_content(urls)
        print("Scraping completed.\n")
        print("Scraped Content:\n")

        for result in results:
            if "error" in result:
                print(f"URL: {result['url']} - Error: {result['error']}")
            else:
                print(f"URL: {result['url']}")
                print(f"Title: {result['title']}")
                print(f"Link: {result['link']}")
                print(f"Snippet: {result['snippet']}")
                print(f"Raw Content: {result['raw_content']}\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    # Set the Tavily API key
    if not os.getenv("TAVILY_API_KEY"):
        os.environ["TAVILY_API_KEY"] = input("Enter your Tavily API key: ")
    main()