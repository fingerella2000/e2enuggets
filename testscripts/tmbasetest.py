import unittest
import logging
from selenium import webdriver
import sys
import os
sys.path.append(os.getcwd())
from uiautomation.pages.tmloginpage import TMLoginPage
from uiautomation.common import BaseWebDriver
from uiautomation.common import Constants

class TMBaseTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = BaseWebDriver.getDriver(self)
        self.login_page = TMLoginPage(self.driver)
        self.assertTrue(self.login_page.goTo())
        self.assertTrue(self.login_page.login(Constants.LOGIN_USERNAME, Constants.LOGIN_PWD))

