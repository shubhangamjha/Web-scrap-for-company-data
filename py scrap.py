from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

df1 = pd.read_excel("C:\\Users\\shubh\\Desktop\\Desktop\\programming\\UptoSkill\\Web Scrapping\\zaubacorp.xlsx")

all_company_data=[]

# Initialize WebDriver
driver = webdriver.Chrome()

# Define a function to scrape data for a single company
def scrape_company_data(url):
    driver.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='table table-striped')
    
    if not tables:
        return None
    
    data = {}
    
    # Scrape data from tables
    rows1 = tables[0].find_all('tr')
    rows2 = tables[3].find_all('tr')
    rows3 = tables[4].find_all('tr')
    
    for row in rows1:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) >= 2:
            data[cols[0]] = cols[1]
    
    for row in rows2:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) >= 2:
            data[cols[0]] = cols[1]
            
    for row in rows3:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) >= 2:
            data[cols[0]] = cols[1]
    
    # Scrape contact details
    contact_details = soup.find_all('div', class_='col-12')
    if contact_details:
        contact_details_row = contact_details[0].find_all('p')
        if len(contact_details_row) >= 4:
            email = contact_details_row[0].text.split(':')[1].strip()
            website = contact_details_row[1].text.split(':')[1].strip()
            address = contact_details_row[3].text.strip()
            
            data['Email'] = email
            data['Website'] = website
            data['Address'] = address
    
    return data

# Scrape data for all companies
all_company_data = []
for url in df1["Url"].iloc[1301:10000]:
    company_data = scrape_company_data(url)
    if company_data:
        all_company_data.append(company_data)

# Close the WebDriver
driver.quit()

