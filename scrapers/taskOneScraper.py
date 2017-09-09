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
import sqlite3

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

margin_stock_mv = []
margin_flow_mv = []
short_stock_shares = []
short_stock_mv = []
short_flow_mv = []
margin_short_totalstock_mv = []
days = []

browser = webdriver.Safari()

for date in dates:
    
    # use safari to get page with javascript generated content
    browser.get('http://www.sse.com.cn/market/othersdata/margin/detail/index.shtml?marginDate=' + date)
    
    # wait for the page to load
    try:
        WebDriverWait(browser, timeout=5).until(lambda browser: browser.find_element_by_id('idStr'))
    except TimeoutException:
        continue

    # store it to string variable
    page_source = browser.page_source

    # create a soup object of the url
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # get the table
    content = soup.find('body')
    
    containerOne = content.find(id="tableData_tableData1")

    tableOne = containerOne.find('table', class_="table search_")

    # get the date from the html
    days.append(date)

    # find all the values (they are all aligned right)
    rows = tableOne.select(".align_right")

    info = []
    # get all the info from the row
    for row in rows:
        val = float(row.get_text().replace(",", ""))
        info.append(val)

    margin_stock_mv.append(info[0])
    margin_flow_mv.append(info[1])
    short_stock_shares.append(info[2])
    short_stock_mv.append(info[3])
    short_flow_mv.append(info[4])
    margin_short_totalstock_mv.append(info[5])
    
    
    #create the data for the database
    d = {"date": days, "margin_stock_mv": margin_stock_mv, "margin_flow_mv": margin_flow_mv, "short_stock_shares": short_stock_shares, "short_stock_mv": short_stock_mv, "short_flow_mv": short_flow_mv, "margin_short_totalstock_mv": margin_short_totalstock_mv}
    
    #create the dataframe
    df = pd.DataFrame(data=d, columns=["date", "margin_stock_mv", "margin_flow_mv", "short_stock_shares", "short_stock_mv", "short_flow_mv", "margin_short_totalstock_mv"])
    
    #write the database to a csv file
    df.to_csv('task_one_data.csv')

    print (date)
