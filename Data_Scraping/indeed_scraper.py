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
        title = jobs.find('a',class_='title fw500 ellipsis')
        print(title.text)

        # Extracting Job URL
        url = jobs.find('a',class_='title fw500 ellipsis').get('href')
        print(url)

        # Extracting Company Name
        company = jobs.find('a',class_='subTitle ellipsis fleft')
        print(company.text)

        # Extracting Job Ratings
        rating_span = jobs.find('span',class_='starRating fleft dot')
        if rating_span is None:
            continue
        else:
            ratings = rating_span.text
            print(ratings)

        # Extracting Job Reviews
        review_a = jobs.find('a',class_='reviewsCount ml-5 fleft blue-text')
        if review_a is None:
            continue
        else:
            reviews = review_a.text
            print(reviews)

        # Extracting Experience Required
        exp_req = jobs.find(class_='fleft grey-text br2 placeHolderLi experience').find('span')
        print(exp_req.text)

        # Extracting Job Salary        
        salary = jobs.find(class_='fleft grey-text br2 placeHolderLi salary').find('span')
        print(salary.text)

        # Extracting Job Location
        location = jobs.find(class_='fleft grey-text br2 placeHolderLi location').find('span')
        print(location.text)

        # Extracting Skills Required
        skills_list=[]
        for job_skills in jobs.find('ul',class_='tags has-description'):
            skills_list.append(job_skills.text)
        print(skills_list)

        print(" "*2)

val = extract(2)
transform(val)