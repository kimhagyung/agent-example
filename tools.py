import os, re
import datetime
from firecrawl import FirecrawlApp

# content(report)를 받아서 리포트용 정보를 수집하는 도구
def web_search_tool(query: str):
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
 
    response = app.search(
        query=query,
        limit=2, 
        scrape_options={
            "formats": ["markdown"]
        }
    )

    if not response.success:
        return "Error using tool."

    cleaned_chunks = []

    for result in response.data:
        title = result.get("title", "")
        url = result.get("url", "")
        markdown = result.get("markdown", "")

        # 정규표현식으로 불필요한 기호 및 공백 제거
        cleaned = re.sub(r"\\+|\n+", " ", markdown).strip()
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

        cleaned_result = {
            "title": title,
            "url": url,
            "markdown": cleaned,
        }

        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks


def save_report_to_md(content: str) -> str:
    """Save report content to report.md file."""
    with open("report.md", "w") as f:
        f.write(content)
    return "report.md"
    
