import os
from smolagents import tool
from playwright.sync_api import sync_playwright

@tool
def visit_page_and_extract_text(url: str) -> str:
    """
    Visits a webpage using a headless browser (Playwright), renders JavaScript, 
    and returns the visible text content. Use this to read the quiz question.
    
    Args:
        url: The URL of the webpage to visit.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            content = page.inner_text("body")
            # Also get raw HTML for link extraction
            html_content = page.content()
            browser.close()
            return f"--- TEXT CONTENT ---\n{content}\n\n--- HTML CONTENT ---\n{html_content[:10000]}"
    except Exception as e:
        return f"Error extracting text from {url}: {str(e)}"