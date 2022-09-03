# Imports Required
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# Function for Accessing the Data related to Naukri.com
def extract(page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f"https://www.naukri.com/data-analyst-jobs-{page}?k=data%20analyst"
    r = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')

    # The data when read via BS4 is encoded this using Selenium Web Dirver to read the same.
    driver = webdriver.Chrome("C:\\BrowserDrivers\\chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    soupData = BeautifulSoup(driver.page_source,'html5lib')
    driver.close
    return soupData

def transform(soupData):
    df =pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL','Experience','Salary','Location','Skills Required'])
    results = soupData.find(class_='list')
    job_details = results.find_all('article',class_='jobTuple bgWhite br4 mb-8')
    for jobs in job_details:
        # Extracting Job Titles

        # Extracting Company Name

        # Extracting Job Ratings

        # Extracting Job Reviews

        # Extracting Job URL

        # Extracting Experience Required

        # Extracting Job Salary

        # Extracting Job Location

        # Extracting Skills Required


val = extract(2)
transform(val)