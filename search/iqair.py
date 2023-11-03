from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def scrape_table_data(driver, number):
    # result_elements = driver.find_elements(By.XPATH, '//*[@id="content-wrapper"]/app-ranking/div/div/div[3]/div/table/tbody/tr')
    # total_items = len(result_elements)

    results = []

    for item_id in range(1, number):
        try:
            flag = driver.find_element(By.XPATH, f'//*[@id="content-wrapper"]/app-ranking/div/div/div[3]/div/table/tbody/tr[{item_id}]/td[2]/img').get_attribute('src')
            city = driver.find_element(By.XPATH, f'//*[@id="content-wrapper"]/app-ranking/div/div/div[3]/div/table/tbody/tr[{item_id}]/td[3]/a')
            score = driver.find_element(By.XPATH, f'//*[@id="content-wrapper"]/app-ranking/div/div/div[3]/div/table/tbody/tr[{item_id}]/td[4]/div')

            results.append({
                "flag": flag,
                "city": city.text,
                "score": score.text,
            })
        except Exception as e:
            if 'DEBUG' in os.environ:
                print(f"[IQAir] Exception: {e}")
            pass

    return results

def top_ranking_air(number):
    # Initialize the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/IQAir/"
    options.add_argument(f"user-data-dir={datadir}")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.iqair.com/world-air-quality-ranking")

    try:
        driver.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/app-cookie-preferences/div/div/button[2]').click()
        print('Cookies accepted')
    except:
        pass

    most_polluted = scrape_table_data(driver, number)

    driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/app-ranking/div/div/app-ranking-nav/div/div[2]/a[2]').click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/app-ranking/div/div/div[3]/div/table/tbody/tr')))

    cleanest = scrape_table_data(driver, number)
    

    # After scraping, close the browser window

    print(most_polluted)
    print(cleanest)
    driver.quit()

top_ranking_air(10)