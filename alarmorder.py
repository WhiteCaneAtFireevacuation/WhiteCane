'''
웹에 있는 버튼 누르는 함수
'''
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime
import time

def alarmorder(alarm, URLADDR,control):
    urladdr = URLADDR[alarm]
    path = "C:/Users/Sangcheol Jeon/Desktop/HHT/chromedriver.exe"
    driver = webdriver.Chrome(path)

    driver.get(urladdr)
    time.sleep(5)

    if(control == 0):
        driver.find_element("xpath",'/html/body/a[1]/button').click()
        print("ON")
        driver.close()

    else:
        driver.find_element("xpath",'/html/body/a[2]').click()
        print("OFF")
        driver.close()



addr = ["http://192.168.167.5/"]

alarmorder(0,addr,0)