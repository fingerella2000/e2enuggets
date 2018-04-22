import unittest
import logging
from selenium import webdriver
import sys
import os
sys.path.append(os.getcwd())
from uiautomation.pages.loginpage import LoginPage
from uiautomation.common import BaseWebDriver
from uiautomation.common import Constants


class TestLogin(unittest.TestCase):
    
    def setUp(self):
        self.driver = BaseWebDriver.getDriver(self)
        self.login_page = LoginPage(self.driver)

    """valid test"""
    def testLogin(self):
        self.assertTrue(self.login_page.goTo())
        self.assertTrue(self.login_page.login(Constants.LOGIN_USERNAME, Constants.LOGIN_PWD))

    """bad case"""
    def testInvalidLogin(self):
        pass
    
    """good cases:"""
    """test case should only be failed by one reason"""
    def testInvalidPwd(self):
        pass

    def testInvalidUsernamer(self):
        pass


    def tearDown(self):
        self.driver.close()
