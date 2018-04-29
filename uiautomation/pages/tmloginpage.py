from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from uiautomation.pages.basepage import BasePage
from uiautomation.common import Constants
from uiautomation.elements import BasePageElement
from selenium.webdriver.common.by import By
import time

class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self

class Locators(object):
    dictionary = {
        "title":(By.CSS_SELECTOR,"#mallPage > div.header > a"),        
        "login_frame":(By.ID,"J_loginIframe"),
        "login_switch":(By.CSS_SELECTOR,"#J_LoginBox > div.hd > div.login-switch"),
        "username":(By.CSS_SELECTOR,"#TPL_username_1"),
        "password":(By.CSS_SELECTOR,"#TPL_password_1"),
        "login":(By.CSS_SELECTOR,"#J_SubmitStatic"),
        "slide_bar":(By.CSS_SELECTOR,"#nc_1_n1z"),
        "slide_pass":(By.CSS_SELECTOR,"#nc_1__scale_text > span > b"),
        "slide_bar_refresh":(By.CSS_SELECTOR,".nc-lang-cnt > a"),
        "slide_bar_container":(By.CSS_SELECTOR,"#nocaptcha")
        
    }

class TitleElement(BasePageElement):
    locator = Locators.dictionary["title"]

class LoginSwitchElement(BasePageElement):
    locator = Locators.dictionary["login_switch"]

class LoginElement(BasePageElement):
    locator = Locators.dictionary["login"]
    
class UserNameElement(BasePageElement):
    locator = Locators.dictionary["username"]

class PasswordElement(BasePageElement):
    locator = Locators.dictionary["password"]

class SlideBarContainerElement(BasePageElement):
    locator = Locators.dictionary["slide_bar_container"]

class SlideBarElement(BasePageElement):
    locator = Locators.dictionary["slide_bar"]
    
class SlidePassElement(BasePageElement):
    locator = Locators.dictionary["slide_pass"]
    
class SlideBarRefreshElement(BasePageElement):
    locator = Locators.dictionary["slide_bar_refresh"]


class TMLoginPage(BasePage):
    login_switch_element = LoginSwitchElement()
    login_element = LoginElement()
    page_title_element = TitleElement()
    login_username_element = UserNameElement()
    login_password_element = PasswordElement()
    slide_bar_container_element = SlideBarContainerElement()
    slide_bar_element = SlideBarElement()
    slide_pass_element = SlidePassElement()
    slide_bar_refresh_element = SlideBarRefreshElement()

    def __init__(self, driver):
        self.driver = driver

    def goTo(self):
        self.driver.get(Constants.TM_LOGIN_URL)    
        return self.isAt()

    def isAt(self):
        return True        

    def login(self, username, password):
        """switch to the login form iframe"""
        self.driver.switch_to_default_content()
        WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.frame_to_be_available_and_switch_to_it(Locators.dictionary["login_frame"]))
        """display PC login form"""
        self.driver.element = self.login_switch_element
        self.driver.element.click()
        _username_element = self.login_username_element
        _password_element = self.login_password_element
        
        """using this way will bypass the slide bar verification"""
        _username_chain_actions = ActionChains(self.driver)
        _username_chain_actions.move_to_element(_username_element).click()
        for c in list(username):
            _username_chain_actions.send_keys(c)
        _username_chain_actions.perform()
        
        _password_chain_actions = ActionChains(self.driver)
        _password_chain_actions.move_to_element(_password_element).click()
        for c in list(password):
            _password_chain_actions.send_keys(c)
        _password_chain_actions.perform()

        """click login button"""
        self.driver.element = self.login_element
        self.driver.element.click()
        
        return Constants.TM_BASE_URL in self.driver.current_url

    def loginBySlideBar(self, username, password):
        """switch to the login form iframe"""
        self.driver.switch_to_default_content()
        WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.frame_to_be_available_and_switch_to_it(Locators.dictionary["login_frame"]))
        """display PC login form"""
        self.driver.element = self.login_switch_element
        self.driver.element.click()
        _username_element = self.login_username_element
        _password_element = self.login_password_element
        
        _username_chain_actions = ActionChains(self.driver)
        _username_chain_actions.move_to_element(_username_element)
        _username_chain_actions.click(_username_element)
        for c in list(username):
            _username_chain_actions.send_keys(c)
        _username_chain_actions.perform()
        
        _password_chain_actions = ActionChains(self.driver)
        _password_chain_actions.move_to_element(_password_element)
        _password_chain_actions.click(_password_element)
        for c in list(password):
            _password_chain_actions.send_keys(c)
        _password_chain_actions.perform()
       
        try:
            """try 3 times to pass the slide bar verification"""
            for i in range(3):
                """locating the slide bar"""
                WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.element_to_be_clickable(Locators.dictionary["slide_bar"]))
                _slide_bar_container_element = self.slide_bar_container_element
                # slide bar container width is 298
                """bypass the slide bar verification"""  
                _slide_bar_element = self.slide_bar_element
                # slide bar button width is 42
                # actions = ActionChains(self.driver)
                actions = Actions(self.driver)
                actions.move_to_element(_slide_bar_element)
                actions.click_and_hold(_slide_bar_element)
                #total x offset is 298-42 = 256
                # actions.move_by_offset(50, 10)
                # actions.move_by_offset(50, 0)
                # actions.move_by_offset(50, -10)
                # actions.move_by_offset(-50, -10)
                # actions.move_by_offset(-50, 0)
                # actions.move_by_offset(50, 10)
                # actions.move_by_offset(50, -10)
                
                # actions.move_by_offset(50, 5)
                # actions.move_by_offset(-50, 5)
                # actions.move_by_offset(50, 5)
                # actions.move_by_offset(-50, 5)
                # actions.move_by_offset(-50, -5)
                # actions.move_by_offset(50, -5)
                # actions.move_by_offset(50, -5)
                # actions.move_by_offset(50, 5)            

                actions.move_by_offset(50, 10)
                actions.move_by_offset(50, -10)
                actions.move_by_offset(50, 0)
                actions.move_by_offset(50, 0)
                actions.move_by_offset(50, -10)
                actions.move_by_offset(8+i, 10+i)
                actions.release(_slide_bar_element)
                actions.perform()

                try:
                    time.sleep(3)
                    """wait untill slide verification passed"""
                    WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.visibility_of_element_located(Locators.dictionary["slide_pass"]))                
                    """then click login button"""
                    self.driver.element = self.login_element
                    self.driver.element.click()
                    return Constants.TM_BASE_URL in self.driver.current_url
                except:
                    """locating the slide bar fresh button and click it to try slide bar again"""
                    self.driver.element = self.slide_bar_refresh_element
                    self.driver.element.click()
                    
                    self.driver.switch_to_default_content()
                    WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.frame_to_be_available_and_switch_to_it(Locators.dictionary["login_frame"]))

                    # raise("cannot pass the slide bar verification!")
                    print("cannot pass the slide bar verification!")
            
        except:
            """if slide bar not found, then click login button directly"""
            self.driver.element = self.login_element
            self.driver.element.click()
            return Constants.TM_BASE_URL in self.driver.current_url
    
        
    
