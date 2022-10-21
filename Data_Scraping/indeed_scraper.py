# Imports Required
from matplotlib.ticker import NullFormatter
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# TODO: Implement Dynamic String for Job Type Search.(Data Analyst, Data Scientist)


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

# Function for Scrapping the data and tranforming it in a Data Frame
def transform(soupData):
    df = pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL','Experience','History','Salary','Location','Skills Required'])
    results = soupData.find(class_='list')

    job_details = results.find_all('article',class_='jobTuple bgWhite br4 mb-8')

    for jobs in job_details:
        # Extracting Job Titles
        title = jobs.find('a',class_='title fw500 ellipsis')
        # print(title.text)

        # Extracting Job URL
        url = jobs.find('a',class_='title fw500 ellipsis').get('href')
        # print(url)

        # Extracting Company Name
        company = jobs.find('a',class_='subTitle ellipsis fleft')
        # print(company.text)

        # Extracting Job Ratings
        rating_span = jobs.find('span',class_='starRating fleft dot')
        if rating_span is None:
            ratings = None
        else:
            ratings = rating_span.text
            # print(ratings)

        # Extracting Job Reviews
        review_a = jobs.find('a',class_='reviewsCount ml-5 fleft blue-text')
        if review_a is None:
            reviews=None
        else:
            reviews = review_a.text
            # print(reviews)

        #Extracting Experience Required
        exp_req_val = jobs.find('li',class_='fleft grey-text br2 placeHolderLi experience')
        # print(exp_req_val)
        if exp_req_val is None:
            experience=None
        else:
            # print(exp_req_val)
            exp_span = exp_req_val.find('span',class_='ellipsis fleft fs12 lh16 expwdth')
            # print(exp_span)
            if exp_span is None:
                experience=None
            else:
                experience = exp_span.text
        # print(experience)


        # Number of days since job posted
        hist = jobs.find("div",["type br2 fleft grey","type br2 fleft green"])
        Post_Hist = hist.find('span',class_='fleft fw500')
        if Post_Hist is None:
            Post_History==None
        else:
            Post_History = Post_Hist.text

        # Extracting Job Salary        
        salary_val = jobs.find(class_='fleft grey-text br2 placeHolderLi salary').find('span')
        if salary_val is None:
            salary=None
        else:
            salary = salary_val.text
        # print(salary.text)

        # Extracting Job Location
        location_val = jobs.find(class_='fleft grey-text br2 placeHolderLi location').find('span')
        if location_val is None:
            location_val=None
        else:
            location = location_val.text
        # print(location.text)

        # Extracting Skills Required
        skills_list=[]
        jobs_val = jobs.find('ul',class_='tags has-description')
        if jobs_val is None:
            jobs_val=None
        else:
            for job_skills in jobs_val:
                skills_list.append(job_skills.text)
        # print(skills_list)

        # print(" "*2)
        df = df.append({'URL':url,'Title':title.text,'Company':company.text,'Ratings':ratings,'Reviews':reviews,'Experience':experience,'History':Post_History,'Salary':salary,'Location':location,'Skills Required':skills_list},ignore_index=True)
    # print(df.head())
    load(df)

# Generating Excel from the data frame created
def load(df):
    # Generating Excel of the Scrapped Data
    df.to_csv("D:/Project_Miscellaneous/DA_Project/Naukri_Data/Naukri_Data/Data_Scraping/Naukri_Data_Raw.csv",mode='a',index=False,header=False)

pageExtracted = int(input("Enter Number of Pages to be Extracted: "))
for i in range(pageExtracted):
    data_scraped = extract(i)
    transform(data_scraped)

# val = extract(2)
# transform(val)