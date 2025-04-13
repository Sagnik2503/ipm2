from crewai.tools import BaseTool
from typing import Type, List, Union
from pydantic import BaseModel, Field
import asyncio
import time
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# Enhanced Input Schema for URLScraperTool
class URLScraperToolInput(BaseModel):
    """Input schema for URLScraperTool."""
    urls: Union[List[str], str] = Field(..., description="URL or list of URLs to crawl.")
    max_concurrent: int = Field(default=3, description="Maximum number of concurrent crawl operations.")

# Enhanced URL Scraper Tool for your workflow
class URLScraperTool(BaseTool):
    name: str = "URL Scraper"
    description: str = (
        "This tool is useful for crawling normal URLs and returning their full content."
    )
    args_schema: Type[BaseModel] = URLScraperToolInput
    
    async def _run(self, urls: Union[List[str], str], max_concurrent: int = 3) -> str:
        """Main execution method to crawl URLs and scrape content."""
        
        # Ensure URLs is a list
        if isinstance(urls, str):
            urls = [urls]
            
        if not urls:
            return "No URLs provided to crawl"
        
        print(f"Found {len(urls)} URLs to crawl")
        
        # Call the helper function for parallel crawling
        result = await crawl_parallel(urls, max_concurrent=max_concurrent)
        
        # Format and return the result as needed
        return result

# Parallel Crawling Logic
async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
    """Crawl multiple URLs in parallel."""
    print("\n*** Crawling URLs in parallel ***")

    # Minimal browser configuration for crawling
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Initialize the web crawler
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        success_count = 0
        fail_count = 0
        start_time = time.time()
        print(f"Start Time: {time.ctime(start_time)}")
        
        # Store the scraped contents
        website_contents = []
        
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i + max_concurrent]
            tasks = []

            for j, url in enumerate(batch):
                session_id = f"parallel_session_{i + j}"
                task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
                tasks.append(task)

            # Gather results for the current batch of URLs
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f"Error crawling {url}: {result}")
                    fail_count += 1
                    website_contents.append(f"--- FAILED TO CRAWL: {url} ---\nError: {str(result)}\n")
                elif result.success:
                    print(f"Successfully crawled {url}")
                    success_count += 1
                    
                    # Extract and return full content without truncation
                    full_content = result.markdown.raw_markdown
                    
                    # Collect the content with proper separators
                    website_contents.append(
                        f"=== BEGIN CONTENT FROM: {url} ===\n\n"
                        f"{full_content}\n\n"
                        f"=== END CONTENT FROM: {url} ===\n\n"
                    )
                    
                    print(f"Retrieved {len(full_content)} characters of content")
                else:
                    print(f"Unsuccessful crawl of {url}")
                    fail_count += 1
                    website_contents.append(f"--- UNSUCCESSFUL CRAWL: {url} ---\n")

        print(f"\nSummary:")
        print(f"  - Successfully crawled: {success_count}")
        print(f"  - Failed: {fail_count}")

        # Combine all website contents into a final string
        all_content = "\n".join(website_contents)
        
        # Add a summary header to the final result
        summary = f"CRAWL SUMMARY: Successfully crawled {success_count} URLs, failed to crawl {fail_count} URLs\n\n"
        
        return summary + all_content

    finally:
        end_time = time.time()
        print(f"End Time: {time.ctime(end_time)}")
        print(f"Total Time Taken: {end_time - start_time:.2f} seconds")
        print("\nClosing crawler...")
        await crawler.close()

# Test/Execution method for local testing
async def main():
    """Test the URLScraperTool locally."""
    # Example test URLs to crawl
    test_urls = [
        "https://github.com/graphile/starter"
    ]
    
    # Max concurrent crawls for testing
    max_concurrent = 3
    
    # Initialize the scraper tool
    scraper_tool = URLScraperTool()

    # Run the scraper tool and await the result
    print("Running scraper tool...")
    result = await scraper_tool._run(urls=test_urls, max_concurrent=max_concurrent)
    
    # Output the final result
    print("\n=== FINAL CRAWL RESULT ===")
    print(result)

if __name__ == "__main__":
    # Run the test locally using asyncio
    asyncio.run(main())
