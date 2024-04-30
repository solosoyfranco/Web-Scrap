#this is to export in json the full list of articles
from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
import time
import requests
import json
import re


class MySpider(Spider):
    name = "myspider"
    # start_urls = ["http://webportal.lstractorusa.com/loginForm.do"] #solo para iniciar sesion
    start_urls = ["http://webportal.lstractorusa.com/approval/work/apprlist/listApprDocAllAdmin.do"] 
    

    def __init__(self):
        chrome_options = Options()
        # Connect to the Chrome instance running on port 9222
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

    def parse(self, response):
        self.driver.get(response.url) # este se queda
        
        # input("Press Enter after you have logged in...")
        # self.driver.get("http://webportal.lstractorusa.com/approval/work/apprMain/apprMenuView.do?uuId=3d228a6e-caba-4ff2-a11f-feb617068a86")
        # self.driver.execute_script("apprLeftMenuClick('/approval/work/apprlist/listApprDocAllAdmin.do');")
        
        
        #set the date range "searchStartDate" to 2012.01.01 with javascript
        self.driver.execute_script("document.getElementById('searchStartDate').value='2012.01.01'")
        self.driver.execute_script("document.getElementById('searchApListButton').click()")
        time.sleep(4)
        #######
        
        data = []

        # Outer loop to iterate 22 times
        for _ in range(22):
            # Inner loop to iterate over child elements from 4 to 13
            for i in range(4, 14):
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                table = soup.find("table", {"id": "listTable"})

                # Extract column names from table headers
                headers = [header.text.replace('\u00a0', ' ').replace('\n', '').replace('\t', '') for header in table.find_all("th")]

                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    row_data = {}
                    for header, col in zip(headers, cols):
                        img = col.find('img')
                        a = col.find('a')
                        if img and 'alt' in img.attrs:
                            row_data[header] = img['alt']
                        else:
                            text = col.text
                            text = text.replace('\u00a0', ' ').replace('\n', '').replace('\t', '')  # Remove unwanted characters
                            row_data[header] = text

                        # Extract onclick attribute value from a elements
                        if a:
                            onclick_value = a.get('onclick')
                            if onclick_value and "getApprDetail" in onclick_value:
                                number = re.search(r"getApprDetail\('(\d+)", onclick_value)
                                if number:
                                    row_data['Reference link'] = number.group(1)  # Add new column with the number

                    data.append(row_data)

                # Move to the next page
                next_page_script = f"""
                var nextPageElement = document.querySelector("#searchForm > div.paging.mHide > a:nth-child({i})");
                if (nextPageElement != null) {{
                    nextPageElement.click();
                }}
                """
                self.driver.execute_script(next_page_script)
                #print outer loop counter and inner loop counter
                print(f"Outer loop counter: {_}")
                print(f"Page {i} of 13")
                time.sleep(3)  # Wait for the page to load
                

        with open("table.json", "w") as outfile:
            json.dump(data, outfile)
        
        
