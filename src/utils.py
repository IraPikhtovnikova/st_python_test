from contextlib import contextmanager
from functools import wraps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def retry(max_attempts=5, delay=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Попытка {attempt + 1} завершилась с ошибкой: {e}. Повтор...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


@contextmanager
def create_driver(options=None):
    driver = None
    try:
        if options is None:
            options = Options()
        
        driver = webdriver.Chrome(options=options)
        yield driver
    finally:
        if driver:
            driver.quit()