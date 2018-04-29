import sys
import os
sys.path.append(os.getcwd())
import unittest
from uiautomation.HTMLTestRunner import HTMLTestRunner
from testlogin import TestLogin
from testtmlogin import TestTMLogin
from testtmhomepage import TestTMHomePage
from testhomepage import TestHomePage
from testshoppage import TestShopPage
from uiautomation.common import Constants
import logging
import logging.config
import glob

# class Sample():
    
#     def __init__(self):        
#         self.logger = logging.getLogger(Sample.__class__.__name__)
#         logger.debug("initialize the Sample class")

#     def test(self):
#         self.logger.debug("invoke test() function")


def suite():
    suite = unittest.TestSuite()
    # does not work
    # suite.addTest(TestTMLogin('testLogin'))
    # suite.addTest(TestHomePage('testSearchAndView'))
    # suite.addTest(TestTMHomePage('testSearchAndView'))
    suite.addTest(TestShopPage('testSearchAndView'))
    return suite

if __name__ == '__main__':

    # logging.config.fileConfig('logging.conf')

    # # create logger
    # logger = logging.getLogger('simpleLogger')

    # # 'application' code
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

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

