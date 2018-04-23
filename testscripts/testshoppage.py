import sys
import os
sys.path.append(os.getcwd())
import unittest
import logging
from selenium import webdriver
from basetest import BaseTest
from uiautomation.common import Constants
from uiautomation.common import BaseWebDriver
from uiautomation.pages.shoppage import ShopPage

   
# class TestShopPage(BaseTest):   
class TestShopPage(unittest.TestCase):    

    def setUp(self):
        self.driver = BaseWebDriver.getDriver(self)
        self.driver.get(Constants.SHOP_URL)

    def testSearchAndView(self):  
        self.driver.get(Constants.SHOP_URL)      
        self.shop_page = ShopPage(self.driver)
        self.assertTrue(self.shop_page.search(Constants.SEARCH_KEY_WORDS))       
        self.assertTrue(self.shop_page.viewTopPages(2))

    def tearDown(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            # self.driver.close()
