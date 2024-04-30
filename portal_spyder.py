
### portal_spider.py with Comments

```python
from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip

class MySpider(Spider):
    name = "myspider"
    start_urls = ["http://webportal.lstractorusa.com/approval/work/apprlist/listApprDocAllAdmin.do"]

    def __init__(self):
        # Initialize Selenium WebDriver with Chrome
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def parse(self, response):
        # Navigate to the specified URL
        self.driver.get(response.url)
        # Wait for the search input to be available and set a date
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'searchStartDate')))
        self.driver.execute_script("document.getElementById('searchStartDate').value='2012.01.01'")
        # Click the search button
        self.driver.execute_script("document.getElementById('searchApListButton').click()")
        time.sleep(50)  # Delay to allow page load

        title_index = 0
        # Iterate through available titles
        while True:
            titles = self.driver.find_elements(By.CSS_SELECTOR, "td.subject a")
            if title_index >= len(titles):
                break  
                
            title = titles[title_index]
            # Scroll into view and click the title
            self.driver.execute_script("arguments[0].scrollIntoView();", title)
            title.click()
            # Wait for the document list button to be visible
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listApprDocButton")))
            time.sleep(2)  # Brief pause

            # Click to print the document, switch to new window, and wait for content
            self.driver.find_element(By.ID, "printApprDocButton").click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'td'))
            )
            # Copy document ID to clipboard and initiate print
            document_id_element = self.driver.find_element(By.XPATH, '//*[@id="contentsHeader"]/tbody/tr[1]/td[1]')
            document_id = document_id_element.text
            pyperclip.copy(document_id)
            self.driver.find_element(By.CSS_SELECTOR, "a[onclick='
