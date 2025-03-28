import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

def scrape_profiles(li_at, search_link, max_results):
    options = Options()
    options.binary_location = "/opt/render/project/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.set_page_load_timeout(180)
    driver.implicitly_wait(10)

    data = []

    try:
        driver.get("https://www.linkedin.com")
        time.sleep(5)
        driver.add_cookie({"name": "li_at", "value": li_at, "domain": ".linkedin.com"})
        driver.refresh()
        time.sleep(10)
        driver.get(search_link)
        time.sleep(5)

        results_scraped = 0

        while results_scraped < max_results:
            for _ in range(5):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(2)

            list_items = driver.find_elements(By.CSS_SELECTOR, '.search-results-container .list-style-none li')

            if not list_items:
                break

            for profile in list_items:
                if results_scraped >= max_results:
                    break
                try:
                    profil_link = profile.find_element(By.CSS_SELECTOR, 'a[data-test-app-aware-link]').get_attribute('href')
                    profil_name = profile.find_element(By.CSS_SELECTOR, 'a span[aria-hidden="true"]').text
                    profil_job = profile.find_element(By.CSS_SELECTOR, 'div.t-14.t-black.t-normal').text
                    profil_local = profile.find_element(By.CSS_SELECTOR, 'div.t-14.t-normal:not(.t-black)').text
                    span_element = profile.find_element(By.CSS_SELECTOR, 'p.entity-result__summary--2-lines > span.white-space-pre:nth-of-type(2)')
                    current_company = driver.execute_script("""
                        var element = arguments[0];
                        if (element.nextSibling) {
                            return element.nextSibling.textContent.trim();
                        }
                        return '';
                    """, span_element)

                    data.append({
                        "Name": profil_name,
                        "Job": profil_job,
                        "Company": current_company,
                        "Link": profil_link,
                        "Location": profil_local
                    })

                    results_scraped += 1
                    time.sleep(3)

                except Exception as e:
                    print(f"Error extracting profile: {e}")

            try:
                next_button = driver.find_element(By.XPATH, '//button[@aria-label="Suivant"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                next_button.click()
                time.sleep(5)
            except:
                break

    finally:
        driver.quit()

    return data
