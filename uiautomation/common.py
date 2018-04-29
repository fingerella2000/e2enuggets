import sys
import os
sys.path.append(os.getcwd())
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import string
import random
from uiautomation.utility import UserAgentUtil

class Constants():
    TM_BASE_URL = "https://www.tmall.com"
    TB_BASE_URL = "https://www.taobao.com"
    TM_LOGIN_URL = "https://login.tmall.com"
    TB_LOGIN_URL = "https://login.taobao.com"    
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
    HOME_PAGE_TITLE = "tmall.com"
    # HOME_PAGE_TITLE = "淘宝"

    SCROLL_STEP = 500
    SCROLL_INTERVAL = 0.3

    """test output related variables"""
    TEST_BASE_LINE_DIR = "baseline/"
    TEST_RESULT_DIR = "testresult/"
    TEST_REPORT_DIR = "testreport/"

    """browser variables"""
    USER_AGENT_RESOURCE = "resources/useragents.txt"

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
            options=webdriver.ChromeOptions()
            _ua_util = UserAgentUtil()
            _user_agent = _ua_util.getRandomUA(Constants.USER_AGENT_RESOURCE)
            options.add_argument("--start-maximized")
            options.add_argument('--user-data-dir=agentprofile')  
            print(_user_agent)  
            options.add_argument('--user-agent=%s' % _user_agent)    
            options.add_argument('--test-type=%s' % "ui")      
            options.add_argument('--disable-infobars')  
            options.add_argument('--ignore-certificate-errors-spki-list')           
            options.add_argument('--ignore-ssl-errors') 

            proxy = "wx.rocketark.com:80" # IP:PORT or HOST:PORT
            # options.add_argument('--user-agent=Googlebot') 
            options.add_argument('--proxy-server=%s' % proxy)

            browser=webdriver.Chrome(chrome_options=options)
            return browser
        elif browser == Constants.BROWSER_PHANTOM:
            return webdriver.PhantomJS()
        else:
            return webdriver.Firefox()

