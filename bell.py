import os
import time
import requests
import urllib.request
from bluepy.btle import Scanner
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

c = 0

s = Service('/usr/local/bin/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(service=s,options=chrome_options)

driver.get("http://192.168.175.5/")


if(c == 0):
    driver.find_element("xpath",'/html/body/a[1]/button').click()

    
else:
    driver.find_element("xpath",'/html/body/a[2]/button').click()
