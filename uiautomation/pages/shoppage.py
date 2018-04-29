from uiautomation.pages.basepage import BasePage
from uiautomation.common import Constants
from uiautomation.elements import BasePageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
import time

class Locators(object):
    dictionary = {
        # """tmall shop page elements"""
        "body":(By.CSS_SELECTOR,"html > body"),
        "search_bar":(By.CSS_SELECTOR,"#mq"),
        "search_all":(By.CSS_SELECTOR,"#J_SearchBtn"),
        "search_shop":(By.CSS_SELECTOR,"#J_CurrShopBtn"),
        "top1_product":(By.CSS_SELECTOR,"#J_ShopSearchResult > div > div.J_TItems > div:nth-child(1) > dl:nth-child(1)"), 
        "top2_product":(By.CSS_SELECTOR,"#J_ShopSearchResult > div > div.J_TItems > div:nth-child(1) > dl:nth-child(2)"),        
        "top3_product":(By.CSS_SELECTOR,"#J_ShopSearchResult > div > div.J_TItems > div:nth-child(1) > dl:nth-child(3)"),
        "next_page":(By.CSS_SELECTOR,"#J_ShopSearchResult > div > div.J_TItems > div.pagination > a.J_SearchAsync.next"),
        "popup_login_username":(By.XPATH,"//*[@id=\"TPL_username_1\"]"),
        "popup_login_password":(By.XPATH,"//*[@id=\"TPL_password_1\"]"),
        "popup_login_frame":(By.CSS_SELECTOR, "#J_sufei > iframe"),
        "popup_login_submit":(By.CSS_SELECTOR, "#J_SubmitStatic")
        
    }

class BodyElement(BasePageElement):
    locator = Locators.dictionary["body"]
class SearchBarElement(BasePageElement):
    locator = Locators.dictionary["search_bar"]
class PopupLoginFrameElement(BasePageElement):
    locator = Locators.dictionary["popup_login_frame"]
class PopupLoginSubmitElement(BasePageElement):
    locator = Locators.dictionary["popup_login_submit"]
class PopupLoginUNElement(BasePageElement):
    locator = Locators.dictionary["popup_login_username"]
class PopupLoginPWDElement(BasePageElement):
    locator = Locators.dictionary["popup_login_password"]
class SearchAllElement(BasePageElement):
    locator = Locators.dictionary["search_all"]
class SearchShopElement(BasePageElement):
    locator = Locators.dictionary["search_shop"]
class NextPageElement(BasePageElement):
    locator = Locators.dictionary["next_page"]
class Top1ProductElement(BasePageElement):
    locator = Locators.dictionary["top1_product"]
class Top2ProductElement(BasePageElement):
    locator = Locators.dictionary["top2_product"]
class Top3ProductElement(BasePageElement):
    locator = Locators.dictionary["top3_product"]

class ShopPage(BasePage):
    search_bar_element = SearchBarElement()
    search_all_element = SearchAllElement()
    search_shop_element = SearchShopElement()
    top1_product_element = Top1ProductElement()
    top2_product_element = Top2ProductElement()
    top3_product_element = Top3ProductElement()
    next_page_element = NextPageElement()

    def search(self, keywords):
        WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.visibility_of_any_elements_located(Locators.dictionary["body"]))
       
        self._scrollDownAndUp()
        """entering search keywords"""
        _search_bar = self.search_bar_element
        _keywords_chain_actions = ActionChains(self.driver)
        _keywords_chain_actions.move_to_element(_search_bar)
        _keywords_chain_actions.click(_search_bar)
        for c in list(keywords):
            _keywords_chain_actions.send_keys(c)
        _keywords_chain_actions.perform()

        """click search button"""
        self.driver.element = self.search_shop_element
        self.driver.element.click()     
        WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.visibility_of_any_elements_located(Locators.dictionary["body"]))
        self._scrollDownAndUp()
        return True

    def viewTop3Products(self):
        _top1_product = self.top1_product_element
        _top1_product_actions = ActionChains(self.driver)
        _top1_product_actions.move_to_element(_top1_product).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
        self._viewNewTabAndCloseAfter()

        _top2_product = self.top2_product_element
        _top2_product_actions = ActionChains(self.driver)
        _top2_product_actions.move_to_element(_top2_product).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
        self._viewNewTabAndCloseAfter()

        _tope3_product = self.top3_product_element
        _tope3_product_actions = ActionChains(self.driver)
        _tope3_product_actions.move_to_element(_tope3_product).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
        self._viewNewTabAndCloseAfter()
        return True

    def viewTopPages(self, number_of_pages):
        for i in range(number_of_pages):
            print("viewing page: " + str(i+1))
            self.viewTop3Products()
            if i+1 == number_of_pages:
                continue
            self.driver.element = self.next_page_element 
            self.driver.element.click()
            self.driver.switch_to_default_content()   
        return True

    def _viewNewTabAndCloseAfter(self):        
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self._scrollDownAndUp()
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.switch_to_default_content()

    def _scrollDownAndUp(self):
        _scroll_step = Constants.SCROLL_STEP  
        _scroll_interval = Constants.SCROLL_INTERVAL
        """scroll down"""   
        _last_height = self.driver.execute_script("return document.body.scrollHeight")
        for h in range(int(_last_height/_scroll_step)):
            time.sleep(_scroll_interval)
            self.driver.execute_script("window.scrollTo(0," + str(_scroll_step*(h+1)) + ");")
        """scroll up"""   
        _last_height = self.driver.execute_script("return document.body.scrollHeight")
        for h in range(int(_last_height/_scroll_step)):
            time.sleep(_scroll_interval)
            self.driver.execute_script("window.scrollTo(0," + str(_last_height - _scroll_step*(h+1)) + ");")
        self.driver.execute_script("window.scrollTo(0, 0);")
