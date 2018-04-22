import sys
import os
sys.path.append(os.getcwd())
import unittest
import logging
from selenium import webdriver
from basetest import BaseTest
from uiautomation.common import Constants
from uiautomation.common import BaseWebDriver
from uiautomation.pages.homepage import HomePage


# class TestHomePage(BaseTest):    
class TestHomePage(unittest.TestCase):    

    def setUp(self):
        self.driver = BaseWebDriver.getDriver(self)
        self.driver.maximize_window()     
        self.driver.get(Constants.BASE_URL)

    def testSearchAndView(self):        
        self.home_page = HomePage(self.driver)
        self.assertTrue(self.home_page.search(Constants.SEARCH_KEY_WORDS))       
        self.assertTrue(self.home_page.viewTopPages(3))

    def tearDown(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            self.driver.close()
