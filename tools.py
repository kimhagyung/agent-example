import time
from crewai.tools import tool
from crewai_tools import SerperDevTool
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup #html을 다루고 조작하는것

search_tool = SerperDevTool(n_results = 30)

@tool
def scrape_tool(url: str): # agent가 읽어야 하는 웹사이트 url
    """
    Use this when you need to read the content of a website.
    Returns the content of a website, in case the website is not available, it returns 'No content'.
    Input should be a `url` string. for example (https://www.reuters.com/world/asia-pacific/thailand-demands-apology-cambodia-over-landmine-incident-2025-11-12/)
    """ 
    # 웹사이트의 컨텐츠를 반환해 비어있으면 반환하지마
    # input url 은 string 이어야해 

    print(f"Scrapping URL: {url}")

    # 1. 브라우져 켠다 
    # 2. 페이지이동 
    # 3. 페이지 html 추출
    # 4. html 정리 (우리가 필요한건 main이니깐 head, footer 정리)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)  # 브라우져 창없이 백그라운드 실행 
        page = browser.new_page() # 새페이지를 열고 

        page.goto(url) # 원하는 url로이동  
        time.sleep(5) # 5초동안 위의상황 마무리  
        html = page.content() #html 추출 
        browser.close()

        soup = BeautifulSoup(html, "html.parser")

        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]

        # 원치않은 태그 제거 
        for tag in soup.find_all(unwanted_tags):
            tag.decompose()
        
        content = soup.get_text(separator=" ")  #html태그 제거 후 , 구분자 공백
        return content if content !="" else "No content"