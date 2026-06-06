from datetime import datetime
from playwright.sync_api import sync_playwright
from urllib.parse import quote
from .models import Result

def extract_sku(link: str) -> str | None:
    if not link:
        return None
    
    link_parts = link.split("/")
    if not link_parts:
        return None
    
    sku = link_parts[-2].split("-")[-1]
    if sku.isdigit():
        return sku
    else:
        return None
    
def create_url(query: str) -> str:
    return f'https://www.ozon.ru/search/?text={quote(query)}'

def find_sku_position(query: str, sku: str, max_results: int = 100) -> Result:

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-position=9999,9999"
            ]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="ru/RU"
        )
        page = context.new_page()

        page.goto(create_url(query), wait_until="networkidle", timeout=30000)

        found = []
        unique = set()
        while len(found) < max_results:
            links = page.locator("a[href*='/product/']").all()

            for link in links:
                href = link.get_attribute("href")
                product_sku = extract_sku(href)
                if not product_sku or product_sku in unique:
                    continue
                found.append(product_sku)
                unique.add(product_sku)

                if len(found) >= max_results:
                    break

            if sku in found:
                position = found.index(sku) + 1
                browser.close()

                return Result(
                    query=query,
                    sku=sku,
                    position=position,
                    page=1,
                    total_checked=len(found),
                    timestamp=datetime.now()
                )
            
            count_before = page.locator("a[href*='/product/']").count()
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            try:
                page.wait_for_function(
                    f"""
                    () => document.querySelectorAll(
                        "a[href*='/product/']"
                    ).length > {count_before}
                    """,
                    timeout=3000
                )
            except Exception:
                break
        browser.close()

        return Result(
            query=query,
            sku=sku,
            position="not_found",
            page=None,
            total_checked=len(found),
            timestamp=datetime.now()
        )


