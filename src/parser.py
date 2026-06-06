from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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


def find_sku_position(query: str, sku: str, max_results: int = 100):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.get(create_url(query))
    time.sleep(5)
    
    found = []
    unique = set()
    last_count = 0
    
    while len(found) < max_results:
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
        
        for link in links:
            if len(found) >= max_results:
                break
            href = link.get_attribute("href")
            product_sku = extract_sku(href)
            if product_sku and product_sku not in unique:
                found.append(product_sku)
                unique.add(product_sku)
                
                if product_sku == sku:
                    driver.quit()
                    return Result(
                        query=query,
                        sku=sku,
                        position=len(found),
                        page=1,
                        total_checked=len(found),
                        timestamp=datetime.now()
                )
        
        # Скроллим до последнего элемента
        if links:
            driver.execute_script("arguments[0].scrollIntoView(true);", links[-1])
        
        time.sleep(2)
        
        # Если количество не увеличилось - выходим
        if len(found) == last_count:
            break
        last_count = len(found)
    
    driver.quit()
    return Result(
            query=query,
            sku=sku,
            position="not_found",
            page=None,
            total_checked=len(found),
            timestamp=datetime.now()
        )