import sys
import os
sys.path.append(os.getcwd())
import unittest
from uiautomation.HTMLTestRunner import HTMLTestRunner
from testlogin import TestLogin
from testhomepage import TestHomePage
from testshoppage import TestShopPage
from uiautomation.common import Constants

def suite():
    suite = unittest.TestSuite()
    # suite.addTest(TestLogin('testLogin'))
    # suite.addTest(TestHomePage('testSearchAndView'))
    suite.addTest(TestShopPage('testSearchAndView'))
    return suite

if __name__ == '__main__':
    # with open(Constants.TEST_REPORT_DIR + "report.html", "w") as outfile:
    #     runner = HTMLTestRunner(
    #                     stream=outfile,
    #                     title='Smoke Test Report',
    #                     description=''
    #                     )
    #     runner.run(suite())
    # outfile.closed

    runner = unittest.TextTestRunner()
    runner.run(suite())

