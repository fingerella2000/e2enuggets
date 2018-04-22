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
        # """tmall home page elements"""
        # "search_bar":(By.CSS_SELECTOR,"#mq"),
        # "search_button":(By.CSS_SELECTOR,"#mallSearch > form > fieldset > div > button"),
        # "top1_product":(By.CSS_SELECTOR,"#J_ItemList > div:nth-child(1)"), 
        # "top2_product":(By.CSS_SELECTOR,"#J_ItemList > div:nth-child(2)"),        
        # "top3_product":(By.CSS_SELECTOR,"#J_ItemList > div:nth-child(3)"),
        # "next_page":(By.CSS_SELECTOR,"#content > div > div.ui-page > div > b.ui-page-num > a.ui-page-next")
        
        # """taobao home page elements"""
        "search_bar":(By.CSS_SELECTOR,"#q"),
        "search_button":(By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button"),
        "next_page":(By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.next"),
        "top1_product":(By.CSS_SELECTOR,"#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(2)"), 
        "top2_product":(By.CSS_SELECTOR,"#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(3)"), 
        "top3_product":(By.CSS_SELECTOR,"#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(4)"),
        "search_tmall_only":(By.CSS_SELECTOR,"#J_relative > div.filter-row > div.filter-box.J_LaterHover > div > div.filters > a:nth-child(6) > span.icon.icon-btn-check-big"),
        "tmall_only_is_selected":(By.CSS_SELECTOR,"#J_relative > div.filter-row > div.filter-box.J_LaterHover > div > div.filters > a.filter.icon-tag.J_Ajax.icon-hover > span.icon.icon-btn-check-big")
    }

class SearchBarElement(BasePageElement):
    locator = Locators.dictionary["search_bar"]
class SearchButtonElement(BasePageElement):
    locator = Locators.dictionary["search_button"]
class NextPageElement(BasePageElement):
    locator = Locators.dictionary["next_page"]
class Top1ProductElement(BasePageElement):
    locator = Locators.dictionary["top1_product"]
class Top2ProductElement(BasePageElement):
    locator = Locators.dictionary["top2_product"]
class Top3ProductElement(BasePageElement):
    locator = Locators.dictionary["top3_product"]
class SearchTmallOnlyElement(BasePageElement):
    locator = Locators.dictionary["search_tmall_only"]
class TmallOnlyIsSelectedElement(BasePageElement):
    locator = Locators.dictionary["tmall_only_is_selected"]

class HomePage(BasePage):
    search_bar_element = SearchBarElement()
    search_button_element = SearchButtonElement()
    top1_product_element = Top1ProductElement()
    top2_product_element = Top2ProductElement()
    top3_product_element = Top3ProductElement()
    next_page_element = NextPageElement()
    search_tmall_only_element = SearchTmallOnlyElement()
    tmall_only_is_selected_element = TmallOnlyIsSelectedElement()

    def search(self, keywords):
        WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.title_contains(Constants.HOME_PAGE_TITLE))
       
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
        self.driver.element = self.search_button_element
        self.driver.element.click()        
        # self._scrollDownAndUp()
        return keywords in self.driver.title

    def viewTop3Products(self, tmall_only=False):
        if tmall_only is True:
            self.driver.element = self.search_tmall_only_element
            self.driver.element.click()
            WebDriverWait(self.driver, Constants.WAIT_TIME_SHORT).until(EC.visibility_of_all_elements_located(Locators.dictionary["tmall_only_is_selected"]))  
        self._scrollDownAndUp()

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
            self.viewTop3Products(tmall_only=True)
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
