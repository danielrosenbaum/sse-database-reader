#!/usr/bin/env python
from contextlib import closing
from selenium import webdriver
from selenium.webdriver import Safari
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# function that determines all possible dates from 20130101 to 20151231
def dateGenerator():
    results = []
    days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    years = ["2013", "2014", "2015", "2016"]
    
    # for loop that calculates all the dates as strings
    for year in years:
        for month in months:
            for day in days:
                results.append(year + month + day)

    # return a list of strings where each one is a date
    return results


dates = dateGenerator()

print (dates)

days = []
company_code = []
company_name = []
finance_more = []
finance_buy = []
finance_comp = []
trading_marg = []
margin_sold = []
margin_repay = []

# use safari to get page with javascript generated content
browser = webdriver.Safari()

for date in dates:
    
    browser.get('http://www.sse.com.cn/market/othersdata/margin/detail/index.shtml?marginDate=' + date)
    
    # wait for the page to load
    try:
        WebDriverWait(browser, timeout=5).until(lambda browser: browser.find_element_by_class_name("btn btn-default navbar-btn next-page classPage"))
    except TimeoutException:
        continue

    # find all the possible buttons
    buttons = browser.find_elements_by_name('nameStr')

    # the last of the buttons is the next page button
    next_button = buttons[-1]

    button_num = (int)(buttons[-2].text)
    
    print ("Date: %d", date)

    for i in range(button_num):
        
        # store it to string variable
        page_source = browser.page_source
        
        # create a soup object of the url
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # get the table
        content = soup.find('body')
        container = content.find(id="tableData_tableData2")
        table = container.find('table', class_="table search_")
        
        # find all the values (they are all aligned right)
        rows = table.find_all('tr')
        
        # remove the titles from parsing
        titles = rows.pop(0)
        
        # row[0] is the title so no need to parse those!
        for row in rows:
            
            info = row.find_all('td')
            
            days.append(info[0].get_text())
            company_code.append(info[1].get_text())
            company_name.append(info[2].get_text())
            finance_more.append((int)(info[3].get_text().replace(',', '')))
            finance_buy.append((int)(info[4].get_text().replace(',', '')))
            finance_comp.append((int)(info[5].get_text().replace(',', '')))
            trading_marg.append((int)(info[6].get_text().replace(',', '')))
            margin_sold.append((int)(info[7].get_text().replace(',', '')))
            margin_repay.append((int)(info[8].get_text().replace(',', '')))
            
            d = {"date": days, "company code": company_code, "company name": company_name, "finance more": finance_more, "finance buy": finance_buy, "finance comp": finance_comp, "trading margin": trading_marg, "margin sold": margin_sold, "margin repay": margin_repay}
            
            #create the dataframe
            df = pd.DataFrame(data=d, columns=["date", "company code", "company name", "finance more", "finance buy", "finance comp", "trading margin", "margin sold", "margin repay"])
            
            #write the database to a csv file
            df.to_csv('TaskTwo2016DataV5.csv')
    
        # scroll to the bottom of the page
        browser.execute_script("window.scrollTo(0, 1000);")
        
        # find all the possible buttons
        buttons = browser.find_elements_by_name('nameStr')
        
        # the last of the buttons is the next page button
        next_button = buttons[-1]
        
        # CLICK THE BUTTON
        next_button.click()

print ("Finished Scraping Data!")
