from selenium.webdriver.support.ui import WebDriverWait
from uiautomation.common import Constants

"""single element base class"""
class BasePageElement(object):
    
    locator = object
    """Base page class that is initialized on every page object class."""
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, Constants.WAIT_TIME_LONG).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the element object"""
        driver = obj.driver
        WebDriverWait(driver, Constants.WAIT_TIME_LONG).until(
            lambda driver: driver.find_element(*self.locator))
        element = driver.find_element(*self.locator)
        return element

"""a set of elements base class"""
class BasePageElements(object):
    
    locator = object

    def __get__(self, obj, owner):
        """Gets the element of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, Constants.WAIT_TIME_LONG).until(
            lambda driver: driver.find_elements(*self.locator))
        elements = driver.find_elements(*self.locator)
        return elements    