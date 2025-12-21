import os, re
import datetime
from firecrawl import FirecrawlApp

# content(report)를 받아서 리포트용 정보를 수집하는 도구
def web_search_tool(query: str):
    """
    웹 검색 도구 (Web Search Tool)
    Args:
        query: str
            검색할 검색어 (한국어로 입력하면 더 정확합니다)
    Returns:
        Markdown 형식의 웹사이트 콘텐츠가 포함된 검색 결과 리스트
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    # 한국어 결과를 얻기 위해 lang="ko" 옵션을 추가했습니다.
    response = app.search(
        query=query,
        limit=2,
        lang="ko", 
        scrape_options={
            "formats": ["markdown"]
        }
    )

    if not response.success:
        return "도구 사용 중 오류가 발생했습니다."

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


# 수집된 content를 report.md 파일에 써주는 도구
def save_report_to_md(content: str) -> str:
    """리포트 내용을 report.md 파일로 저장합니다."""
    # [중요] 한글 깨짐 방지를 위해 encoding="utf-8"을 반드시 추가해야 합니다.
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(content)
    return "report.md 파일에 성공적으로 저장되었습니다."

if __name__ == "__main__":
    print("\n>>> [테스트 시작] 환경 변수 로드 확인 중...")
    
    test_key = os.getenv("FIRECRAWL_API_KEY")
    if test_key:
        print(f"✅ API 키 확인됨: {test_key[:5]}******")
    else:
        print("❌ API 키가 없습니다. .env 파일을 확인해주세요.")
        exit()

    print("\n>>> 1. 검색 도구 테스트 (검색어: '삼성전자 주가')")
    result = web_search_tool("삼성전자 주가")
    
    # 결과 출력 (너무 길면 잘라서 출력)
    if isinstance(result, list) and result:
        print(f"--- 검색 결과 타이틀: {result[0]['title']} ---")
        print(f"--- 내용 미리보기: {result[0]['markdown'][:200]} ...")
    else:
        print(f"--- 검색 결과: {result}")

    print("\n>>> 2. 파일 저장 테스트")
    save_res = save_report_to_md("# 테스트 성공\n\n이 파일은 tools.py 테스트 결과입니다.")
    print(f"--- 저장 결과: {save_res} ---")
    print("\n>>> [테스트 종료]")
    