from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import string
import random

class Constants():
    BASE_URL = "https://www.tmall.com"
    LOGIN_URL = "https://login.tmall.com"
    # BASE_URL = "https://www.taobao.com"
    # LOGIN_URL = "https://login.taobao.com"    
    SHOP_URL = "https://actionfoxhw.tmall.com"
    BROWSER_FF = "FireFox"
    BROWSER_IE = "Internet Explorer"
    BROWSER_CHROME = "Chrome"
    BROWSER_PHANTOM = "PhantomJS"
    LOGIN_USERNAME = "username"
    LOGIN_PWD = "password"
    WAIT_TIME_LONG = 20
    WAIT_TIME_SHORT = 5

    SEARCH_KEY_WORDS = "帽子"
    # HOME_PAGE_TITLE = "tmall.com"
    HOME_PAGE_TITLE = "淘宝"

    SHOP_PAGE_TITLE = "快乐狐狸户外旗舰"
    SCROLL_STEP = 500
    SCROLL_INTERVAL = 0.3

    """test output related variables"""
    TEST_BASE_LINE_DIR = "baseline/"
    TEST_RESULT_DIR = "testresult/"
    TEST_REPORT_DIR = "testreport/"

class BaseWebDriver():

    def getDriver(self, browser=Constants.BROWSER_CHROME):
        if browser == Constants.BROWSER_FF:
            return webdriver.Firefox()
        elif browser == Constants.BROWSER_IE:
            return webdriver.Ie("IEDriverServer")
        elif browser == Constants.BROWSER_CHROME:  
            # return browser quickly
            # return webdriver.Chrome('chromedriver')      

            # return browser slowly    
            option=webdriver.ChromeOptions()            
            option.add_argument('--user-data-dir=agentprofile')            
            # option.add_argument('--user-agent=Googlebot')
            browser=webdriver.Chrome(chrome_options=option)
            return browser
        elif browser == Constants.BROWSER_PHANTOM:
            return webdriver.PhantomJS()
        else:
            return webdriver.Firefox()
          
