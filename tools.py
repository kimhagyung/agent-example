import os
import re
import time
from crewai.tools import tool
from firecrawl import FirecrawlApp

@tool
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

    max_retries = 2
    response = None

    # 1. 재시도 로직을 포함한 검색 실행
    for attempt in range(max_retries):
        try:
            print(f"\n🔎 검색 시도 중... ({attempt + 1}/{max_retries})")
            
            response = app.search(
                query=query,
                limit=5,
                scrape_options={"formats": ["markdown"]}
            )
            
            # 응답이 비어있지 않으면 성공으로 간주
            if response:
                break

        except Exception as e:
            error_msg = str(e)
            # Rate Limit 에러 시 대기
            if "Rate limit" in error_msg or "429" in error_msg:
                print(f"\n⏳ [Rate Limit] API 한도 초과. 65초 대기 후 재시도합니다...")
                time.sleep(65)
                continue
            else:
                return f"Error using tool: {error_msg}"

    if not response:
        return "Error: Search failed or returned no data."

    # 2. 데이터 추출 (여기가 핵심 수정 사항!)
    raw_data = []
    
    # 최신 firecrawl 버전은 .web 속성에 리스트를 담고 있음
    if hasattr(response, 'web'):
        raw_data = response.web
    # 혹시 구버전일 경우 .data 확인
    elif hasattr(response, 'data'):
        raw_data = response.data
    # 딕셔너리 형태로 반환된 경우
    elif isinstance(response, dict):
        raw_data = response.get('web') or response.get('data') or []
    
    if not raw_data:
        return "Error: No search results found in response."

    cleaned_chunks = []

    # 3. 데이터 정제
    for result in raw_data:
        # 객체(Object)인지 딕셔너리(Dict)인지 확인하여 안전하게 값 추출
        title = ""
        url = ""
        content = ""

        if isinstance(result, dict):
            title = result.get("title", "")
            url = result.get("url", "")
            # markdown이 없으면 description이라도 가져옴
            content = result.get("markdown", "") or result.get("description", "")
        else:
            # 객체 속성으로 접근 (getattr 사용)
            title = getattr(result, "title", "")
            url = getattr(result, "url", "")
            content = getattr(result, "markdown", "") or getattr(result, "description", "")

        if not content:
            continue
 
        # 불필요한 문자 제거
        cleaned = re.sub(r"\\+|\n+", " ", content).strip()
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

        cleaned_result = {
            "title": title,
            "url": url,
            "markdown": cleaned[:4000], # 너무 길면 잘라서 에이전트에게 전달
        }

        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks